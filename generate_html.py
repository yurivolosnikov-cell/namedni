#!/usr/bin/env python3
"""
Generate year HTML pages from .md source files.
Reproduces the burgundy notebook style from existing pages.
"""
import re, html, os, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("NAMEDNI_OUT", BASE))

# Key events per year for header subtitle
SUBTITLES = {
    "1980": "12 сентября · Программа 24 января · Бюлент Эрсой · Даллас · Йешильчам",
    "1981": "Агджа · Мюнир Нуреттин · ЙЁК · Трабзонспор · Мамак · Walkman",
    "1982": "«Йол» в Каннах · Банкер Кастелли · АСАЛА · Конституция 91,4% · Gırgır",
    "1983": "АНАП · ККТЦ · АСАЛА в Орли · Землетрясение · E.T. · Studio FM",
    "1984": "ПКК начало · Оруэлл год · Цветное ТВ · Флэшдэнс · Сабанджы",
    "1985": "Болгарские турки · KDV · Рухи Су · Live Aid · 50 миллионов",
    "1986": "Чернобыль · Галерея открывается · Кундера · Видеомагнитофон · Мадонна",
    "1987": "Маганда · Мухсин-бей · Наим · Выборы · Sezen Aksu",
    "1988": "Покушение на Озала · Наим в Сеуле · Галерея · Майлс и Жоан · Берген",
    "1989": "Стена · Озал президент · Берген · Болгарские турки · Первое частное ТВ",
    "1990": "Война в Заливе · Убийства · Памук «Чёрная книга» · Зонгулдак · Show TV",
    "1991": "Зонгулдак · Беженцы · Конец АНАП · Дев-Сол · Метин Октай · Манчо",
}

CSS = """
  @import url('https://fonts.googleapis.com/css2?family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Sans:wght@400;700;900&display=swap');
  :root{--cream:#f5f0e8;--dark:#1a1410;--burgundy:#6b0f1a;--red:#c0392b;--gold:#b8860b;--midgray:#5a5248;--lightgray:#d4cfc8;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--cream);color:var(--dark);font-family:'PT Serif',Georgia,serif;font-size:16px;line-height:1.7;}
  header{background:linear-gradient(135deg,#5a0a14 0%,#7d121e 100%);color:#fff;position:sticky;top:0;z-index:1000;box-shadow:0 4px 15px rgba(0,0,0,.15);}
  .header-inner{max-width:1300px;margin:0 auto;padding:20px 40px;display:flex;align-items:center;gap:40px;}
  .year-number{font-family:'PT Sans',sans-serif;font-size:100px;font-weight:900;line-height:1;color:#fff;letter-spacing:-2px;}
  .header-divider{width:2px;height:70px;background:rgba(255,255,255,.25);flex-shrink:0;}
  .header-text{display:flex;flex-direction:column;gap:6px;font-family:'PT Sans',sans-serif;}
  .header-main-title{font-size:18px;font-weight:700;letter-spacing:1.5px;color:#fff;text-transform:uppercase;}
  .header-summary{font-size:14px;color:#e5cfd2;}
  .header-section{font-size:12px;color:var(--gold);font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-top:2px;}
  .toc{background:var(--dark);color:var(--cream);border-top:1px solid #2a2520;}
  .toc-inner{max-width:1300px;margin:0 auto;padding:15px 40px;display:flex;flex-wrap:wrap;gap:6px 28px;font-family:'PT Sans',sans-serif;font-size:13px;}
  .toc span{color:var(--gold);margin-right:4px;font-weight:700;}
  .toc a{color:#c8c0b0;text-decoration:none;transition:color .2s;}
  .toc a:hover{color:var(--cream);}
  main{max-width:1300px;margin:0 auto;padding:0 40px 80px;}
  .year-nav-bar{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-bottom:1px solid var(--lightgray);font-family:'PT Sans',sans-serif;font-size:13px;margin-bottom:20px;}
  .year-nav-bar a{color:var(--burgundy);text-decoration:none;font-weight:700;}
  .year-nav-bar a:hover{text-decoration:underline;}
  .phenomenon{margin:60px 0;padding-bottom:60px;border-bottom:1px solid var(--lightgray);display:flex;flex-direction:column;gap:20px;}
  .pill-label{padding:5px 12px;background:var(--burgundy);color:#fff;display:inline-block;font-weight:700;font-family:'PT Sans',sans-serif;font-size:11px;letter-spacing:1px;border-radius:2px;width:fit-content;text-transform:uppercase;margin-bottom:8px;}
  .phenom-title{font-family:'PT Sans',sans-serif;font-size:36px;font-weight:900;line-height:1.15;margin-bottom:10px;color:var(--dark);text-transform:uppercase;letter-spacing:-.5px;}
  .phenom-lede{border-left:5px solid var(--burgundy);padding-left:20px;margin:10px 0 25px;font-style:italic;font-weight:700;font-size:18px;line-height:1.6;color:#1a1410;font-family:'PT Serif',serif;}
  .phenom-body-text{column-count:2;column-gap:40px;text-align:justify;color:#2a2420;font-size:15px;line-height:1.75;}
  .phenom-body-text p{margin-bottom:12px;}
  .phenom-body-text p:last-child{margin-bottom:0;}
  .ref-note{font-size:13px;color:var(--midgray);font-style:italic;margin-top:8px;}
  /* ── FALLBACK (no photo yet) ── */
  .fallback-box{background:#eae6de;border:1px dashed #c8c0b0;padding:40px 30px;text-align:center;font-family:'PT Sans',sans-serif;color:#8a8278;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;margin:0 0 28px;min-height:180px;}
  .fallback-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:#a09488;}
  .fallback-subtitle{font-size:11px;}

  /* ── PHOTO CAPTION shared style ── */
  .img-cap{font-family:'PT Sans',sans-serif;font-size:12px;color:var(--midgray);margin-top:8px;line-height:1.55;font-style:italic;padding-left:2px;}

  /* ── HERO: full-width photo, NO crop, natural height ── */
  .img-hero{width:100%;margin:0 0 28px;}
  .img-hero img{width:100%;height:auto;display:block;border:1px solid var(--lightgray);filter:sepia(8%) contrast(1.04) brightness(1.01);}

  /* ── PAIR: two equal photos side by side, full width, NO crop ── */
  .img-pair{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:32px -0px 0;width:100%;}
  .img-pair figure{margin:0;}
  .img-pair figure img{width:100%;height:auto;display:block;border:1px solid var(--lightgray);filter:sepia(8%) contrast(1.04);}

  /* ── TRIO: three photos in a row, NO crop ── */
  .img-trio{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:32px 0 0;width:100%;}
  .img-trio figure{margin:0;}
  .img-trio figure img{width:100%;height:auto;display:block;border:1px solid var(--lightgray);filter:sepia(8%) contrast(1.04);}

  /* ── RIGHT FLOAT: sidebar photo, NO crop ── */
  .img-right{float:right;width:40%;margin:6px 0 20px 32px;}
  .img-right img{width:100%;height:auto;display:block;border:1px solid var(--lightgray);filter:sepia(8%) contrast(1.04);}
  .phenom-body-text::after{content:'';display:table;clear:both;}

  @media(max-width:800px){
    .img-pair,.img-trio{grid-template-columns:1fr;}
    .img-right{float:none;width:100%;margin:20px 0;}
  }
  .chronicle{background:var(--dark);color:var(--cream);margin:70px -40px 0;padding:50px 40px;}
  .chronicle h2{font-family:'PT Sans',sans-serif;font-size:13px;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:30px;font-weight:400;}
  .chronicle-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:6px 40px;}
  .chronicle-item{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid #2a2520;font-size:14px;}
  .chron-month{font-family:'PT Sans',sans-serif;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--gold);margin:20px 0 10px;grid-column:1/-1;}
  .symbols-section{margin:60px 0;background:var(--cream);border:1px solid var(--lightgray);padding:40px;}
  .symbols-title{font-family:'PT Sans',sans-serif;font-size:11px;letter-spacing:3px;text-transform:uppercase;color:var(--midgray);margin-bottom:30px;}
  .symbols-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 40px;}
  .symbol-item{display:flex;flex-direction:column;}
  .symbol-name{font-family:'PT Serif',serif;font-size:20px;font-weight:700;color:var(--burgundy);margin-bottom:8px;}
  .symbol-desc{font-size:14px;color:var(--midgray);line-height:1.6;}
  footer{background:var(--dark);color:#777;text-align:center;padding:30px 40px;font-size:12px;font-family:'PT Sans',sans-serif;border-top:1px solid #222;}
  footer a{color:#999;text-decoration:none;}
  @media(max-width:900px){
    .header-inner{padding:15px 20px;gap:20px;}
    .year-number{font-size:60px;}
    main{padding:0 20px 60px;}
    .phenom-body-text{column-count:1;}
    .symbols-grid{grid-template-columns:1fr;}
    .chronicle{margin:70px -20px 0;padding:40px 20px;}
  }
"""

def he(s):
    return html.escape(str(s))

def parse_md(year):
    path = BASE / f"{year}.md"
    with open(path) as f:
        raw = f.read()
    
    sections = re.split(r'\n## ', raw)
    articles = []
    for s in sections[1:]:
        lines = s.strip().split('\n')
        title = lines[0].strip()
        body  = '\n'.join(lines[1:]).strip()
        articles.append((title, body))
    return articles

def render_body(body):
    """Convert markdown body to HTML paragraphs."""
    parts = []
    # ── Step 1: tokenise ![alt](path)\n*caption* ──────────────────────────
    body = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)\n\*([^*\n]+)\*',
        lambda m: f'§IMG§{m.group(2)}¦¦{m.group(1)}¦¦{m.group(3)}§END§',
        body
    )
    # bare image without caption
    body = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)(?!\n\*)',
        lambda m: f'§IMG§{m.group(2)}¦¦{m.group(1)}¦¦§END§',
        body
    )
    # {right} prefix
    body = re.sub(r'\{right\}(§IMG§[^§]+§END§)', r'§RIGHT§\1', body)

    # {pair} explicit pair block: {pair}§IMG§...§END§\n§IMG§...§END§
    body = re.sub(
        r'\{pair\}(§IMG§[^§]+§END§)\n(§IMG§[^§]+§END§)',
        lambda m: f'§PAIR§{m.group(1)}¶{m.group(2)}§ENDPAIR§',
        body
    )

    # ── Step 2: auto-group consecutive images ─────────────────────────────
    # trio (3 in a row, blank lines)
    body = re.sub(
        r'(§IMG§[^§]+§END§)\n\n(§IMG§[^§]+§END§)\n\n(§IMG§[^§]+§END§)',
        lambda m: f'§TRIO§{m.group(1)}¶{m.group(2)}¶{m.group(3)}§ENDTRIO§',
        body
    )
    # pair (2 in a row, blank lines)
    body = re.sub(
        r'(§IMG§[^§]+§END§)\n\n(§IMG§[^§]+§END§)',
        lambda m: f'§PAIR§{m.group(1)}¶{m.group(2)}§ENDPAIR§',
        body
    )

    def fig(path, alt, caption):
        cap_html = f'<figcaption class="img-cap">{he(caption)}</figcaption>' if caption else ''
        return (f'<figure>'
                f'<img src="{he(path)}" alt="{he(alt)}" loading="lazy">'
                f'{cap_html}</figure>')

    def parse_tok(tok):
        tok = tok.strip()
        if not tok.startswith('§IMG§'): return ''
        parts_t = tok[5:-5].split('¦¦')
        path, alt, caption = parts_t[0], parts_t[1], parts_t[2] if len(parts_t)>2 else ''
        return path, alt, caption

    for para in body.split('\n\n'):
        para = para.strip()
        if not para: continue
        if para.startswith('|'): continue

        # RIGHT float
        if para.startswith('§RIGHT§§IMG§'):
            t = parse_tok(para[8:])
            if t:
                path, alt, caption = t
                cap_html = f'<figcaption class="img-cap">{he(caption)}</figcaption>' if caption else ''
                parts.append(f'<div class="img-right"><img src="{he(path)}" alt="{he(alt)}" loading="lazy">{cap_html}</div>')
            continue

        # TRIO
        if para.startswith('§TRIO§'):
            inner = para[6:-9]
            figs = ''.join(fig(*parse_tok(t)) for t in inner.split('¶') if parse_tok(t))
            parts.append(f'<div class="img-trio">{figs}</div>')
            continue

        # PAIR
        if para.startswith('§PAIR§'):
            inner = para[6:-9]
            figs = ''.join(fig(*parse_tok(t)) for t in inner.split('¶') if parse_tok(t))
            parts.append(f'<div class="img-pair">{figs}</div>')
            continue

        # SINGLE HERO
        if para.startswith('§IMG§'):
            t = parse_tok(para)
            if t:
                path, alt, caption = t
                cap_html = f'<figcaption class="img-cap">{he(caption)}</figcaption>' if caption else ''
                parts.append(f'<div class="img-hero"><img src="{he(path)}" alt="{he(alt)}" loading="lazy">{cap_html}</div>')
            continue
        # lede: single line **...**
        if para.startswith('**') and para.endswith('**') and '\n' not in para:
            parts.append(f'<p class="phenom-lede">{he(para[2:-2])}</p>')
            continue
        # ref note *(см. ...)*
        if para.startswith('*(') and para.endswith(')*'):
            parts.append(f'<p class="ref-note">{he(para[2:-2])}</p>')
            continue
        # chronology lines: starts with - or **Month**
        lines = para.split('\n')
        is_chron = all(l.strip().startswith('-') or l.strip().startswith('**') or not l.strip() for l in lines)
        if is_chron and any(l.strip().startswith('-') for l in lines):
            items = []
            for l in lines:
                l = l.strip()
                if not l: continue
                if l.startswith('**') and l.endswith('**'):
                    items.append(f'<div class="chron-month">{he(l[2:-2])}</div>')
                elif l.startswith('- '):
                    items.append(f'<div class="chronicle-item"><span>—</span><span>{he(l[2:])}</span></div>')
            parts.append('<div class="chronicle-grid">' + ''.join(items) + '</div>')
            continue
        # symbol entries: **Name.** text
        sym_match = re.match(r'^\*\*(.+?)\.\*\*\s*(.+)$', para, re.DOTALL)
        if sym_match:
            name, desc = sym_match.groups()
            parts.append(f'<div class="symbol-item"><div class="symbol-name">{he(name)}</div><div class="symbol-desc">{he(desc.strip())}</div></div>')
            continue
        # normal paragraph
        parts.append(f'<p>{he(para)}</p>')
    return '\n'.join(parts)

def make_slug(title):
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s.strip())
    return re.sub(r'-+', '-', s)[:60] or 'sec'

def generate_year(year):
    articles = parse_md(year)
    yr = int(year)
    prev_yr = str(yr - 1)
    next_yr = str(yr + 1)
    
    subtitle = SUBTITLES.get(year, '')
    
    # Separate main articles, chronology, symbols
    main_arts   = [(t,b) for t,b in articles if 'Хронология' not in t and 'Символы' not in t]
    chron_arts  = [(t,b) for t,b in articles if 'Хронология' in t]
    symbol_arts = [(t,b) for t,b in articles if 'Символы' in t]
    
    # TOC links
    toc_items = ''.join(
        f'<span>·</span><a href="#{make_slug(t)}">{he(t)}</a>'
        for t,_ in main_arts
    )
    
    # Main articles HTML
    arts_html_parts = []
    for title, body in main_arts:
        slug = make_slug(title)
        body_html = render_body(body)

        # Extract lede
        lede_m = re.search(r'<p class="phenom-lede">.*?</p>', body_html, re.DOTALL)
        lede_html = lede_m.group(0) if lede_m else ''
        rest_html = body_html.replace(lede_html, '', 1).strip() if lede_html else body_html

        # Pull ALL full-width blocks (hero, pair, trio) OUT of the body column
        # They go AFTER the text block at full article width
        # img-right stays INSIDE the text (float)
        fullwidth_pattern = re.compile(
            r'<div class="img-(?:hero|pair|trio)">.*?</div>',
            re.DOTALL
        )

        # Collect in order
        above_blocks = []   # hero goes above text
        below_blocks = []   # pair/trio go below text
        hero_found = False

        def extract_fw(m):
            block = m.group(0)
            nonlocal hero_found
            if 'img-hero' in block and not hero_found:
                hero_found = True
                above_blocks.append(block)
            else:
                below_blocks.append(block)
            return ''   # remove from body

        rest_html = fullwidth_pattern.sub(extract_fw, rest_html).strip()

        # Build photo block above text
        if above_blocks:
            photo_block = '\n'.join(above_blocks)
        else:
            photo_block = (
                '<div class="fallback-box">'
                '<div class="fallback-title">Архивное фото</div>'
                '<div class="fallback-subtitle">Место для исторической фотографии</div>'
                '</div>'
            )

        below_html = '\n'.join(below_blocks)

        arts_html_parts.append(f'''
<div class="phenomenon" id="{slug}">
  <div>
    <div class="pill-label">{he(year)}</div>
    <h2 class="phenom-title">{he(title)}</h2>
  </div>
  {lede_html}
  {photo_block}
  <div class="phenom-body-text">
    {rest_html}
  </div>
  {below_html}
</div>''')
    
    # Chronology section
    chron_html = ''
    if chron_arts:
        _, chron_body = chron_arts[0]
        chron_content = render_body(chron_body)
        chron_html = f'''
<section class="chronicle">
  <h2>Хронология {year}</h2>
  {chron_content}
</section>'''
    
    # Symbols section
    symbols_html = ''
    if symbol_arts:
        _, sym_body = symbol_arts[0]
        sym_content = render_body(sym_body)
        symbols_html = f'''
<section class="symbols-section">
  <div class="symbols-title">Символы {year} года</div>
  <div class="symbols-grid">
    {sym_content}
  </div>
</section>'''
    
    # Year nav
    prev_link = f'<a href="{prev_yr}.html">← {prev_yr}</a>' if yr > 1980 else '<span></span>'
    next_link = f'<a href="{next_yr}.html">{next_yr} →</a>' if yr < 1991 else '<span></span>'
    
    page = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Намедни по-турецки — {year}</title>
<style>{CSS}</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="year-block">
      <div class="year-number">{year}</div>
    </div>
    <div class="header-divider"></div>
    <div class="header-text">
      <div class="header-main-title">Намедни по-турецки</div>
      <div class="header-summary">{he(subtitle)}</div>
      <div class="header-section">Турция · Феномены по годам</div>
    </div>
  </div>
  <nav class="toc">
    <div class="toc-inner">
      <a href="index.html" style="color:var(--gold);font-weight:700;text-decoration:none;">← Все годы</a>
      {toc_items}
    </div>
  </nav>
</header>

<main>
  <div class="year-nav-bar">
    {prev_link}
    <span style="font-family:'PT Sans',sans-serif;color:var(--midgray);">{year} — {len(main_arts)} феноменов</span>
    {next_link}
  </div>

  {''.join(arts_html_parts)}

  {chron_html}
  {symbols_html}

</main>

<footer>
  <p>© Намедни по-турецки · <a href="index.html">Все годы</a></p>
</footer>

</body>
</html>'''
    
    out = OUT / f"{year}.html"
    with open(out, 'w') as f:
        f.write(page)
    return len(main_arts)

# Generate all years
years = sys.argv[1:] or [str(y) for y in range(1980, 1992)]
for year in years:
    count = generate_year(year)
    print(f"  {year}.html — {count} феноменов")

print("\nГотово!")
