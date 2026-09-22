#!/usr/bin/env python3
import json
import re
import os
from pathlib import Path

BASE_DIR = Path("/Users/mac2021/Documents/Claude/Projects/namedni")
DATA_PATH = BASE_DIR / "1980_data.json"

SECTIONS_CONFIG = {
    "12 сентября": {
        "id": "sep12",
        "category": "Главное событие года",
        "theme": "s-coup",
        "img": "img/1980/1980_12-eylul_03.jpg",
        "img_orient": "landscape",
        "caption": "Пресс-конференция военного Совета национальной безопасности. Генералы за столом с микрофонами международных агентств. Анкара, сентябрь 1980.",
        "extra_imgs": [
            {"path": "img/1980/1980_12-eylul_01.jpg", "caption": "Солдат останавливает машины у светофора. Перекрёсток Кызылай — Чанкая, Анкара. 12 сентября 1980."},
            {"path": "img/1980/1980_12-eylul_02.jpg", "caption": "Танк M48 на центральном проспекте Анкары. Солдаты в белых касках патрулируют улицу. 12 сентября 1980."}
        ],
        "date": "12 сентября 1980",
        "idx": "01",
    },
    "Тариш": {
        "id": "tarish",
        "category": "Политика",
        "theme": "s-tarish",
        "img": None,
        "img_orient": "text-only",
        "date": "14 февраля 1980",
        "idx": "02",
    },
    "Фатса": {
        "id": "fatsa",
        "category": "Политика",
        "theme": "s-fatsa",
        "img": "img/1980/1980_fatsa_01.jpg",
        "img_orient": "landscape",
        "caption": "Военная операция в Фатсе. Офицеры на совещании, июль 1980 года.",
        "date": "Июль 1980",
        "idx": "03",
    },
    "24 января": {
        "id": "yan24",
        "category": "Экономика",
        "theme": "s-economy",
        "img": "img/1980/1980_24-ocak_01.jpg",
        "img_orient": "landscape",
        "caption": "Передовицы турецких газет января 1980-го: «1 доллар = 70 лир», «Цены свободны — повышения пришли», «Жизнь стала тяжелее». Хурриет, Миллиет, Халк Газетеси.",
        "date": "24 января 1980",
        "idx": "04",
    },
    "Жертвы": {
        "id": "victims",
        "category": "Общество · Жертвы",
        "theme": "s-victims",
        "img": "img/1980/1980_erdal-eren_01.jpg",
        "img_orient": "landscape",
        "caption": "Эрдал Эрен — семнадцатилетний школьник — на слушании военного трибунала. Приговорён к смертной казни и повешен 13 декабря 1980 года. Анкара, 1980.",
        "date": "Декабрь 1980",
        "idx": "05",
    },
    "Independenta": {
        "id": "independenta",
        "category": "Общество · Катастрофа",
        "theme": "s-independenta",
        "img": "img/1980/1980_independenta_01.png",
        "img_orient": "square",
        "caption": "Катастрофа румынского супертанкера «Индепенденца» в Босфоре. Огонь полыхал на воде больше месяца. Ноябрь 1979 года.",
        "date": "Ноябрь 1979",
        "idx": "06",
    },
    "Кыраатхане: мужской мир": {
        "id": "kiraathane",
        "category": "Повседневная жизнь",
        "theme": "s-kiraathane",
        "img": "img/1980/1980_kiraathane_01.jpg",
        "img_orient": "landscape",
        "caption": "Кыраатхане «Merkez Kıraathanesi» с посетителями на улице. Турция, 1980-е.",
        "extra_imgs": [
            {"path": "img/1980/1980_kiraathane_02.jpg", "caption": "Внутри кыраатхане: мужчины за столиками играют в нарды и окей, беседуют за чаем."}
        ],
        "date": "1980-е",
        "idx": "07",
    },
    "Даллас": {
        "id": "dallas",
        "category": "Телевидение",
        "theme": "s-dallas",
        "img": "img/1980/1980_dallas_01.jpg",
        "img_orient": "landscape",
        "caption": "Актерский состав сериала «Даллас»: Юинги у бассейна в Техасе. Символ эпохи TRT.",
        "date": "6 ноября 1980",
        "idx": "08",
    },
    "Бюлент Эрсой": {
        "id": "bulent",
        "category": "Музыка · Общество",
        "theme": "s-bulent",
        "img": "img/1980/1980_bulent-ersoy_03.jpg",
        "img_orient": "portrait",
        "caption": "Афиша фильма «Şöhretin Sonu» («Конец славы») с Бюлентом Эрсоем, 1980 год.",
        "extra_imgs": [
            {"path": "img/1980/1980_bulent-ersoy_01.jpg", "caption": "Бюлент Эрсой под стражей в окружении жандармерии, Измир, сентябрь 1980."},
            {"path": "img/1980/1980_bulent-ersoy_02.jpg", "caption": "Обложка раннего винилового альбома Бюлента Эрсоя."}
        ],
        "date": "1980–1988",
        "idx": "09",
    },
    "Петрол": {
        "id": "petrol",
        "category": "Музыка · Евровидение",
        "theme": "s-petrol",
        "img": "img/1980/1980_petrol-evrovid_01.png",
        "img_orient": "portrait",
        "caption": "Аджда Пеккан на обложке журнала после отбора с песней «Petrol». Апрель 1980 года.",
        "extra_imgs": [
            {"path": "img/1980/1980_petrol-krizi_01.jpg", "caption": "Аджда Пеккан позирует на бензоколонке с заправочным шлангом в руках — промо-акция к выпуску сингла «Petrol» на фоне дефицита топлива."}
        ],
        "date": "Апрель 1980",
        "idx": "10",
    },
    "Таверна": {
        "id": "taverna",
        "category": "Музыка · Жанр",
        "theme": "s-taverna",
        "img": "img/1980/1980_taverna_01.jpg",
        "img_orient": "landscape",
        "caption": "Вечер в турецкой таверне: мезе, ракы, живая музыка на синтезаторе. Начало 1980-х.",
        "date": "Конец 1970-х",
        "idx": "11",
    },
    "Хисселли Харикалар Кумпаньясы": {
        "id": "hisseli",
        "category": "Культура · Театр",
        "theme": "s-hisseli",
        "img": "img/1980/1980_hisseli_01.png",
        "img_orient": "square",
        "caption": "Афиша мюзикла «Hisseli Harikalar Kumpanyası» Халдуна Дормена. Премьера 3 марта 1980 года.",
        "date": "3 марта 1980",
        "idx": "12",
    },
    "Шахов тоже убивают": {
        "id": "sahlari",
        "category": "Культура · Театр",
        "theme": "s-sahlari",
        "img": "img/1980/1980_sahlari_01.jpg",
        "img_orient": "landscape",
        "caption": "Труппа театра «Ортаойунджулар» на афише спектакля «Шахов тоже убивают» (Şahları da Öldürürler). Март 1980.",
        "date": "Март 1980",
        "idx": "13",
    },
    "Джон Леннон": {
        "id": "lennon",
        "category": "Культура · Мир",
        "theme": "s-lennon",
        "img": "img/1980/1980_john-lennon_01.png",
        "img_orient": "portrait",
        "caption": "Джон Леннон и Йоко Оно на обложке пластинки «Double Fantasy». Нью-Йорк, 1980.",
        "date": "8 декабря 1980",
        "idx": "14",
    },
    "Йешильчам: последние годы народного кино": {
        "id": "yesilcam",
        "category": "Кино",
        "theme": "s-yesilcam",
        "img": "img/1980/1980_yesil-cam_01.jpg",
        "img_orient": "landscape",
        "caption": "Актёры и съёмочная группа турецкого кино эпохи Йешильчама. Народные звёзды ТБММ и съезды.",
        "date": "1980 год",
        "idx": "15",
    },
    "Футбол": {
        "id": "futbol",
        "category": "Спорт · Футбол",
        "theme": "s-sport",
        "img": "img/1980/1980_futbol-trabzonspor_01.jpg",
        "img_orient": "landscape",
        "caption": "«Трабзонспор» — чемпион Турции сезона 1979/80. Командное фото клуба.",
        "date": "Сезон 1979/80",
        "idx": "16",
    }
}

def get_image_orientation(img_path):
    if not img_path:
        return "text-only"
    full_path = BASE_DIR / img_path
    if not full_path.exists():
        return "landscape"
    try:
        from PIL import Image
        with Image.open(full_path) as img:
            w, h = img.size
            if abs(w - h) / max(w, h) < 0.05:
                return "square"
            elif w > h:
                return "landscape"
            else:
                return "portrait"
    except Exception as e:
        print(f"Error reading image {img_path}: {e}")
        return "landscape"

def clean_text(p):
    # Remove markdown image lines
    if p.startswith("![") or "img/1980" in p or p.startswith("{pair}!") or p.startswith("{right}!"):
        return None
    # Remove caption lines (often start with *)
    if p.startswith("*") and p.endswith("*") and "img/1980" in p:
        return None
    # Skip reference notes like *(см. ...)* as they are handled separately
    if p.startswith("*(") and p.endswith(")*"):
        return None
    return p

def parse_section(title, paragraphs):
    cleaned = []
    lede = ""
    ref_note = ""
    for p in paragraphs:
        p_clean = clean_text(p)
        if not p_clean:
            continue
        
        # Lede paragraph check (starts with ** and ends with **)
        if p_clean.startswith("**") and p_clean.endswith("**"):
            # strip **
            lede = p_clean[2:-2]
            continue
        
        # Check if reference note
        if p_clean.startswith("*(") and p_clean.endswith(")*"):
            ref_note = p_clean[2:-2]
            continue
            
        cleaned.append(p_clean)
        
    return lede, cleaned, ref_note

# Load parsed MD data
with open(DATA_PATH) as f:
    raw_data = json.load(f)

# Build matching mapping
md_dict = {sec["title"]: sec["paragraphs"] for sec in raw_data}

# Generate Spreads
spreads_html = []
toc_items = []
current_side_by_side_count = 0

# Track active navigation indicators
nav_links = []

# Process MD items in order of SECTIONS_CONFIG
sorted_titles = sorted(SECTIONS_CONFIG.keys(), key=lambda t: SECTIONS_CONFIG[t]["idx"])

# To match standard order, let's categorize them by groups
groups = [
    {"num": "01", "name": "Главное событие года", "keys": ["12 сентября"]},
    {"num": "02", "name": "Политика", "keys": ["Тариш", "Фатса"]},
    {"num": "03", "name": "Экономика", "keys": ["24 января"]},
    {"num": "04", "name": "Общество", "keys": ["Жертвы", "Independenta"]},
    {"num": "05", "name": "Повседневная жизнь", "keys": ["Кыраатхане: мужской мир"]},
    {"num": "06", "name": "Телевидение", "keys": ["Даллас"]},
    {"num": "07", "name": "Музыка", "keys": ["Бюлент Эрсой", "Петрол", "Таверна"]},
    {"num": "08", "name": "Культура", "keys": ["Хисселли Харикалар Кумпаньясы", "Шахов тоже убивают", "Джон Леннон"]},
    {"num": "09", "name": "Кино", "keys": ["Йешильчам: последние годы народного кино"]},
    {"num": "10", "name": "Спорт", "keys": ["Футбол"]}
]

for g in groups:
    # Add group banner in TOC
    first_key = g["keys"][0]
    first_cfg = SECTIONS_CONFIG.get(first_key)
    if first_cfg:
        toc_items.append(f'<a href="#{first_cfg["id"]}">{g["name"]}</a>')

# Generate the actual spread HTML
for group_idx, g in enumerate(groups):
    # Output category header banner
    banner_id = SECTIONS_CONFIG[g["keys"][0]]["id"]
    spreads_html.append(f'''
<!-- ══════════════════════════════════════════
     {g["num"]} · {g["name"].upper()}
══════════════════════════════════════════ -->
<div class="group-banner" id="{banner_id}">
  <span class="group-banner-num">{g["num"]}</span>
  <span class="group-banner-title">{g["name"]}</span>
  <span class="group-banner-count">{len(g["keys"])} {"феномена" if len(g["keys"]) == 2 else "феномен"}</span>
</div>
''')

    for key in g["keys"]:
        cfg = SECTIONS_CONFIG[key]
        md_paragraphs = md_dict.get(key, [])
        if not md_paragraphs:
            # Fallback if key is slightly different (e.g. Yesilcam / Cinema name match)
            for md_title in md_dict.keys():
                if key.split(":")[0].lower() in md_title.lower() or md_title.lower().split(":")[0] in key.lower():
                    md_paragraphs = md_dict[md_title]
                    break
        
        lede, body_paragraphs, ref_note = parse_section(key, md_paragraphs)
        
        # Custom classes & config
        s_id = cfg["id"]
        theme = cfg["theme"]
        img_path = cfg["img"]
        orient = get_image_orientation(img_path)
        caption = cfg.get("caption", "")
        idx = cfg["idx"]
        date_str = cfg["date"]
        
        # Format paragraphs
        body_html = "\n".join(f"<p>{p}</p>" for p in body_paragraphs)
        if ref_note:
            body_html += f'\n<p class="ref-note">*(см. {ref_note})*</p>'
            
        # Orientation-specific HTML structure
        if orient == "text-only":
            # Typography-focused stacked layout without image
            spread_class = "spread-text-only"
            photo_block = ""
            body_container = f'''
  <div class="spread-body">
    <div class="spread-tag">{cfg["category"]} · {date_str}</div>
    <h2 class="spread-title">{key}</h2>
    <p class="spread-lede">{lede}</p>
    <div class="spread-text">
      {body_html}
    </div>
  </div>
'''
        elif orient in ["portrait", "square"]:
            # Side-by-side layout (photo left or right)
            # Alternate left/right based on count
            side_class = "photo-right" if current_side_by_side_count % 2 == 1 else "photo-left"
            current_side_by_side_count += 1
            
            spread_class = f"spread spread-side-by-side {side_class}"
            
            # Additional photos if any
            extra_photos_html = ""
            if cfg.get("extra_imgs"):
                extra_photos_html = '<div class="extra-photos-grid">'
                for ex in cfg["extra_imgs"]:
                    extra_photos_html += f'''
                    <figure class="extra-photo-item">
                      <img src="{ex["path"]}" alt="{ex["caption"]}" onclick="openLightbox(this.src, this.alt)">
                      <figcaption class="img-cap-small">{ex["caption"]}</figcaption>
                    </figure>
                    '''
                extra_photos_html += '</div>'
                
            photo_block = f'''
  <div class="spread-photo">
    <span class="spread-date">{date_str}</span>
    <img src="{img_path}" alt="{caption}" onclick="openLightbox(this.src, this.alt)">
    <div class="spread-num">{idx}</div>
    <figcaption class="img-cap-overlay">{caption}</figcaption>
  </div>
'''
            body_container = f'''
  <div class="spread-body">
    <div class="spread-tag">{cfg["category"]}</div>
    <h2 class="spread-title">{key}</h2>
    <p class="spread-lede">{lede}</p>
    <div class="spread-text">
      {body_html}
      {extra_photos_html}
    </div>
  </div>
'''
        else:
            # Landscape layout -> STACKED
            spread_class = "spread spread-stacked"
            
            # Additional images (e.g. for September 12 tank/soldiers)
            extra_photos_html = ""
            if cfg.get("extra_imgs"):
                extra_photos_html = '<div class="img-pair">'
                for ex in cfg["extra_imgs"]:
                    extra_photos_html += f'''
                    <figure>
                      <img src="{ex["path"]}" alt="{ex["caption"]}" onclick="openLightbox(this.src, this.alt)">
                      <figcaption class="img-cap">{ex["caption"]}</figcaption>
                    </figure>
                    '''
                extra_photos_html += '</div>'
                
            photo_block = f'''
  <div class="spread-photo">
    <span class="spread-date">{date_str}</span>
    <img src="{img_path}" alt="{caption}" onclick="openLightbox(this.src, this.alt)">
    <div class="spread-num">{idx}</div>
    <figcaption class="img-cap-overlay">{caption}</figcaption>
  </div>
'''
            body_container = f'''
  <div class="spread-body">
    <div class="spread-tag">{cfg["category"]}</div>
    <h2 class="spread-title">{key}</h2>
    <p class="spread-lede">{lede}</p>
    <div class="spread-text">
      {body_html}
    </div>
    {extra_photos_html}
  </div>
'''

        spreads_html.append(f'''
<article class="spread {theme} {spread_class}" id="{s_id}" data-idx="{idx}">
  {photo_block}
  {body_container}
</article>
<div class="spread-sep"></div>
''')

    # Add 3D placeholder parallelepipeds for future categories
    if g["name"] == "Телевидение":
        # Insert Technologies placeholder after Television
        spreads_html.append('''
<!-- ══════════════════════════════════════════
     3D PLACEHOLDER · ТЕХНОЛОГИИ
══════════════════════════════════════════ -->
<div class="group-banner" id="technologies">
  <span class="group-banner-num">06B</span>
  <span class="group-banner-title">Технологии</span>
  <span class="group-banner-count">в работе</span>
</div>
<div class="spread spread-empty-3d">
  <div class="wireframe-container">
    <div class="box-3d">
      <div class="box-face face-front"></div>
      <div class="box-face face-back"></div>
      <div class="box-face face-left"></div>
      <div class="box-face face-right"></div>
      <div class="box-face face-top"></div>
      <div class="box-face face-bottom"></div>
    </div>
    <div class="placeholder-text">Требуется феномен · Технологии</div>
  </div>
</div>
<div class="spread-sep"></div>
''')
        toc_items.insert(6, '<a href="#technologies" class="placeholder-nav-link">Технологии (3D)</a>')

    elif g["name"] == "Кино":
        # Insert Science placeholder after Cinema
        spreads_html.append('''
<!-- ══════════════════════════════════════════
     3D PLACEHOLDER · НАУКА
══════════════════════════════════════════ -->
<div class="group-banner" id="science">
  <span class="group-banner-num">09B</span>
  <span class="group-banner-title">Наука</span>
  <span class="group-banner-count">в работе</span>
</div>
<div class="spread spread-empty-3d">
  <div class="wireframe-container">
    <div class="box-3d">
      <div class="box-face face-front"></div>
      <div class="box-face face-back"></div>
      <div class="box-face face-left"></div>
      <div class="box-face face-right"></div>
      <div class="box-face face-top"></div>
      <div class="box-face face-bottom"></div>
    </div>
    <div class="placeholder-text">Требуется феномен · Наука</div>
  </div>
</div>
<div class="spread-sep"></div>
''')
        toc_items.insert(10, '<a href="#science" class="placeholder-nav-link">Наука (3D)</a>')


# Construct full page
html_template = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1980 — Намедни по-турецки (Gemini Interactive Edition)</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=PT+Sans:wght@400;700;900&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@400;700;900&family=Special+Elite&family=Sacramento&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}

:root {{
  --header-h: 112px;
  --cream: #f4eadf;
  --ink: #1d1a17;
  --panel-bg: #2a1c0c;
  --scroll-pct: 0;
  --scroll-angle: 125deg;
}}

html {{
  scroll-behavior: smooth;
}}

body {{
  font-family: 'PT Serif', Georgia, serif;
  color: var(--ink);
  overflow-x: hidden;
  background: #2a1c0c;
}}

/* ── ПЕРЕЛИВАЮЩИЙСЯ ФОН — тёплый, живой ── */
.bg-canvas {{
  position: fixed;
  inset: 0;
  z-index: 0;
  background: linear-gradient(
    var(--scroll-angle, 125deg),
    #e8d5b0 0%,
    #d4b896 calc(var(--scroll-pct, 0) * 15% + 5%),
    #c8a87a calc(var(--scroll-pct, 0) * 30% + 15%),
    #d9c4a0 calc(var(--scroll-pct, 0) * 45% + 25%),
    #e2d0b5 calc(var(--scroll-pct, 0) * 60% + 35%),
    #c9b890 calc(var(--scroll-pct, 0) * 75% + 45%),
    #ddc8a8 100%
  );
  background-size: 200% 200%;
  pointer-events: none;
}}
.bg-canvas::after {{
  content: '';
  position: absolute;
  inset: 0;
  opacity: .05;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px;
}}

/* ═══════════════════════════════════════════
   ШАПКА — залипает при скролле
═══════════════════════════════════════════ */
.site-header {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(18, 8, 2, .96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(160,80,20,.35);
  box-shadow: 0 2px 24px rgba(0,0,0,.5);
}}
.header-inner {{
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 20px;
  padding: 10px 40px;
}}
.year-mark {{
  font-family: 'Cinzel', serif;
  font-size: 52px;
  font-weight: 900;
  color: #fff;
  line-height: 1;
  letter-spacing: -.03em;
}}
.header-brand {{
  display: flex;
  flex-direction: column;
  gap: 2px;
}}
.site-name {{
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 14px;
  color: rgba(255,220,150,.85);
}}
.site-sub {{
  font-family: 'PT Sans', sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: .16em;
  text-transform: uppercase;
  color: rgba(255,255,255,.35);
}}
.spread-counter {{
  font-family: 'Cinzel', serif;
  font-size: 13px;
  color: rgba(255,255,255,.25);
  letter-spacing: .08em;
  white-space: nowrap;
}}
.spread-counter span {{ color: rgba(255,200,80,.85); }}

.header-nav {{
  grid-column: 1 / -1;
  display: flex;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
  border-top: 1px solid rgba(255,255,255,.06);
  padding: 0 40px;
  margin: 0 -40px;
}}
.header-nav::-webkit-scrollbar {{ display: none; }}
.header-nav a {{
  font-family: 'PT Sans', sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: rgba(255,255,255,.35);
  padding: 8px 13px 7px;
  white-space: nowrap;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all .18s;
}}
.header-nav a:hover,
.header-nav a.active {{ color: #fff; border-color: #c04020; }}

/* ═══════════════════════════════════════════
   РАЗВОРОТЫ — АДАПТИВНАЯ ВЕРСТКА ПО ФОРМАТУ ФОТО
═══════════════════════════════════════════ */
.spread {{
  position: relative;
  z-index: 5;
  background: var(--panel-bg, #2a1c0c);
  transition: background 0.3s ease;
  overflow: hidden;
  border-bottom: 1px solid rgba(0,0,0,0.2);
}}

/* ── 1. Горизонтальная картинка (Landscape) -> Stacked Layout ── */
.spread-stacked {{
  display: flex;
  flex-direction: column;
  height: auto;
  min-height: auto;
}}
.spread-stacked .spread-photo {{
  position: relative;
  width: 100%;
  height: 50vh;
  min-height: 350px;
  max-height: 550px;
  overflow: hidden;
}}
.spread-stacked .spread-photo img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  cursor: zoom-in;
  filter: sepia(10%) contrast(1.05) brightness(0.85);
  transition: transform 6s ease, filter 0.4s ease;
}}
.spread-stacked:hover .spread-photo img {{
  transform: scale(1.03);
  filter: sepia(3%) contrast(1.1) brightness(0.92);
}}
.spread-stacked .spread-body {{
  padding: 50px 80px 60px 80px;
  background: linear-gradient(180deg, var(--panel-bg) 0%, rgba(0,0,0,0.1) 100%);
}}
.spread-stacked .spread-title {{
  font-family: 'Playfair Display', serif;
  font-size: 38px;
  font-weight: 900;
  line-height: 1.15;
  margin-bottom: 20px;
  max-width: 900px;
}}
.spread-stacked .spread-lede {{
  font-size: 17px;
  line-height: 1.8;
  max-width: 900px;
  margin-bottom: 30px;
  border-left: 4px solid var(--text-accent, #c0392b);
  padding-left: 24px;
}}
.spread-stacked .spread-text {{
  column-count: 2;
  column-gap: 50px;
  text-align: justify;
  font-size: 14.5px;
  line-height: 1.85;
}}
.spread-stacked .spread-text p {{
  margin-bottom: 14px;
}}

/* ── 2. Вертикальная или Квадратная (Portrait/Square) -> Side-by-Side ── */
.spread-side-by-side {{
  height: calc(100vh - var(--header-h));
  min-height: 600px;
  display: grid;
  grid-template-columns: 45% 55%;
}}
.spread-side-by-side.photo-right {{
  grid-template-columns: 55% 45%;
}}
.spread-side-by-side.photo-right .spread-photo {{
  order: 2;
}}
.spread-side-by-side.photo-right .spread-body {{
  order: 1;
  padding: 44px 44px 44px 52px;
}}
.spread-side-by-side .spread-photo {{
  position: relative;
  height: 100%;
  overflow: hidden;
}}
.spread-side-by-side .spread-photo img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  cursor: zoom-in;
  filter: sepia(10%) contrast(1.05) brightness(0.85);
  transition: transform 6s ease, filter 0.4s ease;
}}
.spread-side-by-side:hover .spread-photo img {{
  transform: scale(1.03);
  filter: sepia(3%) contrast(1.1) brightness(0.92);
}}
.spread-side-by-side .spread-body {{
  height: 100%;
  overflow-y: auto;
  padding: 44px 52px 44px 44px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,.1) transparent;
}}
.spread-side-by-side .spread-body::-webkit-scrollbar {{ width: 3px; }}
.spread-side-by-side .spread-body::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,.15); border-radius: 2px; }}
.spread-side-by-side .spread-title {{
  font-family: 'Playfair Display', serif;
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
}}
.spread-side-by-side .spread-lede {{
  font-size: 15px;
  line-height: 1.75;
  margin-bottom: 16px;
  border-left: 3px solid var(--text-accent, #c0392b);
  padding-left: 18px;
}}
.spread-side-by-side .spread-text {{
  font-size: 13.5px;
  line-height: 1.85;
  text-align: justify;
}}
.spread-side-by-side .spread-text p {{
  margin-bottom: 12px;
}}

/* ── 3. Текстовый разворот (без фото) ── */
.spread-text-only {{
  display: flex !important;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - var(--header-h));
  padding: 80px 24px;
}}
.spread-text-only .spread-body {{
  padding: 60px 60px;
  max-width: 760px;
  width: 100%;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}}
.spread-text-only .spread-title {{
  text-align: center;
  font-family: 'Special Elite', monospace;
  font-size: 38px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 20px;
  color: #fff;
}}
.spread-text-only .spread-tag {{
  text-align: center;
  font-family: 'Special Elite', monospace;
  font-size: 11px;
  letter-spacing: 0.15em;
  margin-bottom: 15px;
  color: var(--text-accent, #ff3333);
}}
.spread-text-only .spread-lede {{
  text-align: center;
  font-family: 'Special Elite', monospace;
  font-size: 16px;
  line-height: 1.7;
  color: #fce4e4;
  border-left: none;
  padding-left: 0;
  margin-bottom: 30px;
}}
.spread-text-only .spread-text {{
  column-count: 1;
  text-align: justify;
  font-family: 'Special Elite', monospace;
  font-size: 14.5px;
  line-height: 1.8;
  color: #d6a2a8;
}}


/* ── Элементы внутри разворотов ── */
.spread-date {{
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0,0,0,.7);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  color: #fff;
  font-family: 'PT Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .16em;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 2px;
  z-index: 10;
}}
.spread-num {{
  position: absolute;
  bottom: 10px;
  left: 20px;
  font-family: 'Cinzel', serif;
  font-size: 90px;
  font-weight: 900;
  line-height: 1;
  color: rgba(255,255,255,.06);
  pointer-events: none;
  user-select: none;
  z-index: 10;
}}
.spread-tag {{
  font-family: 'PT Sans', sans-serif;
  font-size: 9px;
  font-weight: 900;
  letter-spacing: .22em;
  text-transform: uppercase;
  margin-bottom: 12px;
}}
.img-cap-overlay {{
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 70%, transparent 100%);
  padding: 30px 20px 15px;
  color: rgba(255,255,255,0.7);
  font-size: 11px;
  font-style: italic;
  font-family: 'PT Sans', sans-serif;
  line-height: 1.5;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.4s ease;
  pointer-events: none;
  z-index: 9;
}}
.spread:hover .img-cap-overlay {{
  opacity: 1;
  transform: translateY(0);
}}

/* Дополнительные фото-сетки */
.img-pair {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 30px;
}}
.img-pair figure {{
  margin: 0;
}}
.img-pair figure img {{
  width: 100%;
  height: auto;
  border: 1px solid rgba(255,255,255,0.1);
  cursor: zoom-in;
}}
.img-cap {{
  font-family: 'PT Sans', sans-serif;
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  font-style: italic;
  margin-top: 6px;
  line-height: 1.4;
}}
.extra-photos-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-top: 20px;
}}
.extra-photo-item img {{
  width: 100%;
  height: 120px;
  object-fit: cover;
  border: 1px solid rgba(255,255,255,0.1);
  cursor: zoom-in;
}}
.img-cap-small {{
  font-size: 10px;
  color: rgba(255,255,255,0.4);
  font-style: italic;
  margin-top: 4px;
}}

/* Полоска-разделитель */
.spread-sep {{
  position: relative;
  z-index: 5;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1) 20%, rgba(255,255,255,0.1) 80%, transparent);
}}

/* Заголовки категорий */
.group-banner {{
  position: relative;
  z-index: 5;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 48px;
  background: rgba(18, 8, 2, .75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-top: 1px solid rgba(255,255,255,.06);
  border-bottom: 1px solid rgba(255,255,255,.04);
  scroll-margin-top: var(--header-h);
}}
.group-banner-num {{
  font-family: 'Cinzel', serif;
  font-size: 11px;
  font-weight: 700;
  color: rgba(255,200,80,.45);
}}
.group-banner-title {{
  font-family: 'Cinzel', serif;
  font-size: 18px;
  font-weight: 700;
  color: rgba(255,255,255,.7);
  letter-spacing: 1px;
}}
.group-banner-count {{
  margin-left: auto;
  font-family: 'PT Sans', sans-serif;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: rgba(255,255,255,.25);
}}

/* ═══════════════════════════════════════════
   3D PLACEHOLDER STYLING (Empty categories)
═══════════════════════════════════════════ */
.spread-empty-3d {{
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(18, 8, 2, 0.4);
}}
.wireframe-container {{
  perspective: 600px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}}
.box-3d {{
  width: 120px;
  height: 80px;
  position: relative;
  transform-style: preserve-3d;
  transform: rotateX(-20deg) rotateY(30deg);
  transition: transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}
.wireframe-container:hover .box-3d {{
  transform: rotateX(20deg) rotateY(210deg) scale(1.1);
}}
.box-face {{
  position: absolute;
  border: 1.5px dashed rgba(255,200,80, 0.4);
  background: rgba(255, 200, 80, 0.03);
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
}}
.face-front  {{ width: 120px; height: 80px; transform: translateZ(30px); }}
.face-back   {{ width: 120px; height: 80px; transform: rotateY(180deg) translateZ(30px); }}
.face-left   {{ width: 60px;  height: 80px; transform: rotateY(-90deg) translateZ(30px); left: 30px; }}
.face-right  {{ width: 60px;  height: 80px; transform: rotateY(90deg) translateZ(30px); left: 30px; }}
.face-top    {{ width: 120px; height: 60px; transform: rotateX(90deg) translateZ(30px); top: 10px; }}
.face-bottom {{ width: 120px; height: 60px; transform: rotateX(-90deg) translateZ(30px); top: 10px; }}

.placeholder-text {{
  margin-top: 20px;
  font-family: 'Cinzel', serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: rgba(255,200,80, 0.6);
  text-transform: uppercase;
}}

/* ═══════════════════════════════════════════
   ЦВЕТОВЫЕ СХЕМЫ С ИНДИВИДУАЛЬНЫМИ СТИЛЯМИ
═══════════════════════════════════════════ */

/* 1. Военный переворот (12 сентября) */
.s-coup {{
  --panel-bg: #1e1d1c;
  --text-accent: #c0392b;
  border: 2px solid #2d2b29;
}}
.s-coup .spread-body {{
  background: linear-gradient(135deg, #161514 0%, #22201f 100%);
  border-left: 2px solid #2d2b29;
}}
.s-coup .spread-tag {{ color: #e74c3c; font-family: 'PT Sans', sans-serif; }}
.s-coup .spread-title {{ color: #e1dcd6; font-family: 'Cinzel', serif; font-weight: 900; letter-spacing: -1px; }}
.s-coup .spread-lede {{ color: #b8b1a8; font-family: 'Special Elite', monospace; border-color: #e74c3c; }}
.s-coup .spread-text {{ color: #a39b90; }}
.s-coup .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #161514 100%);
}}

/* 2. Тариш (Забастовка) */
.s-tarish {{
  --panel-bg: #2e1216;
  --text-accent: #ff3333;
}}
.s-tarish .spread-body {{
  background: linear-gradient(135deg, #1f0b0e 0%, #3a161b 100%);
  font-family: 'Special Elite', monospace;
}}
.s-tarish .spread-tag {{ color: #ff5555; }}
.s-tarish .spread-title {{ color: #ffd6d6; font-family: 'Special Elite', monospace; }}
.s-tarish .spread-lede {{ color: #e5b3b3; border-color: #ff3333; }}
.s-tarish .spread-text {{ color: #d6a2a8; }}

/* 3. Фатса (Коммуна) */
.s-fatsa {{
  --panel-bg: #1a251b;
  --text-accent: #e74c3c;
}}
.s-fatsa .spread-body {{
  background: linear-gradient(135deg, #111a12 0%, #253327 100%);
}}
.s-fatsa .spread-tag {{ color: #2ecc71; }}
.s-fatsa .spread-title {{ color: #e3efeb; font-family: 'Playfair Display', serif; }}
.s-fatsa .spread-lede {{ color: #b5c7b9; border-color: #2ecc71; }}
.s-fatsa .spread-text {{ color: #9bb0a0; }}
.s-fatsa .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #111a12 100%);
}}

/* 4. 24 января (Экономика) */
.s-economy {{
  --panel-bg: #2b2416;
  --text-accent: #d4a824;
}}
.s-economy .spread-body {{
  background: linear-gradient(135deg, #1a150c 0%, #362e1c 100%);
  border-left: 1px double rgba(255,255,255,0.08);
}}
.s-economy .spread-tag {{ color: #f1c40f; }}
.s-economy .spread-title {{ color: #fdf5e2; font-family: 'Playfair Display', serif; letter-spacing: -0.5px; }}
.s-economy .spread-lede {{ color: #e5d9bd; border-color: #f1c40f; }}
.s-economy .spread-text {{ color: #c8bd9f; }}
.s-economy .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #1a150c 100%);
}}

/* 5. Жертвы */
.s-victims {{
  --panel-bg: #0d0c0c;
  --text-accent: #7f7f7f;
}}
.s-victims .spread-body {{
  background: #0d0c0c;
  border-left: 3px double #333;
}}
.s-victims .spread-tag {{ color: #888; }}
.s-victims .spread-title {{ color: #eee; font-family: 'Cinzel', serif; font-weight: 700; }}
.s-victims .spread-lede {{ color: #ccc; border-color: #888; font-family: 'Special Elite', monospace; }}
.s-victims .spread-text {{ color: #aaa; }}
.s-victims .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #0d0c0c 100%);
}}

/* 6. Independenta (Катастрофа) */
.s-independenta {{
  --panel-bg: #1a100a;
  --text-accent: #d35400;
}}
.s-independenta .spread-body {{
  background: linear-gradient(135deg, #100a06 0%, #24150c 100%);
  box-shadow: inset 0 0 100px rgba(211, 84, 0, 0.05);
}}
.s-independenta .spread-tag {{ color: #e67e22; }}
.s-independenta .spread-title {{ color: #faede3; text-shadow: 0 0 15px rgba(211,84,0,0.1); }}
.s-independenta .spread-lede {{ color: #eccab3; border-color: #d35400; }}
.s-independenta .spread-text {{ color: #cfb3a0; }}
.s-independenta .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #100a06 100%);
}}

/* 7. Кыраатхане (Повседневная) */
.s-kiraathane {{
  --panel-bg: #24140b;
  --text-accent: #e67e22;
}}
.s-kiraathane .spread-body {{
  background: linear-gradient(135deg, #160c07 0%, #2f1b0f 100%);
}}
.s-kiraathane .spread-tag {{ color: #d35400; }}
.s-kiraathane .spread-title {{ color: #faede6; }}
.s-kiraathane .spread-lede {{ color: #eac8b4; border-color: #d35400; }}
.s-kiraathane .spread-text {{ color: #cfb2a2; }}
.s-kiraathane .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #160c07 100%);
}}

/* 8. Даллас (Телевидение) */
.s-dallas {{
  --panel-bg: #091024;
  --text-accent: #3498db;
}}
.s-dallas .spread-body {{
  background: linear-gradient(135deg, #050b18 0%, #101c3d 100%);
  position: relative;
}}
/* Эффект ретро ЭЛТ телевизора с линиями */
.s-dallas .spread-body::before {{
  content: " ";
  display: block;
  position: absolute;
  top: 0; left: 0; bottom: 0; right: 0;
  background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
  z-index: 2;
  background-size: 100% 4px, 6px 100%;
  pointer-events: none;
}}
.s-dallas .spread-tag {{ color: #52a8ff; }}
.s-dallas .spread-title {{ color: #e6f1ff; font-family: 'Cinzel', serif; }}
.s-dallas .spread-lede {{ color: #b8d2f0; border-color: #3498db; }}
.s-dallas .spread-text {{ color: #9bb2cd; }}
.s-dallas .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #050b18 100%);
}}

/* 9. Бюлент Эрсой (Глэм-стекломорфизм) */
.s-bulent {{
  --panel-bg: #27061d;
  --text-accent: #e0115f;
}}
.s-bulent .spread-body {{
  background: linear-gradient(135deg, #180312 0%, #360929 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: inset 0 0 80px rgba(224, 17, 95, 0.08);
}}
.s-bulent .spread-tag {{ color: #ff66a3; }}
.s-bulent .spread-title {{ color: #ffe6f2; font-family: 'Sacramento', cursive; font-size: 52px; font-weight: 400; text-shadow: 0 0 10px rgba(224,17,95,0.2); }}
.s-bulent .spread-lede {{ color: #f5bccc; border-color: #e0115f; font-family: 'Playfair Display', serif; font-style: italic; }}
.s-bulent .spread-text {{ color: #d69db5; }}
.s-bulent .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #180312 100%);
}}

/* 10. Петрол (Поп-винил) */
.s-petrol {{
  --panel-bg: #12151c;
  --text-accent: #e74c3c;
}}
.s-petrol .spread-body {{
  background: linear-gradient(135deg, #0b0d12 0%, #1f2533 100%);
}}
.s-petrol .spread-tag {{ color: #ff6b6b; }}
.s-petrol .spread-title {{ color: #e9f0fa; font-family: 'PT Sans', sans-serif; font-weight: 900; letter-spacing: -0.5px; }}
.s-petrol .spread-lede {{ color: #b7c7dc; border-color: #ff6b6b; }}
.s-petrol .spread-text {{ color: #98a9c0; }}
.s-petrol .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #0b0d12 100%);
}}

/* 11. Таверна */
.s-taverna {{
  --panel-bg: #291206;
  --text-accent: #d35400;
}}
.s-taverna .spread-body {{
  background: linear-gradient(135deg, #1b0a03 0%, #381909 100%);
}}
.s-taverna .spread-tag {{ color: #e67e22; }}
.s-taverna .spread-title {{ color: #faece3; }}
.s-taverna .spread-lede {{ color: #e7c5b0; border-color: #d35400; }}
.s-taverna .spread-text {{ color: #cead98; }}
.s-taverna .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #1b0a03 100%);
}}

/* 12. Hisseli Harikalar (Театр) */
.s-hisseli {{
  --panel-bg: #33080e;
  --text-accent: #f1c40f;
}}
.s-hisseli .spread-body {{
  background: linear-gradient(135deg, #200408 0%, #460d16 100%);
  border: 1px solid rgba(241, 196, 15, 0.1);
}}
.s-hisseli .spread-tag {{ color: #f39c12; }}
.s-hisseli .spread-title {{ color: #fdf2d0; font-family: 'Cinzel', serif; }}
.s-hisseli .spread-lede {{ color: #eecda3; border-color: #f1c40f; }}
.s-hisseli .spread-text {{ color: #ccaeab; }}
.s-hisseli .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #200408 100%);
}}

/* 13. Шахов тоже убивают */
.s-sahlari {{
  --panel-bg: #1c0e2b;
  --text-accent: #9b59b6;
}}
.s-sahlari .spread-body {{
  background: linear-gradient(135deg, #10071a 0%, #28153c 100%);
}}
.s-sahlari .spread-tag {{ color: #be2edd; }}
.s-sahlari .spread-title {{ color: #f5ebff; }}
.s-sahlari .spread-lede {{ color: #d6bdf2; border-color: #9b59b6; }}
.s-sahlari .spread-text {{ color: #baa3cc; }}
.s-sahlari .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #10071a 100%);
}}

/* 14. Джон Леннон (Космос/Звезды) */
.s-lennon {{
  --panel-bg: #05060b;
  --text-accent: #f5f6fa;
}}
.s-lennon .spread-body {{
  background: radial-gradient(circle at 70% 30%, #0c0e1a 0%, #030407 100%);
  position: relative;
}}
.s-lennon .spread-tag {{ color: #dcdde1; }}
.s-lennon .spread-title {{ color: #ffffff; font-family: 'Playfair Display', serif; font-weight: 400; }}
.s-lennon .spread-lede {{ color: #f5f6fa; border-color: #f5f6fa; font-family: 'PT Serif', serif; font-style: italic; }}
.s-lennon .spread-text {{ color: #dcdde1; }}
.s-lennon .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #030407 100%);
}}

/* 15. Йешильчам (Кинолента) */
.s-yesilcam {{
  --panel-bg: #1d1713;
  --text-accent: #e67e22;
}}
.s-yesilcam .spread-body {{
  background: linear-gradient(135deg, #120e0b 0%, #29211b 100%);
}}
.s-yesilcam .spread-tag {{ color: #e67e22; }}
.s-yesilcam .spread-title {{ color: #f6efe9; font-family: 'Playfair Display', serif; font-style: italic; }}
.s-yesilcam .spread-lede {{ color: #dfd2c6; border-color: #e67e22; }}
.s-yesilcam .spread-text {{ color: #c3b4a5; }}
.s-yesilcam .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #120e0b 100%);
}}

/* 16. Трабзонспор (Спорт) */
.s-sport {{
  --panel-bg: #26050b;
  --text-accent: #87ceeb;
}}
.s-sport .spread-body {{
  background: linear-gradient(135deg, #1a0206 0%, #350b14 100%);
  border-left: 2px solid #87ceeb;
}}
.s-sport .spread-tag {{ color: #87ceeb; }}
.s-sport .spread-title {{ color: #fae6ea; font-family: 'PT Sans', sans-serif; font-weight: 900; }}
.s-sport .spread-lede {{ color: #e9c9cf; border-color: #87ceeb; }}
.s-sport .spread-text {{ color: #cfb2b6; }}
.s-sport .spread-photo::after {{
  background: linear-gradient(90deg, transparent 65%, #1a0206 100%);
}}

/* ═══════════════════════════════════════════
   ХРОНОЛОГИЯ И СИМВОЛЫ
═══════════════════════════════════════════ */
.chronicle {{
  background: rgba(18, 8, 2, .9);
  color: var(--cream);
  padding: 60px 80px;
  position: relative;
  z-index: 5;
  border-top: 1px solid rgba(255,255,255,.07);
}}
.chronicle h2 {{
  font-family: 'Cinzel', serif;
  font-size: 24px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(255,200,80,.85);
  margin-bottom: 40px;
  text-align: center;
}}
.chronicle-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px 40px;
}}
.chronicle-item {{
  display: flex;
  gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255,255,255,.05);
  font-size: 14px;
  line-height: 1.6;
}}
.chron-month {{
  font-family: 'Cinzel', serif;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(255,200,80,.85);
  margin: 30px 0 10px;
  grid-column: 1 / -1;
  border-bottom: 2px solid rgba(255,200,80,.2);
  padding-bottom: 6px;
}}

.symbols-section {{
  margin: 0;
  background: rgba(26, 12, 4, 0.95);
  color: var(--cream);
  border-top: 1px solid rgba(255,255,255,.07);
  padding: 60px 80px;
  position: relative;
  z-index: 5;
}}
.symbols-title {{
  font-family: 'Cinzel', serif;
  font-size: 24px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(255,200,80,.85);
  margin-bottom: 40px;
  text-align: center;
}}
.symbols-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}}
.symbol-item {{
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.02);
  padding: 24px;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 4px;
  transition: all 0.3s ease;
}}
.symbol-item:hover {{
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,200,80,0.3);
  transform: translateY(-4px);
}}
.symbol-name {{
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 700;
  color: rgba(255,200,80,.95);
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(255,200,80,0.15);
  padding-bottom: 8px;
}}
.symbol-desc {{
  font-size: 13.5px;
  color: rgba(255,255,255,0.6);
  line-height: 1.65;
}}

/* ── ЛАЙТБОКС (Lightbox Modal) ── */
.lightbox {{
  position: fixed;
  inset: 0;
  background: rgba(10,8,7,0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.35s ease;
  padding: 40px;
}}
.lightbox.active {{
  opacity: 1;
  pointer-events: auto;
}}
.lightbox-content {{
  max-width: 90%;
  max-height: 80vh;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}}
.lightbox-content img {{
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
  border: 2px solid rgba(255,255,255,0.1);
  box-shadow: 0 20px 50px rgba(0,0,0,0.8);
}}
.lightbox-caption {{
  color: rgba(255,255,255,0.8);
  font-family: 'PT Sans', sans-serif;
  font-size: 13px;
  font-style: italic;
  margin-top: 15px;
  text-align: center;
  line-height: 1.5;
  max-width: 600px;
}}
.lightbox-close {{
  position: absolute;
  top: 30px;
  right: 40px;
  color: #fff;
  font-size: 40px;
  font-weight: 300;
  cursor: pointer;
  background: none;
  border: none;
  transition: transform 0.2s;
  z-index: 2001;
}}
.lightbox-close:hover {{
  transform: scale(1.1) rotate(90deg);
}}

/* ── Футер ── */
footer {{
  background: rgba(12,5,1,1);
  color: #777;
  text-align: center;
  padding: 40px;
  font-size: 12px;
  font-family: 'PT Sans', sans-serif;
  border-top: 1px solid #222;
  position: relative;
  z-index: 5;
}}
footer a {{
  color: #999;
  text-decoration: none;
}}
footer a:hover {{ color: #fff; }}

@media(max-width:900px){{
  .chronicle {{ padding: 40px 20px; }}
  .symbols-section {{ padding: 40px 20px; }}
  .symbols-grid {{ grid-template-columns: 1fr; gap: 20px; }}
}}
</style>
</head>
<body>

<div class="bg-canvas"></div>

<!-- ══════════════════════════════════════════
     ШАПКА
══════════════════════════════════════════ -->
<header class="site-header">
  <div class="header-inner">
    <div class="year-mark">1980</div>
    <div class="header-brand">
      <div class="site-name">Намедни по-турецки</div>
      <div class="site-sub">Турция · Феномены по годам · 1980–1991</div>
    </div>
    <div class="spread-counter"><span id="cur">1</span> / <span id="tot">16</span></div>
  </div>
  <nav class="header-nav">
    <a href="index.html" style="color:rgba(255,200,80,.85);">← Все годы</a>
    {"".join(f'<a href="#{SECTIONS_CONFIG[t]["id"]}">{t.split(":")[0]}</a>' for t in sorted_titles)}
  </nav>
</header>

<main>
  {"".join(spreads_html)}
</main>

<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close">&times;</button>
  <div class="lightbox-content" onclick="event.stopPropagation()">
    <img id="lightboxImg" src="" alt="">
    <div class="lightbox-caption" id="lightboxCap"></div>
  </div>
</div>

<footer>
  <p>© Намедни по-турецки · <a href="index.html">Все годы</a></p>
</footer>

<script>
// ── Скролл-динамика градиента ──────────────────
window.addEventListener('scroll', () => {{
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  if (scrollHeight <= 0) return;
  const pct = window.scrollY / scrollHeight;
  document.documentElement.style.setProperty('--scroll-pct', pct);
  document.documentElement.style.setProperty('--scroll-angle', `${{125 + pct * 180}}deg`);
}});

// ── Лайтбокс ──────────────────
function openLightbox(src, alt) {{
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCap');
  img.src = src;
  cap.textContent = alt || '';
  lb.classList.add('active');
  document.body.style.overflow = 'hidden';
}}

function closeLightbox() {{
  const lb = document.getElementById('lightbox');
  lb.classList.remove('active');
  document.body.style.overflow = '';
}}

document.addEventListener('keydown', (e) => {{
  if (e.key === 'Escape') closeLightbox();
}});

// ── Счётчик текущего разворота и подсветка меню ──────────────────
(function () {{
  const spreads = [...document.querySelectorAll('.spread[data-idx]')];
  const cur = document.getElementById('cur');
  const tot = document.getElementById('tot');
  if (!spreads.length) return;
  tot.textContent = spreads.length;

  const io = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting && e.intersectionRatio >= 0.3) {{
        cur.textContent = e.target.dataset.idx;
      }}
    }});
  }}, {{ threshold: 0.3 }});

  spreads.forEach(s => io.observe(s));

  // Подсветка активной категории в навигации
  const banners = [...document.querySelectorAll('.group-banner')];
  const links = [...document.querySelectorAll('.header-nav a[href^="#"]')];

  const bio = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        const id = e.target.id;
        links.forEach(l => {{
          l.classList.toggle('active', l.getAttribute('href') === '#' + id);
        }});
      }}
    }});
  }}, {{ rootMargin: '-10% 0px -75% 0px' }});

  banners.forEach(b => bio.observe(b));
}})();
</script>

</body>
</html>
'''

# Write to target files
with open(BASE_DIR / "80808080.html", "w") as f:
    f.write(html_template)
    
with open(BASE_DIR / "1980_Gemini.html", "w") as f:
    f.write(html_template)

print("Both 80808080.html and 1980_Gemini.html updated successfully!")
