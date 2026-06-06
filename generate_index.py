#!/usr/bin/env python3
import json
from pathlib import Path

def generate_index():
    script_dir = Path(__file__).parent
    parsed_json_path = Path("/Users/mac2021/.gemini/antigravity-ide/brain/8fcd98a0-e21e-462d-83ae-12b46302a0e4/scratch/parsed_years.json")
    
    if not parsed_json_path.exists():
        print(f"Error: {parsed_json_path} does not exist. Run parse_years.py first.")
        return
        
    with open(parsed_json_path, "r", encoding="utf-8") as f:
        years_data = json.load(f)
        
    # Sort years in ascending order
    sorted_years = sorted([int(y) for y in years_data.keys()])
    
    # Generate year blocks
    grid_html = ""
    for year in sorted_years:
        year_str = str(year)
        data = years_data[year_str]
        filename = data["file"]
        phenomena = data["phenomena"]
        
        # Build phenomena links
        links_html = []
        for item in phenomena:
            title = item["title"]
            anchor = item["anchor"]
            # Link to the year's html file with the anchor
            links_html.append(f'<a href="{filename}{anchor}">{title}</a>')
            
        # Join with bullet separator
        bullets_sep = ' <span class="bullet">•</span> '
        phenomena_list_str = bullets_sep.join(links_html)
        
        grid_html += f"""
      <div class="year-block">
        <div class="year-label">{year}</div>
        <div class="phenomena-list">
          {phenomena_list_str}
        </div>
      </div>"""

    # Build full HTML
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Намедни по-турецки — Феномены по годам</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=PT+Sans:wght@400;700&display=swap');

  :root {{
    --dark-blue: #070c24;
    --dark-red: #800c14;
    --gold: #b8860b;
    --text-color: #1a1a1a;
    --link-color: #1a548c;
    --bullet-color: #999999;
    --bg-cream: #faf9f6;
  }}

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    background-color: #ffffff;
    color: var(--text-color);
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
  }}

  /* ======= HEADER GRADIENT WITH COLLAGE ======= */
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
  }}

  .nav-item:hover {{
    color: #ffffff;
  }}

  .nav-item.active {{
    color: #ffffff;
    border-bottom-color: #ffffff;
  }}

  /* ======= Stylized NTV Flower Logo Badge ======= */
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

  /* Beautiful CSS NTV spoked asterisk */
  .ntv-asterisk {{
    color: #a3cc29; /* Lime green / yellow NTV flower color */
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
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #111111;
    margin-bottom: 40px;
    letter-spacing: -0.5px;
  }}

  /* ======= YEARS GRID ======= */
  .years-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 60px;
    row-gap: 35px;
  }}

  .year-block {{
    display: flex;
    align-items: flex-start;
    padding: 5px 0;
    transition: background-color 0.2s ease, transform 0.2s ease;
    border-radius: 4px;
  }}

  .year-block:hover {{
    background-color: #f7f9fc;
    transform: translateX(5px);
  }}

  /* Rotated Year text */
  .year-label {{
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--link-color);
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    line-height: 1;
    padding-top: 2px;
    margin-right: 18px;
    flex-shrink: 0;
    user-select: none;
    transition: color 0.2s ease;
  }}

  .year-block:hover .year-label {{
    color: #e02424; /* Red highlight on hover matching Namedni theme */
  }}

  /* Phenomena text list */
  .phenomena-list {{
    font-family: 'PT Sans', Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    color: #333333;
    padding-top: 2px;
  }}

  .phenomena-list a {{
    color: var(--link-color);
    text-decoration: none;
    font-weight: 400;
    transition: color 0.15s, border-bottom 0.15s;
    border-bottom: 1px solid transparent;
  }}

  .phenomena-list a:hover {{
    color: #0b2e59;
    border-bottom-color: #0b2e59;
  }}

  .bullet {{
    color: var(--bullet-color);
    margin: 0 4px;
    font-weight: bold;
    user-select: none;
  }}

  /* ======= FOOTER ======= */
  footer {{
    background-color: #111111;
    color: #777777;
    text-align: center;
    padding: 30px 40px;
    font-size: 12px;
    border-top: 1px solid #222;
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
    .years-grid {{
      grid-template-columns: 1fr;
      row-gap: 30px;
    }}
    header {{
      padding: 20px 20px 0 20px;
    }}
    main {{
      padding: 0 20px;
      margin: 30px auto 60px;
    }}
  }}

  @media (max-width: 500px) {{
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
        <a href="index.html" class="nav-item active">Феномены по годам</a>
        <a href="companies.html" class="nav-item">30 крупнейших компаний Турции</a>
        <a href="rich_families.html" class="nav-item">30 самых богатых людей и семей Турции</a>
        <a href="actors.html" class="nav-item">Список турецких актеров</a>
      </nav>
    </div>
    <div class="ntv-badge-container">
      <div class="ntv-badge" title="Намедни / НТВ">
        <span class="ntv-asterisk">✳</span>
      </div>
    </div>
  </div>
</header>

<main>
  <h1 class="page-title">Феномены по годам</h1>
  
  <div class="years-grid">
    {grid_html}
  </div>
</main>

<footer>
  <p>© Намедни. Наша Эра · Леонид Парфенов. Турция: 1942, 1980–1991.</p>
</footer>

</body>
</html>
"""
    
    index_file = script_dir / "index.html"
    index_file.write_text(html_content, encoding="utf-8")
    print(f"✓ Created landing page: {index_file.name}")

if __name__ == "__main__":
    generate_index()
