#!/usr/bin/env python3
import re
from pathlib import Path

# Common HTML header template
def get_html_header(title, active_tab):
    tabs = {
        "index": "Феномены по годам",
        "companies": "30 крупнейших компаний Турции",
        "rich_families": "30 самых богатых людей и семей Турции",
        "actors": "Список турецких актеров"
    }
    
    nav_html = ""
    for tab_id, tab_title in tabs.items():
        active_class = "active" if tab_id == active_tab else ""
        href = "index.html" if tab_id == "index" else f"{tab_id}.html"
        nav_html += f'        <a href="{href}" class="nav-item {active_class}">{tab_title}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Намедни по-турецки — {title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=PT+Serif:ital,wght@0,400;0,700;1,400&family=PT+Sans:wght@400;700&display=swap');

  :root {{
    --dark-blue: #070c24;
    --dark-red: #800c14;
    --gold: #b8860b;
    --text-color: #1a1a1a;
    --link-color: #1a548c;
    --bullet-color: #999999;
    --bg-cream: #faf9f6;
    --cream-card: #f5f0e8;
    --border-color: #d4cfc8;
  }}

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    background-color: var(--bg-cream);
    color: var(--text-color);
    font-family: 'PT Serif', Georgia, serif;
    font-size: 16px;
    line-height: 1.7;
  }}

  /* ======= HEADER STYLE ======= */
  header {{
    background: linear-gradient(135deg, rgba(7, 12, 36, 0.88) 0%, rgba(74, 13, 21, 0.8) 60%, rgba(128, 12, 20, 0.88) 100%), url('turkish_collage.png') no-repeat center center;
    background-size: cover;
    color: #ffffff;
    padding: 30px 40px 0 40px;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }}

  .header-container {{
    max-width: 1250px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    position: relative;
  }}

  .header-left {{
    display: flex;
    flex-direction: column;
  }}

  .header-title-block {{
    margin-bottom: 25px;
  }}

  .header-title {{
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.5px;
    line-height: 1.2;
    color: #ffffff;
  }}

  .header-subtitle {{
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 16px;
    font-weight: 400;
    opacity: 0.85;
    margin-top: 2px;
  }}

  /* ======= HEADER NAVIGATION ======= */
  nav.header-nav {{
    display: flex;
    gap: 24px;
  }}

  .nav-item {{
    color: #d8c2c8;
    text-decoration: none;
    font-weight: 700;
    font-size: 13px;
    padding-bottom: 12px;
    border-bottom: 3px solid transparent;
    transition: color 0.2s, border-bottom-color 0.2s;
    font-family: 'PT Sans', Arial, sans-serif;
  }}

  .nav-item:hover {{
    color: #ffffff;
  }}

  .nav-item.active {{
    color: #ffffff;
    border-bottom-color: #ffffff;
  }}

  .ntv-badge-container {{
    display: flex;
    align-items: center;
    align-self: center;
    margin-bottom: 15px;
  }}

  .ntv-badge {{
    width: 44px;
    height: 44px;
    background-color: #1a1a1a;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    border: 1px solid #333;
    transition: transform 0.2s ease;
  }}

  .ntv-badge:hover {{
    transform: scale(1.08);
  }}

  .ntv-asterisk {{
    color: #a3cc29;
    font-size: 32px;
    font-weight: bold;
    line-height: 1;
    font-family: 'PT Sans', sans-serif;
    cursor: default;
  }}

  /* ======= MAIN CONTAINER ======= */
  main {{
    max-width: 1250px;
    margin: 40px auto 80px;
    padding: 0 40px;
  }}

  .page-title {{
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 900;
    color: #111111;
    margin-bottom: 25px;
    letter-spacing: -0.5px;
    border-bottom: 2px solid var(--dark-red);
    padding-bottom: 10px;
  }}
  
  .intro-text {{
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 35px;
    color: #333;
    font-style: italic;
  }}

  /* ======= STYLED TABLES ======= */
  table.premium-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 30px 0;
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    border-radius: 4px;
    overflow: hidden;
  }}

  table.premium-table th {{
    background-color: var(--dark-blue);
    color: #ffffff;
    font-family: 'PT Sans', sans-serif;
    font-weight: 700;
    text-align: left;
    padding: 14px 20px;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  table.premium-table td {{
    padding: 14px 20px;
    border-bottom: 1px solid var(--border-color);
    font-size: 15px;
  }}

  table.premium-table tr:last-child td {{
    border-bottom: none;
  }}

  table.premium-table tr:nth-child(even) {{
    background-color: #fcfbfa;
  }}

  table.premium-table tr:hover {{
    background-color: #f7f5f0;
  }}
  
  .rank-badge {{
    display: inline-block;
    width: 28px;
    height: 28px;
    background-color: var(--dark-red);
    color: #ffffff;
    border-radius: 50%;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    font-family: 'PT Sans', sans-serif;
    font-size: 13px;
  }}

  /* ======= CARDS & LISTS ======= */
  .bracket-section {{
    margin-bottom: 45px;
  }}

  .bracket-title {{
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--dark-red);
    margin-bottom: 20px;
    border-left: 4px solid var(--gold);
    padding-left: 15px;
  }}

  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 20px;
  }}

  .family-card {{
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    display: flex;
    align-items: center;
    gap: 15px;
    transition: transform 0.2s, box-shadow 0.2s;
  }}

  .family-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    border-color: var(--gold);
  }}

  .family-num {{
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 900;
    color: var(--gold);
    min-width: 40px;
  }}

  .family-details {{
    display: flex;
    flex-direction: column;
  }}

  .family-name {{
    font-weight: 700;
    font-size: 18px;
    color: var(--text-color);
  }}

  .family-business {{
    font-family: 'PT Sans', sans-serif;
    font-size: 14px;
    color: #666;
    margin-top: 2px;
  }}

  /* ======= ACTORS DESIGN ======= */
  .actor-block {{
    margin-bottom: 40px;
  }}

  .actor-section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 900;
    color: var(--dark-blue);
    margin: 40px 0 20px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 8px;
  }}

  .actor-era-title {{
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--dark-red);
    margin: 25px 0 15px;
  }}

  .actors-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    margin-bottom: 40px;
  }}

  @media (max-width: 800px) {{
    .actors-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .actor-card {{
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 25px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.02);
  }}

  .actor-name {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--dark-blue);
    margin-bottom: 8px;
  }}

  .actor-meta {{
    font-family: 'PT Sans', sans-serif;
    font-size: 13px;
    color: var(--gold);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }}

  .actor-bio {{
    font-size: 15px;
    color: #333333;
    line-height: 1.6;
  }}
  
  .actor-bio p {{
    margin-bottom: 10px;
  }}
  .actor-bio p:last-child {{
    margin-bottom: 0;
  }}

  .alphabet-columns {{
    column-count: 4;
    column-gap: 30px;
    margin-top: 20px;
    background: #ffffff;
    padding: 30px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
  }}

  @media (max-width: 900px) {{
    .alphabet-columns {{
      column-count: 3;
    }}
  }}
  @media (max-width: 600px) {{
    .alphabet-columns {{
      column-count: 2;
    }}
  }}
  @media (max-width: 400px) {{
    .alphabet-columns {{
      column-count: 1;
    }}
  }}

  .letter-group {{
    break-inside: avoid;
    margin-bottom: 20px;
  }}

  .letter-title {{
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    color: var(--dark-red);
    border-bottom: 2px solid var(--gold);
    display: inline-block;
    padding-right: 15px;
    margin-bottom: 8px;
  }}

  .actors-list-item {{
    list-style: none;
    font-family: 'PT Sans', sans-serif;
    font-size: 14px;
    padding: 4px 0;
    color: #444;
  }}

  /* ======= FOOTER ======= */
  footer {{
    background-color: #111111;
    color: #777777;
    text-align: center;
    padding: 30px 40px;
    font-size: 12px;
    border-top: 1px solid #222;
    font-family: 'PT Sans', sans-serif;
  }}

  footer a {{
    color: #999999;
    text-decoration: none;
    transition: color 0.2s;
  }}

  footer a:hover {{
    color: #ffffff;
  }}

  /* ======= RESPONSIVE DESIGN ======= */
  @media (max-width: 900px) {{
    header {{
      padding: 20px 20px 0 20px;
    }}
    main {{
      padding: 0 20px;
      margin: 30px auto 60px;
    }}
  }}

  @media (max-width: 600px) {{
    .header-container {{
      flex-direction: column;
      gap: 15px;
    }}
    .ntv-badge-container {{
      align-self: flex-start;
      margin-bottom: 10px;
    }}
    nav.header-nav {{
      flex-wrap: wrap;
      gap: 12px;
    }}
    .nav-item {{
      font-size: 12px;
      padding-bottom: 6px;
    }}
  }}
</style>
</head>
<body>

<header>
  <div class="header-container">
    <div class="header-left">
      <div class="header-title-block">
        <h2 class="header-title">Намедни по-турецки</h2>
        <div class="header-subtitle">Проект, вдохновленный Л.Парфеновым</div>
      </div>
      <nav class="header-nav">
{nav_html}      </nav>
    </div>
    <div class="ntv-badge-container">
      <div class="ntv-badge" title="Намедни / НТВ">
        <span class="ntv-asterisk">✳</span>
      </div>
    </div>
  </div>
</header>

<main>
"""

def get_html_footer():
    return """
</main>

<footer>
  <p>© Намедни по-турецки · Проект, вдохновленный Л.Парфеновым. <a href="index.html">Феномены по годам</a></p>
</footer>

</body>
</html>
"""

def compile_companies():
    events_file = Path("Значимые турецкие события и персоналии.md")
    if not events_file.exists():
        print(f"Error: {events_file} not found")
        return
        
    content = events_file.read_text(encoding="utf-8")
    
    # Extract the companies section
    pattern = r"# (?:Türkiye’nin En Büyük 30 Firması — 30 крупнейших компаний Турции|30 крупнейших компаний Турции).*?(?=\n#|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        print("Error: Could not find companies section in Значимые турецкие события и персоналии.md")
        return
        
    section = match.group(0)
    
    # Parse table lines
    table_rows = []
    for line in section.splitlines():
        if line.strip().startswith("|") and not "Чистые продажи" in line and not "---" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                rank = parts[1]
                name = parts[2]
                sales = parts[3]
                table_rows.append((rank, name, sales))
                
    # Also parse continuation list: "15. Türkiye Kömür İşletmeleri Kurumu — 868,009,182"
    for line in section.splitlines():
        m = re.match(r"(\d+)\.\s*(.*?)\s*—\s*(.*)", line.strip())
        if m:
            rank = m.group(1)
            name = m.group(2)
            sales = m.group(3)
            if not any(r == rank for r, _, _ in table_rows):
                table_rows.append((rank, name, sales))
                
    # Generate HTML
    html = get_html_header("30 крупнейших компаний Турции", "companies")
    html += '  <h1 class="page-title">30 крупнейших компаний Турции</h1>\n'
    html += '  <div class="intro-text">Крупнейшие промышленные холдинги и предприятия Турецкой Республики по объемам чистых продаж. Рейтинг Türkiye’nin En Büyük Firmaları.</div>\n'
    
    html += '  <table class="premium-table">\n'
    html += '    <thead>\n'
    html += '      <tr>\n'
    html += '        <th style="width: 80px;">Место</th>\n'
    html += '        <th>Компания / Холдинг</th>\n'
    html += '        <th style="text-align: right;">Чистые продажи (TL)</th>\n'
    html += '      </tr>\n'
    html += '    </thead>\n'
    html += '    <tbody>\n'
    
    for rank, name, sales in sorted(table_rows, key=lambda x: int(x[0])):
        html += f'      <tr>\n'
        html += f'        <td><span class="rank-badge">{rank}</span></td>\n'
        html += f'        <td><strong>{name}</strong></td>\n'
        html += f'        <td style="text-align: right; font-weight: bold; font-family: \'PT Sans\', sans-serif;">{sales}</td>\n'
        html += f'      </tr>\n'
        
    html += '    </tbody>\n'
    html += '  </table>\n'
    
    html += get_html_footer()
    
    Path("companies.html").write_text(html, encoding="utf-8")
    print("✓ Created companies.html")

def compile_rich_families():
    events_file = Path("Значимые турецкие события и персоналии.md")
    if not events_file.exists():
        print(f"Error: {events_file} not found")
        return
        
    content = events_file.read_text(encoding="utf-8")
    
    # Extract the rich families section
    pattern = r"# (?:Türkiye’nin En Zengin 30 Kişi ve Ailesi|30 самых богатых людей и семей Турции).*?(?=\n#|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if not match:
        pattern = r"# 30 самых богатых людей и семей Турции.*?(?=\n#|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
    if not match:
        print("Error: Could not find rich families section in Значимые турецкие события и персоналии.md")
        return
        
    section = match.group(0)
    
    # Parse brackets and families
    brackets = []
    current_bracket = None
    
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("##"):
            bracket_name = line.replace("##", "").strip()
            current_bracket = {"name": bracket_name, "families": []}
            brackets.append(current_bracket)
        elif line and current_bracket and (re.match(r"\d+\.", line) or line.startswith("-")):
            m = re.match(r"(?:\d+\.|\-)\s*(.*?)(?:\s*—\s*(.*))?$", line)
            if m:
                name = m.group(1).strip()
                holding = m.group(2).strip() if m.group(2) else ""
                current_bracket["families"].append({
                    "num": len(current_bracket["families"]) + 1,
                    "name": name,
                    "holding": holding
                })
                
    # Re-index global numbers 1 to 30
    global_num = 1
    for b in brackets:
        for f in b["families"]:
            f["global_num"] = global_num
            global_num += 1
            
    # Generate HTML
    html = get_html_header("30 самых богатых людей и семей Турции", "rich_families")
    html += '  <h1 class="page-title">30 самых богатых людей и семей Турции</h1>\n'
    html += '  <div class="intro-text">Рейтинг крупнейших частных состояний и семейных кланов Турецкой Республики (по оценке финансово-экономических изданий).</div>\n'
    
    for b in brackets:
        if not b["families"]:
            continue
        html += f'  <div class="bracket-section">\n'
        html += f'    <h2 class="bracket-title">{b["name"]}</h2>\n'
        html += f'    <div class="cards-grid">\n'
        
        for f in b["families"]:
            html += f'      <div class="family-card">\n'
            html += f'        <div class="family-num">{f["global_num"]}</div>\n'
            html += f'        <div class="family-details">\n'
            html += f'          <div class="family-name">{f["name"]}</div>\n'
            if f["holding"]:
                html += f'          <div class="family-business">{f["holding"]}</div>\n'
            html += f'        </div>\n'
            html += f'      </div>\n'
            
        html += f'    </div>\n'
        html += f'  </div>\n'
        
    html += get_html_footer()
    
    Path("rich_families.html").write_text(html, encoding="utf-8")
    print("✓ Created rich_families.html")

def compile_actors():
    actors_file = Path("list_of_turkish_actors.md")
    if not actors_file.exists():
        print(f"Error: {actors_file} not found")
        return
        
    content = actors_file.read_text(encoding="utf-8")
    
    # 1. Extract Overview
    overview_text = ""
    overview_match = re.search(r"## Historical Overview(.*?)(?=\n# \w|\Z)", content, re.DOTALL)
    if overview_match:
        sect = overview_match.group(1)
        subs = re.split(r"###\s+", sect)
        for s in subs[1:]:
            lines = s.splitlines()
            sub_title = lines[0].strip()
            sub_body = "\n".join(lines[1:]).strip()
            paragraphs_html = ""
            for p in sub_body.split("\n\n"):
                p = p.strip()
                if p.startswith("-"):
                    paragraphs_html += "<ul>"
                    for li in p.split("\n"):
                        li_text = li.replace("-", "").strip()
                        paragraphs_html += f"<li>{li_text}</li>"
                    paragraphs_html += "</ul>"
                elif p:
                    p_clean = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", p)
                    p_clean = re.sub(r"\*(.*?)\*", r"<em>\1</em>", p_clean)
                    paragraphs_html += f"<p>{p_clean}</p>\n"
            overview_text += f'<div class="actor-block">\n  <h3 class="actor-era-title">{sub_title}</h3>\n  <div style="font-size: 16px; color: #333;">{paragraphs_html}</div>\n</div>\n'

    # Helper function to parse bio profiles for Male/Female actors
    def parse_actor_profiles(gender_header):
        block_html = ""
        pattern = rf"# {gender_header}(.*?)(?=\n# \w|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if not match:
            return ""
            
        gender_sec = match.group(1)
        eras = re.split(r"##\s+", gender_sec)
        for era in eras[1:]:
            lines = era.splitlines()
            era_title = lines[0].strip()
            era_body = "\n".join(lines[1:])
            
            block_html += f'<h3 class="actor-era-title">{era_title}</h3>\n'
            block_html += '<div class="actors-grid">\n'
            
            actors_sects = re.split(r"###\s+", era_body)
            for act_sect in actors_sects[1:]:
                act_lines = act_sect.splitlines()
                act_name = act_lines[0].strip()
                act_body = "\n".join(act_lines[1:]).strip()
                
                if act_name.startswith("|") or "Notable Productions" in act_name:
                    continue
                    
                bio_html = ""
                meta_html = "Yeşilçam / Modern"
                
                for p in act_body.split("\n\n"):
                    p = p.strip()
                    if p.startswith("|") or "Notable Productions" in p:
                        continue
                    if p:
                        if not bio_html and "(" in p and ")" in p:
                            meta_match = re.search(r"\((.*?)\)", p)
                            if meta_match:
                                meta_html = meta_match.group(1)
                        p_clean = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", p)
                        p_clean = re.sub(r"\*(.*?)\*", r"<em>\1</em>", p_clean)
                        bio_html += f"<p>{p_clean}</p>\n"
                
                block_html += f"""  <div class="actor-card">
    <div class="actor-name">{act_name}</div>
    <div class="actor-meta">{meta_html}</div>
    <div class="actor-bio">{bio_html}</div>
  </div>\n"""
            block_html += '</div>\n'
        return block_html

    # Parse Male and Female actors
    male_actors_html = parse_actor_profiles("Male Actors")
    female_actors_html = parse_actor_profiles("Female Actors")
    
    # Diaspora section
    diaspora_html = ""
    diaspora_match = re.search(r"# Turkish Actors in the Diaspora(.*?)(?=\n# \w|\Z)", content, re.DOTALL | re.IGNORECASE)
    if diaspora_match:
        diaspora_sec = diaspora_match.group(1)
        subs = re.split(r"##\s+", diaspora_sec)
        for s in subs[1:]:
            lines = s.splitlines()
            sub_title = lines[0].strip()
            sub_body = "\n".join(lines[1:]).strip()
            
            diaspora_html += f'<h3 class="actor-era-title">{sub_title}</h3>\n'
            diaspora_html += '<div class="actors-grid">\n'
            
            actors_sects = re.split(r"###\s+", sub_body)
            for act_sect in actors_sects[1:]:
                act_lines = act_sect.splitlines()
                act_name = act_lines[0].strip()
                act_body = "\n".join(act_lines[1:]).strip()
                if not act_name:
                    continue
                bio_html = ""
                meta_html = "Diaspora"
                for p in act_body.split("\n\n"):
                    p = p.strip()
                    if p.startswith("-"):
                        bio_html += "<ul>"
                        for li in p.split("\n"):
                            li_text = li.replace("-", "").strip()
                            bio_html += f"<li>{li_text}</li>"
                        bio_html += "</ul>"
                    elif p:
                        if not bio_html and "(" in p and ")" in p:
                            meta_match = re.search(r"\((.*?)\)", p)
                            if meta_match:
                                meta_html = meta_match.group(1)
                        p_clean = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", p)
                        p_clean = re.sub(r"\*(.*?)\*", r"<em>\1</em>", p_clean)
                        bio_html += f"<p>{p_clean}</p>\n"
                
                diaspora_html += f"""  <div class="actor-card">
    <div class="actor-name">{act_name}</div>
    <div class="actor-meta">{meta_html}</div>
    <div class="actor-bio">{bio_html}</div>
  </div>\n"""
            diaspora_html += '</div>\n'

    # Alphabetical List section
    alphabet_html = ""
    alphabet_match = re.search(r"# Turkish Actors List(.*?)$", content, re.DOTALL | re.IGNORECASE)
    if alphabet_match:
        alphabet_sec = alphabet_match.group(1)
        letters = re.split(r"##\s+", alphabet_sec)
        
        alphabet_html += '<div class="alphabet-columns">\n'
        for let in letters[1:]:
            lines = let.splitlines()
            letter = lines[0].strip()
            body = "\n".join(lines[1:]).strip()
            
            alphabet_html += f'  <div class="letter-group">\n'
            alphabet_html += f'    <div class="letter-title">{letter}</div>\n'
            alphabet_html += f'    <ul>\n'
            
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    act_name = line.replace("-", "").strip()
                    alphabet_html += f'      <li class="actors-list-item">{act_name}</li>\n'
            alphabet_html += f'    </ul>\n'
            alphabet_html += f'  </div>\n'
        alphabet_html += '</div>\n'

    # Assemble HTML page
    html = get_html_header("Список турецких актеров", "actors")
    html += '  <h1 class="page-title">Список турецких актеров</h1>\n'
    html += '  <div class="intro-text">История турецкого театра и кинематографа от зарождения в поздний османский период до триумфа золотого века Yeşilçam и современной мировой экспансии турецких сериалов (dizi).</div>\n'
    
    html += '  <h2 class="actor-section-title">Исторический очерк</h2>\n'
    html += overview_text
    
    html += '  <h2 class="actor-section-title">Легендарные актеры (Мужчины)</h2>\n'
    html += male_actors_html
    
    html += '  <h2 class="actor-section-title">Легендарные актрисы (Женщины)</h2>\n'
    html += female_actors_html
    
    if diaspora_html:
        html += '  <h2 class="actor-section-title">Турецкие актеры в диаспоре</h2>\n'
        html += diaspora_html
        
    if alphabet_html:
        html += '  <h2 class="actor-section-title">Алфавитный указатель актеров</h2>\n'
        html += alphabet_html
        
    html += get_html_footer()
    
    Path("actors.html").write_text(html, encoding="utf-8")
    print("✓ Created actors.html")

if __name__ == "__main__":
    compile_companies()
    compile_rich_families()
    compile_actors()
