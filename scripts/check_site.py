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
        self.forms=[]; self.current_form=None; self.labels=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='label' and a.get('for'): self.labels.add(a['for'])
        if tag=='form':
            self.current_form={'attrs':a,'controls':{}}
            self.forms.append(self.current_form)
        if tag in ['input','select','textarea'] and self.current_form is not None:
            self.current_form['controls'][a.get('name')]=a
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
        if tag=='form': self.current_form=None
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
for rel in ['index.html','en/index.html']:
    path=ROOT/rel; doc=docs[path.resolve()]; en=rel.startswith('en/')
    if len(doc.forms)!=1:
        ERRORS.append(rel+': expected one contact form'); continue
    form=doc.forms[0]; controls=form['controls']; attrs=form['attrs']
    if attrs.get('method','').lower()!='post' or attrs.get('action')!='https://form.taxi/s/3retq47d':
        ERRORS.append(rel+': form delivery endpoint')
    expected_next=BASE+('en/' if en else '')+'danke.html'
    if controls.get('_next',{}).get('value')!=expected_next: ERRORS.append(rel+': confirmation URL')
    if controls.get('_lang',{}).get('value')!=('en' if en else 'de'): ERRORS.append(rel+': form language')
    email=controls.get('email',{})
    if email.get('type')!='email' or 'required' not in email: ERRORS.append(rel+': required email')
    for name in ['Name','Gerät','Nachricht']:
        if name not in controls or 'required' in controls[name]: ERRORS.append(rel+': optional '+name)
    for name,control in controls.items():
        if control.get('type')!='hidden' and control.get('id') not in doc.labels:
            ERRORS.append(rel+': missing control label '+str(name))
    if controls.get('_gotcha',{}).get('tabindex')!='-1': ERRORS.append(rel+': honeypot keyboard access')
    if not controls.get('_subject',{}).get('value','').startswith('Hippovex'): ERRORS.append(rel+': form subject')
    if any(url.startswith('mailto:') for url in doc.links): ERRORS.append(rel+': marketing mailto link')
    if 'Schreib Sara' in path.read_text(encoding='utf-8') or 'Email Sara' in path.read_text(encoding='utf-8'):
        ERRORS.append(rel+': personal contact copy')
for file in ['.nojekyll','assets/hippovex-logo.png','site.js','contact.js','robots.txt','danke.html','en/danke.html']:
    if not (ROOT/file).exists(): ERRORS.append('missing '+file)
if ERRORS:
    print('\n'.join(ERRORS)); raise SystemExit(1)
print(f'PASS: {len(docs)} HTML pages; links, metadata, languages, structured data, sitemap, assets and bilingual contact form contracts.')
