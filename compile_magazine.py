#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
import requests

# Add current directory to path to import photo_search
sys.path.append(str(Path(__file__).parent))
try:
    import photo_search
except ImportError:
    photo_search = None

SCRIPT_DIR = Path(__file__).parent
PHOTO_DIR = SCRIPT_DIR / "Database photos"
PHOTO_DIR.mkdir(exist_ok=True)

# Wikimedia API headers
HEADERS = {
    "User-Agent": "NamedniPhotoBot/2.0 (historical research; contact: namedniturkeyproject@gmail.com)",
    "Api-User-Agent": "NamedniPhotoBot/2.0 (historical research; contact: namedniturkeyproject@gmail.com)"
}

# Load categories mapping from fenomeny_80h_baza.md
def load_categories_mapping() -> dict[str, str]:
    mapping = {}
    baza_path = SCRIPT_DIR / "fenomeny_80h_baza.md"
    if not baza_path.exists():
        return mapping
    
    current_cat = "Общество"
    content = baza_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        # Match markdown headers or table rows
        if "|" in line and "стр." not in line.lower() and "---" not in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                title = parts[1].lower()
                cat = parts[3]
                mapping[title] = cat
    return mapping

def robust_get(url: str, params: dict | None = None, headers: dict | None = None, timeout: int = 10, max_retries: int = 5) -> requests.Response | None:
    backoff = 1.0
    for attempt in range(max_retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout)
            if r.status_code == 429:
                print(f"  [429 Too Many Requests, retrying in {backoff}s...]")
                time.sleep(backoff)
                backoff *= 2.0
                continue
            r.raise_for_status()
            return r
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"  [HTTP request failed: {e}]")
                return None
            print(f"  [Error: {e}, retrying in {backoff}s...]")
            time.sleep(backoff)
            backoff *= 2.0
    print("  [HTTP request failed: Max retries reached with status 429]")
    return None

def robust_get_image_info(file_title: str) -> dict | None:
    params = {
        "action":  "query",
        "titles":  file_title,
        "prop":    "imageinfo",
        "iiprop":  "url|extmetadata|size|mime",
        "iiurlwidth": photo_search.THUMB_W if photo_search else 800,
        "format":  "json",
    }
    # photo_search might be None, fallback API URI
    api_url = photo_search.API if photo_search else "https://commons.wikimedia.org/w/api.php"
    r = robust_get(api_url, params=params, headers=HEADERS)
    if not r:
        return None
    try:
        pages = r.json().get("query", {}).get("pages", {})
        page  = next(iter(pages.values()))
        infos = page.get("imageinfo", [])
        if not infos:
            return None
        info = infos[0]
        meta = info.get("extmetadata", {})

        license_raw = meta.get("LicenseShortName", {}).get("value", "").lower()
        mime        = info.get("mime", "")

        if photo_search:
            if mime not in photo_search.GOOD_MIMES:
                return None
            license_ok = any(good in license_raw for good in photo_search.GOOD_LICENSES)
            if not license_ok and license_raw:
                return None

        return {
            "title":       file_title,
            "full_url":    info.get("url"),
            "thumb_url":   info.get("thumburl"),
            "width":       info.get("width", 0),
            "height":      info.get("height", 0),
            "mime":        mime,
            "license":     meta.get("LicenseShortName", {}).get("value", "unknown"),
            "author":      photo_search._strip_html(meta.get("Artist", {}).get("value", "")) if photo_search else "",
            "date":        (meta.get("DateTimeOriginal", {}).get("value", "")
                            or meta.get("DateTime",         {}).get("value", "")),
            "description": photo_search._strip_html(meta.get("ImageDescription", {}).get("value", "")) if photo_search else "",
            "commons_url": "https://commons.wikimedia.org/wiki/" + file_title.replace(" ", "_"),
        }
    except Exception:
        return None

def robust_download_image(url: str, dest: Path) -> bool:
    backoff = 1.0
    for attempt in range(5):
        try:
            r = requests.get(url, headers=HEADERS, timeout=40, stream=True)
            if r.status_code == 429:
                time.sleep(backoff)
                backoff *= 2.0
                continue
            r.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            return True
        except Exception:
            if attempt == 4:
                return False
            time.sleep(backoff)
            backoff *= 2.0
    return False

# Search and download the best photo
def auto_get_photo(year: str, article_title: str) -> tuple[str, str] | None:
    """
    Searches Commons, downloads the best image, and returns (local_path_rel, caption)
    """
    # Build local path details first
    slug = re.sub(r"[^\w\s]", "", article_title).strip().lower()
    slug = re.sub(r"\s+", "_", slug)[:28]
    
    # Try finding an existing image in Database photos
    for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        filename = f"{year}_{slug}{ext}"
        dest = PHOTO_DIR / filename
        if dest.exists():
            caption = f"{article_title} ({year})"
            sidecar = dest.with_suffix(".txt")
            if sidecar.exists():
                try:
                    sidecar_lines = sidecar.read_text(encoding="utf-8").splitlines()
                    for line in sidecar_lines:
                        if line.startswith("Caption:"):
                            caption = line.replace("Caption:", "").strip()
                            break
                except Exception:
                    pass
            return f"Database photos/{filename}", caption

    if not photo_search:
        return None

    queries = []
    # Try importing from photo_search TOPICS
    if hasattr(photo_search, "TOPICS") and year in photo_search.TOPICS:
        for art, q_list in photo_search.TOPICS[year]:
            if art.lower() in article_title.lower() or article_title.lower() in art.lower():
                queries = q_list
                break
    
    if not queries:
        queries = [
            f"Turkey {article_title} {year}",
            f"Türkiye {article_title} {year}",
            f"{article_title} {year}"
        ]

    # Search Commons
    all_candidates = []
    for q in queries[:2]:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{q} filetype:bitmap",
            "srnamespace": 6,
            "srlimit": 5,
            "format": "json"
        }
        r = robust_get(photo_search.API, params=params, headers=HEADERS)
        if r:
            try:
                results = r.json().get("query", {}).get("search", [])
                for res in results:
                    title = res["title"]
                    info = robust_get_image_info(title)
                    if info:
                        info["_score"] = photo_search.score_image(info)
                        all_candidates.append(info)
                    time.sleep(1.0)
            except Exception as e:
                print(f"  [Parsing search results failed for query '{q}': {e}]")
        time.sleep(2.0)

    if not all_candidates:
        return None

    all_candidates.sort(key=lambda x: x["_score"], reverse=True)
    best = all_candidates[0]

    # Download
    ext = Path(best["title"]).suffix.lower() or ".jpg"
    filename = f"{year}_{slug}{ext}"
    dest = PHOTO_DIR / filename
    
    print(f"  Auto-downloading photo for '{article_title}' -> {filename}")
    if robust_download_image(best["full_url"], dest):
        caption = photo_search.suggest_caption(best, article_title, year)
        sidecar = dest.with_suffix(".txt")
        sidecar.write_text(
            f"Year:     {year}\n"
            f"Article:  {article_title}\n"
            f"Caption:  {caption}\n"
            f"Source:   {best['commons_url']}\n"
            f"License:  {best['license']}\n",
            encoding="utf-8"
        )
        return f"Database photos/{filename}", caption
    return None

# Dictionary mapping each year to summary and section title
YEAR_METADATA = {
    "1942": {
        "summary": "Хлебные карточки · Налог на богатство · Трагедия Струмы",
        "section": "Раздел I — Военные годы"
    },
    "1980": {
        "summary": "Военный переворот · Экономический шок · Конец эпохи",
        "section": "Раздел II — Политика и власть"
    },
    "1981": {
        "summary": "Покушение на Папу · Дефицит лиры · Рождение Walkman",
        "section": "Раздел III — Время молчания"
    },
    "1982": {
        "summary": "Новая Конституция · Суд над Бюлент Эрсой · Бегство Гюнея",
        "section": "Раздел IV — Режим Эврена"
    },
    "1983": {
        "summary": "Выборы Озала · Раздел Кипра · Взрыв в Орли",
        "section": "Раздел V — Гражданское правление"
    },
    "1984": {
        "summary": "Начало борьбы с ПКК · Введение КДВ · Цветное ТВ",
        "section": "Раздел VI — Новые реформы"
    },
    "1985": {
        "summary": "Болгарский кризис · Мост через Босфор · Первый СПИД",
        "section": "Раздел VII — Анатолийский подъем"
    },
    "1986": {
        "summary": "Чернобыльское облако · Гамбургер в Стамбуле · Капитал Коч",
        "section": "Раздел VIII — Внешние ветры"
    },
    "1987": {
        "summary": "Снятие запретов · Триумф Наима · Крылья THY",
        "section": "Раздел IX — Эпоха выборов"
    },
    "1988": {
        "summary": "Покушение на Озала · Золото Сеула · Возвращение Примадонны",
        "section": "Раздел X — Культурные бури"
    },
    "1989": {
        "summary": "Озал президент · Первое частное ТВ · Исход турок",
        "section": "Раздел XI — Конец ANAP"
    },
    "1990": {
        "summary": "Война в Заливе · Политический террор · Мусорный кризис",
        "section": "Раздел XII — Смутное время"
    },
    "1991": {
        "summary": "Забастовка в Зонгулдаке · Конец эпохи Озала · Курдские беженцы",
        "section": "Раздел XIII — Хроника перемен"
    }
}

def extract_pull_quote(paragraphs: list[str]) -> str | None:
    # 1. Search for a sentence in double quotes «...»
    for p in paragraphs:
        match = re.search(r'«([^»]{15,100})»', p)
        if match:
            return f"«{match.group(1)}»"
            
    # 2. Or search for the first sentence of the second paragraph
    if len(paragraphs) >= 2:
        sentences = re.split(r'(?<=[.!?])\s+', paragraphs[1])
        if sentences:
            first_sent = sentences[0].strip()
            first_sent = re.sub(r'\*\*|\*', '', first_sent)
            if 20 <= len(first_sent) <= 120:
                if not (first_sent.startswith("«") and first_sent.endswith("»")):
                     return f"«{first_sent.rstrip('.')}»"
                return first_sent
                
    # 3. Fallback: first sentence of first paragraph
    if len(paragraphs) >= 1:
        sentences = re.split(r'(?<=[.!?])\s+', paragraphs[0])
        if sentences:
            first_sent = sentences[0].strip()
            first_sent = re.sub(r'\*\*|\*', '', first_sent)
            if 20 <= len(first_sent) <= 120:
                return f"«{first_sent.rstrip('.')}»"
                
    return None

def get_pill_label(title: str, year: str, category: str) -> str:
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    title_lower = title.lower()
    for m in months:
        if m in title_lower:
            match = re.search(rf'(\d+)\s+{m}', title_lower)
            if match:
                day = match.group(1)
                return f"{day} {m.upper()} {year}"
            return f"{title.upper()} {year}"
    return f"{category.upper()} {year}"

def get_fallback_caption(title: str, year: str) -> str:
    months_genitive = {
        "января": "января", "февраля": "февраля", "марта": "марта", "апреля": "апреля",
        "мая": "мая", "июня": "июня", "июля": "июля", "августа": "августа",
        "сентября": "сентября", "октября": "октября", "ноября": "ноября", "декабря": "декабря"
    }
    title_lower = title.lower()
    for m in months_genitive:
        if m in title_lower:
            match = re.search(rf'(\d+)\s+{m}', title_lower)
            if match:
                day = match.group(1)
                return f"События {title_lower}. Анкара, {day} {months_genitive[m]} {year} г."
            return f"События в Турции. {title}, {year} г."
    return f"{title}. Исторический снимок. Турция, {year} г."

# Parse markdown file
def parse_markdown(year: str) -> dict:
    md_path = SCRIPT_DIR / f"{year}.md"
    if not md_path.exists():
        sys.exit(f"File {year}.md does not exist.")
    
    content = md_path.read_text(encoding="utf-8")
    
    # Split content by H2 headers
    sections = re.split(r'\n##\s+', content)
    
    articles = []
    chronology = []
    symbols = []
    
    # Category mappings
    cat_mapping = load_categories_mapping()

    for sec in sections[1:]:
        lines = sec.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body_lines = lines[1:]
        
        # Check if it is Chronology or Symbols
        if "ХРОНОЛОГИЯ" in title.upper():
            current_month = "Январь"
            for line in body_lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("**") and line.endswith("**"):
                    current_month = line.replace("**", "").strip()
                elif line.startswith("-"):
                    item_text = line[1:].strip()
                    # extract date if exists, e.g. "23 янв — ..."
                    date_part = ""
                    text_part = item_text
                    if " — " in item_text:
                        date_part, text_part = item_text.split(" — ", 1)
                    elif " - " in item_text:
                        date_part, text_part = item_text.split(" - ", 1)
                    chronology.append({
                        "month": current_month,
                        "date": date_part.strip(),
                        "text": text_part.strip()
                    })
        elif "СИМВОЛЫ" in title.upper():
            for line in body_lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("**"):
                    # format: **Symbol.** Description
                    match = re.match(r'\*\*(.*?)\*\*(.*)', line)
                    if match:
                        sym_title = match.group(1).strip().rstrip(".")
                        sym_desc = match.group(2).strip()
                        symbols.append({
                            "title": sym_title,
                            "desc": sym_desc
                        })
        else:
            # Regular article
            lede = ""
            paragraphs = []
            refs = ""
            
            # Category search
            category = "Общество"
            for key, val in cat_mapping.items():
                if key in title.lower() or title.lower() in key:
                    category = val
                    break
            
            for line in body_lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("---"):
                    continue
                if line.startswith("**") and line.endswith("**"):
                    lede = line.replace("**", "").strip()
                elif line.startswith("*(") and line.endswith(")*"):
                    refs = line[2:-2].strip()
                else:
                    paragraphs.append(line)
                    
            articles.append({
                "title": title,
                "category": category,
                "lede": lede,
                "paragraphs": paragraphs,
                "refs": refs
            })
            
    return {
        "year": year,
        "articles": articles,
        "chronology": chronology,
        "symbols": symbols
    }

# Generate HTML
def generate_html(data: dict) -> str:
    year = data["year"]
    metadata = YEAR_METADATA.get(str(year), {
        "summary": "События, люди и явления, определившие облик Турции",
        "section": "Раздел — История и современность"
    })
    summary = metadata["summary"]
    section = metadata["section"]

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Намедни по-турецки — {year}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Sans:wght@400;700;900&display=swap');

  :root {{
    --cream: #f5f0e8;
    --dark: #1a1410;
    --burgundy: #6b0f1a;
    --red: #c0392b;
    --gold: #b8860b;
    --midgray: #5a5248;
    --lightgray: #d4cfc8;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: var(--cream);
    color: var(--dark);
    font-family: 'PT Serif', Georgia, serif;
    font-size: 16px;
    line-height: 1.7;
  }}

  /* ======= STICKY HEADER (Burgundy Notebook style) ======= */
  header {{
    background: linear-gradient(135deg, #5a0a14 0%, #7d121e 100%);
    color: #ffffff;
    padding: 0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  }}

  .header-inner {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 20px 40px;
    display: flex;
    align-items: center;
    gap: 40px;
  }}

  .year-block {{
    flex-shrink: 0;
  }}

  .year-number {{
    font-family: 'PT Sans', sans-serif;
    font-size: 100px;
    font-weight: 900;
    line-height: 1;
    color: #ffffff;
    letter-spacing: -2px;
  }}

  .header-divider {{
    width: 2px;
    height: 70px;
    background-color: rgba(255, 255, 255, 0.25);
  }}

  .header-text {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-family: 'PT Sans', sans-serif;
  }}

  .header-main-title {{
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #ffffff;
    text-transform: uppercase;
  }}

  .header-summary {{
    font-size: 14px;
    color: #e5cfd2;
    font-weight: 400;
  }}

  .header-section {{
    font-size: 12px;
    color: var(--gold);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
  }}

  .toc {{
    background: var(--dark);
    color: var(--cream);
    border-top: 1px solid #2a2520;
  }}

  .toc-inner {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 15px 40px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px 28px;
    font-family: 'PT Sans', sans-serif;
    font-size: 13px;
  }}

  .toc span {{ color: var(--gold); margin-right: 4px; font-weight: 700; }}
  .toc a {{ color: #c8c0b0; text-decoration: none; transition: color 0.2s; }}
  .toc a:hover {{ color: var(--cream); }}

  main {{
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 40px 80px;
  }}

  /* ======= ARTICLE LAYOUT ======= */
  .phenomenon {{
    margin: 60px 0;
    padding-bottom: 60px;
    border-bottom: 1px solid var(--lightgray);
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}

  .pill-label {{
    padding: 5px 12px;
    background-color: var(--burgundy);
    color: #ffffff;
    display: inline-block;
    font-weight: 700;
    font-family: 'PT Sans', sans-serif;
    font-size: 11px;
    letter-spacing: 1px;
    border-radius: 2px;
    width: fit-content;
    text-transform: uppercase;
    margin-bottom: 8px;
  }}

  .phenom-title {{
    font-family: 'PT Sans', sans-serif;
    font-size: 36px;
    font-weight: 900;
    line-height: 1.15;
    margin-bottom: 10px;
    color: var(--dark);
    text-transform: uppercase;
    letter-spacing: -0.5px;
  }}

  .phenom-lede {{
    border-left: 5px solid var(--burgundy);
    padding-left: 20px;
    margin: 10px 0 25px 0;
    font-style: italic;
    font-weight: 700;
    font-size: 18px;
    line-height: 1.6;
    color: #1a1410;
    font-family: 'PT Serif', serif;
  }}

  .phenom-body-text {{
    column-count: 2;
    column-gap: 40px;
    text-align: justify;
    color: #2a2420;
    font-size: 15px;
    line-height: 1.75;
  }}

  .pull-quote {{
    break-inside: avoid;
    border-top: 1px solid rgba(107, 15, 26, 0.3);
    border-bottom: 1px solid rgba(107, 15, 26, 0.3);
    padding: 18px 0;
    margin: 20px 0;
    color: var(--burgundy);
    font-family: 'PT Serif', Georgia, serif;
    font-size: 17px;
    font-weight: 700;
    font-style: italic;
    line-height: 1.5;
  }}

  .phenom-image {{ margin: 20px 0; width: 100%; }}
  .phenom-image img {{ width: 100%; max-height: 550px; object-fit: cover; display: block; filter: sepia(15%) contrast(1.02); border: 1px solid var(--lightgray); }}
  .img-caption {{ font-family: 'PT Sans', sans-serif; font-size: 12px; color: var(--midgray); margin-top: 10px; line-height: 1.5; font-style: italic; }}

  /* ======= FALLBACK ARCHIVAL PHOTO SLOT ======= */
  .fallback-box {{
    background-color: #eae6de;
    border: 1px solid #d4cfc8;
    padding: 50px 30px;
    text-align: center;
    font-family: 'PT Sans', sans-serif;
    color: #5a5248;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin: 20px 0 10px 0;
    min-height: 220px;
  }}
  
  .fallback-image-icon {{
    width: 48px;
    height: 48px;
    border: 3px solid rgba(90, 82, 72, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 5px;
  }}
  
  .fallback-image-icon::after {{
    content: "";
    width: 18px;
    height: 18px;
    border: 3px solid rgba(90, 82, 72, 0.4);
  }}

  .fallback-title {{
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #5a5248;
  }}
  
  .fallback-subtitle {{
    font-size: 12px;
    color: #8a8278;
  }}
  
  .fallback-caption {{
    font-family: 'PT Serif', Georgia, serif;
    font-size: 13px;
    color: #5a5248;
    font-style: italic;
    margin-top: 8px;
    margin-bottom: 25px;
    line-height: 1.5;
  }}

  /* ======= CHRONOLOGY & SYMBOLS SECTION ======= */
  .chronicle {{ background: var(--dark); color: var(--cream); margin: 70px -40px 0; padding: 50px 40px; }}
  .chronicle-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 6px 40px; }}
  .chronicle-item {{ display: flex; gap: 14px; padding: 12px 0; border-bottom: 1px solid #2a2520; font-size: 14px; }}
  .chronicle h2 {{ font-family: 'PT Sans', sans-serif; font-size: 13px; letter-spacing: 4px; text-transform: uppercase; color: var(--gold); margin-bottom: 30px; font-weight: 400; }}

  .section-divider {{
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 60px 0 0;
  }}

  .section-divider span {{
    font-family: 'PT Sans', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--midgray);
    white-space: nowrap;
  }}

  .section-divider::before,
  .section-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--lightgray);
  }}

  .symbols-section {{
    margin: 60px 0;
    background: var(--cream);
    border: 1px solid var(--lightgray);
    padding: 40px;
  }}

  .symbols-title {{
    font-family: 'PT Sans', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--midgray);
    margin-bottom: 30px;
  }}

  .symbols-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px 40px;
  }}

  .symbol-item {{
    display: flex;
    flex-direction: column;
  }}

  .symbol-name {{
    font-family: 'PT Serif', Georgia, serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--burgundy);
    line-height: 1.3;
    margin-bottom: 10px;
  }}

  .symbol-desc {{
    font-family: 'PT Serif', Georgia, serif;
    font-size: 14px;
    color: #2a2420;
    line-height: 1.6;
    text-align: justify;
  }}

  .running-footer {{ display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--lightgray); padding-top: 15px; margin-top: 60px; font-family: 'PT Sans', sans-serif; font-size: 11px; color: var(--midgray); text-transform: uppercase; letter-spacing: 1px; }}

  @media (max-width: 900px) {{
    .symbols-grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}

  @media (max-width: 768px) {{
    .header-inner {{ flex-direction: column; gap: 20px; padding: 40px 20px 30px; }}
    .year-number {{ font-size: 80px; }}
    .header-divider {{ display: none; }}
    main {{ padding: 0 20px 60px; }}
    .phenom-body-text {{ column-count: 1; }}
    .chronicle {{ margin: 60px -20px 0; padding: 40px 20px; }}
  }}

  @media (max-width: 600px) {{
    .symbols-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="year-block">
      <div class="year-number">{year}</div>
    </div>
    <div class="header-divider"></div>
    <div class="header-text">
      <div class="header-main-title">ТУРЦИЯ: ГОД ЗА ГОДОМ</div>
      <div class="header-summary">{summary}</div>
      <div class="header-section">{section}</div>
    </div>
  </div>
</header>

<nav class="toc">
  <div class="toc-inner">
"""
    
    # Add TOC items
    for idx, art in enumerate(data["articles"]):
        slug = re.sub(r"[^\w\s]", "", art["title"]).strip().lower().replace(" ", "-")
        html += f'    <div><span>►</span><a href="#{slug}">{art["title"]}</a></div>\n'
    
    if data["chronology"]:
        html += f'    <div><span>►</span><a href="#chronicle">Хроника года</a></div>\n'
    if data["symbols"]:
        html += f'    <div><span>►</span><a href="#symbols">Символы года</a></div>\n'
        
    html += """  </div>
</nav>

<main>
"""

    # Add Articles
    for idx, art in enumerate(data["articles"]):
        slug = re.sub(r"[^\w\s]", "", art["title"]).strip().lower().replace(" ", "-")
        
        # 1. Pill label
        pill_label = get_pill_label(art["title"], year, art["category"])
        
        # 2. Lede html
        lede_html = ""
        if art["lede"]:
            lede_html = f'  <div class="phenom-lede">{art["lede"]}</div>\n'
            
        # 3. Image block
        photo_info = auto_get_photo(year, art["title"])
        image_html = ""
        if photo_info:
            img_path, img_caption = photo_info
            image_html = f"""  <div class="phenom-image">
    <img src="{img_path}" alt="{art["title"]}">
    <div class="img-caption">{img_caption}</div>
  </div>\n"""
        else:
            # Archival fallback caption
            fallback_cap = get_fallback_caption(art["title"], year)
            image_html = f"""  <div class="phenom-image-fallback">
    <div class="fallback-box">
      <div class="fallback-image-icon"></div>
      <div class="fallback-title">Место для архивного фото</div>
      <div class="fallback-subtitle">(Wikimedia Commons / TRT-архив)</div>
    </div>
    <div class="fallback-caption">Пример подписи: {fallback_cap}</div>
  </div>\n"""
  
        # 4. Pull Quote & Columns Paragraphs
        paragraphs = art["paragraphs"]
        pull_quote = extract_pull_quote(paragraphs)
        
        paragraphs_html = ""
        pq_inserted = False
        
        for p_idx, p in enumerate(paragraphs):
            p_clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
            p_clean = re.sub(r'\*(.*?)\*', r'<em>\1</em>', p_clean)
            
            paragraphs_html += f'    <p>{p_clean}</p>\n'
            
            # Insert pull quote in the middle of columns
            if pull_quote and not pq_inserted:
                if len(paragraphs) >= 3 and p_idx == 1:
                    paragraphs_html += f'    <div class="pull-quote">{pull_quote}</div>\n'
                    pq_inserted = True
                elif len(paragraphs) < 3 and p_idx == 0:
                    paragraphs_html += f'    <div class="pull-quote">{pull_quote}</div>\n'
                    pq_inserted = True
                    
        if pull_quote and not pq_inserted:
            paragraphs_html += f'    <div class="pull-quote">{pull_quote}</div>\n'
            
        if art["refs"]:
            paragraphs_html += f'    <p style="margin-top:16px;font-style:italic;color:var(--midgray);">{art["refs"]}</p>\n'

        html += f'  <div class="section-divider"><span>{art["category"]}</span></div>\n\n'
        html += f'  <article class="phenomenon" id="{slug}">\n'
        html += f'    <div class="pill-label">{pill_label}</div>\n'
        html += f'    <h2 class="phenom-title">{art["title"]}</h2>\n'
        html += lede_html
        html += image_html
        html += f'    <div class="phenom-body-text">\n'
        html += paragraphs_html
        html += f'    </div>\n'
        html += f'  </article>\n\n'

    # Chronology
    if data["chronology"]:
        html += f"""  <div class="section-divider" id="chronicle"><span>Хроника</span></div>
  <section class="chronicle">
    <h2>ХРОНОЛОГИЯ {year}</h2>
    <div class="chronicle-grid">
"""
        for item in data["chronology"]:
            html += f"""      <div class="chronicle-item">
        <div class="chronicle-date">{item["date"]}</div>
        <div class="chronicle-text"><strong>{item["month"]}</strong> · {item["text"]}</div>
      </div>\n"""
        html += """    </div>
  </section>\n\n"""

    # Symbols
    if data["symbols"]:
        html += f"""  <div class="section-divider" id="symbols"><span>Символы</span></div>
  <section class="symbols-section">
    <div class="symbols-title">СИМВОЛЫ {year} ГОДА</div>
    <div class="symbols-grid">
"""
        for item in data["symbols"]:
            html += f"""      <div class="symbol-item">
        <div class="symbol-name">{item["title"]}</div>
        <div class="symbol-desc">{item["desc"]}</div>
      </div>\n"""
        html += """    </div>
  </section>\n\n"""

    html += f"""</main>

<main style="margin: 0 auto 50px; max-width: 1300px; padding: 0 40px;">
  <div class="running-footer">
    <div><a href="index.html" style="color: inherit; text-decoration: none;">Турция: год за годом</a></div>
    <div>{year} — стр. 1</div>
    <div>Исторический архив · Не для переиздания</div>
  </div>
</main>

</body>
</html>
"""
    return html

def compile_pdf(year: str):
    html_file = SCRIPT_DIR / f"{year}.html"
    pdf_file = SCRIPT_DIR / f"{year}.pdf"
    
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_file}",
        str(html_file)
    ]
    print(f"Compiling {html_file.name} to {pdf_file.name} ...")
    subprocess.run(cmd, check=True)
    print(f"✓ PDF created successfully: {pdf_file.name}")

def main():
    parser = argparse.ArgumentParser(description="Compile Turkey Namedni markdown to rich HTML/PDF magazine")
    parser.add_argument("--year", required=True, help="Year to process (e.g. 1980)")
    args = parser.parse_args()
    
    print(f"Parsing {args.year}.md ...")
    data = parse_markdown(args.year)
    
    print("Generating HTML ...")
    html_content = generate_html(data)
    
    html_file = SCRIPT_DIR / f"{args.year}.html"
    html_file.write_text(html_content, encoding="utf-8")
    print(f"✓ HTML created: {html_file.name}")

if __name__ == "__main__":
    main()
