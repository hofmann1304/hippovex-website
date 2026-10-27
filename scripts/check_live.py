from pathlib import Path
from urllib.request import urlopen, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError
import ssl, socket, json, datetime
ROOT=Path(__file__).resolve().parents[1]
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':[],'tls':[],'redirects':[]}
for host in ['hippovex.de','www.hippovex.de']:
    try:
        with socket.create_connection((host,443),timeout=15) as s:
            with ssl.create_default_context().wrap_socket(s,server_hostname=host) as t:
                c=t.getpeercert()
                report['tls'].append({'host':host,'valid':True,'TLS':t.version(),'SAN':c.get('subjectAltName'),'notBefore':c.get('notBefore'),'notAfter':c.get('notAfter'),'issuer':c.get('issuer')})
    except Exception as e: report['tls'].append({'host':host,'valid':False,'error':str(e)})
for rel in ['','en/','impressum.html','datenschutz.html','en/impressum.html','en/datenschutz.html','styles.css','site.js','robots.txt','sitemap.xml','assets/hippovex-logo.png']:
    try:
        with urlopen('https://hippovex.de/'+rel,timeout=15) as r: data=r.read(); status=r.status; url=r.url
        local=(ROOT/(rel+'index.html' if rel in ['','en/'] else rel)).read_bytes()
        report['pages'].append({'path':rel,'status':status,'url':url,'matches_source':data.replace(b'\r\n',b'\n')==local.replace(b'\r\n',b'\n')})
    except Exception as e: report['pages'].append({'path':rel,'error':str(e)})
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None
opener=build_opener(NoRedirect)
for url,expected in [('http://hippovex.de/','https://hippovex.de/'),('http://www.hippovex.de/','https://hippovex.de/'),('https://www.hippovex.de/','https://hippovex.de/'),('http://hippovex.de/en/','https://hippovex.de/en/'),('https://www.hippovex.de/en/','https://hippovex.de/en/')]:
    try:
        try: r=opener.open(url,timeout=15)
        except HTTPError as e: r=e
        location=r.headers.get('Location')
        with urlopen(url,timeout=15) as final: final_url=final.url; final_status=final.status
        ok=r.status in (301,302,307,308) and bool(location) and final_url==expected and final_status==200
        report['redirects'].append({'url':url,'status':r.status,'location':location,'final_url':final_url,'final_status':final_status,'ok':ok})
    except Exception as e: report['redirects'].append({'url':url,'error':str(e),'ok':False})
try:
    urlopen('https://hippovex.de/not-a-real-page-qa/',timeout=15)
    report['404']={'ok':False}
except HTTPError as e:
    report['404']={'status':e.code,'custom_page':'Hier geht es nicht weiter.' in e.read().decode()}
except Exception as e: report['404']={'error':str(e)}
report['passed']=all(x.get('valid') for x in report['tls']) and all(x.get('status')==200 and x.get('matches_source') for x in report['pages']) and all(x.get('ok') for x in report['redirects']) and report['404'].get('status')==404 and report['404'].get('custom_page')
out=ROOT/'verification'; out.mkdir(exist_ok=True)
(out/'live-check-2026-10-27.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'passed':report['passed'],'TLS':report['tls'],'redirects':report['redirects'],'pages_ok':sum(x.get('status')==200 and x.get('matches_source',False) for x in report['pages']),'404':report['404']},indent=2,ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
