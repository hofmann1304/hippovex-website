"""Dependency-free static release checks. Run from any directory."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://hippovex.de/'
ERRORS = []

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=set(); self.links=[]; self.canonical=[]; self.alternates={}; self.h1=0
        self.lang=None; self.description=False; self.jsons=[]; self.json_current=None; self.title=False
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: ERRORS.append('duplicate id '+a['id'])
            self.ids.add(a['id'])
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if tag=='title': self.title=True
        if tag=='meta' and a.get('name')=='description': self.description=bool(a.get('content'))
        if tag=='script' and a.get('type')=='application/ld+json': self.json_current=''
        for key in ['href','src']:
            if key in a: self.links.append(a[key])
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
        if tag=='link' and a.get('rel')=='alternate': self.alternates[a.get('hreflang')]=a.get('href')
        if tag=='img' and 'alt' not in a: ERRORS.append('image without alt')
    def handle_data(self,data):
        if self.json_current is not None: self.json_current+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.json_current is not None:
            self.jsons.append(json.loads(self.json_current)); self.json_current=None

docs={}
for path in ROOT.rglob('*.html'):
    doc=Document(); doc.feed(path.read_text(encoding='utf-8')); docs[path.resolve()]=doc
    if not doc.lang or doc.h1!=1 or not doc.title: ERRORS.append(f'{path.name}: lang/title/h1')
    if path.name!='404.html':
        rel=path.relative_to(ROOT).as_posix().replace('index.html','')
        if doc.canonical != [BASE+rel]: ERRORS.append(f'{rel}: canonical')
        if set(doc.alternates)!={'de','en','x-default'}: ERRORS.append(f'{rel}: hreflang')
        if not doc.description: ERRORS.append(f'{rel}: description')
for path,doc in docs.items():
    for link in doc.links:
        parsed=urlparse(link)
        if parsed.scheme in ['mailto','tel']: continue
        if parsed.scheme:
            if parsed.scheme!='https': ERRORS.append(f'{path.name}: insecure URL {link}')
            if not link.startswith(BASE): continue
            relative=parsed.path.removeprefix(urlparse(BASE).path)
            target=ROOT/relative
        else:
            target=path.parent/unquote(parsed.path) if parsed.path else path
        if target.is_dir(): target=target/'index.html'
        target=target.resolve()
        if not target.exists(): ERRORS.append(f'{path.relative_to(ROOT)}: missing {link}')
        elif parsed.fragment and target in docs and unquote(parsed.fragment) not in docs[target].ids:
            ERRORS.append(f'{path.relative_to(ROOT)}: missing anchor {link}')
    for lang,url in doc.alternates.items():
        target=ROOT/url.removeprefix(BASE)
        if target.is_dir(): target=target/'index.html'
        other=docs.get(target.resolve())
        if not other or other.alternates!=doc.alternates: ERRORS.append(f'{path.name}: reciprocal hreflang')
tree=ET.parse(ROOT/'sitemap.xml')
for loc in tree.findall('.//{*}loc'):
    target=ROOT/loc.text.removeprefix(BASE)
    if target.is_dir(): target=target/'index.html'
    if not target.exists(): ERRORS.append('sitemap: '+loc.text)
css=(ROOT/'styles.css').read_text(encoding='utf-8')
if css.count('{')!=css.count('}'): ERRORS.append('CSS brace count')
for file in ['.nojekyll','assets/hippovex-logo.png','site.js','robots.txt']:
    if not (ROOT/file).exists(): ERRORS.append('missing '+file)
if ERRORS:
    print('\n'.join(ERRORS)); raise SystemExit(1)
print(f'PASS: {len(docs)} HTML pages; local links/anchors, metadata, reciprocal languages, structured data, sitemap, CSS and assets.')
