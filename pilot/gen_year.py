import re, html, sys
src = open('1985_pilot.md').read()

PHOTOS = {
  'Болгарские турки': [
    ('img/1985/1985_bolgarskie-turki_01.jpg', 'Турецкие беженцы из Болгарии. Снимок из «Türkiye Cumhuriyeti Tarihi».', 'wide'),
    ('img/1985/1985_bolgarskie-turki_02.jpg', 'Четыре года спустя: изгнанные турки на пограничной станции, 1989 (см. «Исход болгарских турок», 1989).', 'tall'),
  ],
  'Мост': [
    ('img/1985/1985_most_01.jpg', 'Стройка второго Босфорского моста: пилоны уже стоят, пролёта ещё нет. Снимок из «Türkiye Cumhuriyeti Tarihi».', 'wide'),
  ],
}

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\(см\. ([^)]+)\)', r'<span class="see">(см. \1)</span>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t

def slug(s):
    return re.sub(r'[^\w]+', '-', s.lower()).strip('-')

parts = re.split(r'\n## ', src)
arts, chron = [], ''
for p in parts[1:]:
    title, body = p.split('\n', 1)
    body = body.strip().strip('-').strip()
    if title.startswith('Хронология'):
        chron = body
        continue
    paras = [x.strip() for x in body.split('\n\n') if x.strip() and x.strip() != '---']
    lead = paras[0].strip('*')
    brief = ''
    rest = []
    for x in paras[1:]:
        if x.startswith('*Фото:'):
            brief = x.strip('*').replace('Фото:', '').strip()
        else:
            rest.append(x)
    arts.append((title, lead, rest, brief))

out = []
toc = ''.join(f'<li><a href="#{slug(t)}"><span class="n">{i+1:02d}</span>{html.escape(t)}</a></li>' for i, (t, *_ ) in enumerate(arts))
out.append(f'''<header class="cover">
  <div class="cover-top"><span>Намедни · Türkiye</span><span>Пилотный год</span></div>
  <h1 class="year" aria-label="1985">1985</h1>
  <p class="cover-lede">Чеки в коробке, три недели снежных каникул, болгарские паспорта с чужими именами, партия, которой руководит жена, и воскресенье, когда вся страна сидит дома и ждёт счётчика.</p>
  <ol class="toc">{toc}</ol>
</header>''')

for i, (t, lead, rest, brief) in enumerate(arts):
    photos = PHOTOS.get(t, [])
    side = 'left' if i % 2 == 0 else 'right'
    if photos:
        figs = ''.join(
            f'<figure class="ph {cls}"><img src="{src}" alt="{html.escape(cap)}" loading="lazy"><span class="tag">ч/б · к колоризации</span><figcaption>{inline(cap)}</figcaption></figure>'
            for src, cap, cls in photos)
        media = f'<div class="media">{figs}</div>'
    else:
        media = f'<div class="media"><div class="brief"><span class="brief-k">Фото в поиске</span><p>{inline(brief)}</p></div></div>'
    body = ''.join(f'<p>{inline(x)}</p>' for x in rest)
    out.append(f'''<article class="spread {side}" id="{slug(t)}">
  {media}
  <div class="text">
    <div class="kicker"><span class="n">{i+1:02d}</span><span>1985</span></div>
    <h2>{html.escape(t)}</h2>
    <p class="lead">{inline(lead)}</p>
    <div class="body">{body}</div>
  </div>
</article>''')

# chronology
months = re.split(r'\n?\*\*(.+?)\*\*\n', '\n' + chron)
cm = ''
src_note = ''
for j in range(1, len(months), 2):
    m = months[j]
    items = [l[2:] for l in months[j+1].split('\n') if l.startswith('- ')]
    tail = [l for l in months[j+1].split('\n') if l.startswith('*Источники')]
    if tail: src_note = tail[0].strip('*')
    lis = ''
    for it in items:
        d, _, txt = it.partition(' — ')
        lis += f'<li><time>{html.escape(d)}</time><span>{inline(txt)}</span></li>'
    cm += f'<section class="month"><h3>{html.escape(m)}</h3><ul>{lis}</ul></section>'
out.append(f'''<section class="chron" id="chron">
  <div class="chron-head"><h2>Хронология 1985</h2><p>По «Türkiye Cumhuriyeti Tarihi» и Almanak Türkiye.</p></div>
  <div class="months">{cm}</div>
  <p class="sources">{html.escape(src_note)}</p>
</section>''')

BODY = '\n'.join(out)
CSS = open('style.css').read()
HEAD = '<title>Намедни. 1985</title>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;800;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Sans+Condensed:wght@400;600&display=swap">\n'
page = HEAD + f'<style>{CSS}</style>\n<div class="wrap">\n{BODY}\n</div>\n'
open('artifact_1985.html', 'w').write(page)
full = '<!doctype html>\n<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n' + HEAD + f'<style>{CSS}</style></head>\n<body><div class="wrap">\n{BODY}\n</div></body></html>\n'
open('1985_pilot.html', 'w').write(full)
print(len(arts), 'spreads')
