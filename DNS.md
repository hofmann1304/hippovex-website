# hippovex.de bei INWX mit GitHub Pages verbinden

Zuständigkeiten: INWX = Registrierung und DNS, GitHub Pages = Website und TLS-Zertifikat. Kein zusätzliches Webhosting und kein separat gekauftes SSL-Zertifikat erforderlich.

INWX-Bedienpfad laut Anbieter: Kundenbereich → Nameserver → `hippovex.de` suchen → Augensymbol → DNS-Einträge hinzufügen bzw. vorhandene Website-Einträge bearbeiten.

## Reihenfolge

1. Repository veröffentlichen und GitHub Pages aktivieren (`main`, `/`).
2. Optional empfohlen: GitHub-Kontoeinstellungen → Pages → Add a domain → `hippovex.de`. Den dort tatsächlich erzeugten TXT-Wert bei INWX eintragen, dann Verify anklicken. Ein Wert darf nicht erfunden werden. TXT dauerhaft behalten.
3. In den Pages-Einstellungen des Repositorys die Custom Domain `hippovex.de` setzen; passende `CNAME`-Datei im Repository behalten. Die Domain auf GitHub vor der DNS-Zielumschaltung zuordnen.
4. In der bestehenden INWX-DNS-Zone ausschließlich die nachstehenden Website-Einträge setzen. Bereits vorhandene Werte zuerst prüfen. MX-, Mail-, SPF-, DKIM-, DMARC-, NS- und andere unabhängige TXT-Einträge erhalten.
5. Nach DNS-Propagation das automatisch von GitHub ausgestellte Zertifikat abwarten. Erst dann `Enforce HTTPS` aktivieren und beide Hostnamen sowie HTTP-Weiterleitungen prüfen.

## Website-Einträge

In INWX steht ein leerer Name typischerweise für die Hauptdomain; falls die Oberfläche `@` verwendet, dieses verwenden. Bei vollständig qualifiziertem Namen ist das Ziel entsprechend `hippovex.de.` bzw. `www.hippovex.de.`. TTL 3600 ist geeignet. IPv6 ist optional; bei Nutzung alle vier AAAA-Einträge setzen und keine alten Web-AAAA-Werte stehen lassen.

| Name | Typ | Wert |
| --- | --- | --- |
| Hauptdomain / leer / `@` | A | `185.199.108.153` |
| Hauptdomain / leer / `@` | A | `185.199.109.153` |
| Hauptdomain / leer / `@` | A | `185.199.110.153` |
| Hauptdomain / leer / `@` | A | `185.199.111.153` |
| Hauptdomain / leer / `@` | AAAA | `2606:50c0:8000::153` |
| Hauptdomain / leer / `@` | AAAA | `2606:50c0:8001::153` |
| Hauptdomain / leer / `@` | AAAA | `2606:50c0:8002::153` |
| Hauptdomain / leer / `@` | AAAA | `2606:50c0:8003::153` |
| `www` | CNAME | `hofmann1304.github.io.` |

Keine Wildcard-Ziele einrichten. `www` darf nicht gleichzeitig andere A-/AAAA-/CNAME-Ziele haben. Kein URL-Redirect-/Webforwarding-Produkt verwenden. Bei bestehenden CAA-Regeln muss Let's Encrypt berechtigt sein; die ursprüngliche Zone vor einer Änderung prüfen.

Der optionale Verifikations-TXT hat den Namen `_github-pages-challenge-hofmann1304`. Der Inhalt kommt ausschließlich aus den GitHub-Kontoeinstellungen.

Eine BIND-kompatible Vorlage mit ausschließlich den neun Website-Einträgen liegt in `dns/hippovex-web-records.zone`. Diese ist **keine vollständige Zone** und darf nicht zum ungeprüften Ersetzen der gesamten INWX-Zone benutzt werden.

## Abschlussprüfung unter Windows

```powershell
Resolve-DnsName hippovex.de -Type A
Resolve-DnsName hippovex.de -Type AAAA
Resolve-DnsName www.hippovex.de -Type CNAME
gh api repos/hofmann1304/hippovex-website/pages
```

Danach `https://hippovex.de/`, `/en/`, die Rechtstexte, `sitemap.xml`, `robots.txt`, HTTPS auf `www` und HTTP→HTTPS prüfen. Ein erfolgreicher Pages-Build allein bestätigt weder DNS noch Zertifikat. DNS-Caches können laut GitHub bis zu 24 Stunden benötigen.

## Primärquellen, geprüft am 27.10.2026

- [GitHub: Custom Domain und aktuelle DNS-Ziele](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub: HTTPS und Zertifikatsbereitstellung](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [GitHub: Domain-Verifizierung und TXT](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [GitHub: Pages und protokollierte IP-Adressen](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)
- [GitHub-Datenschutzerklärung](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)
- [Google-Datenschutzerklärung für E-Mail-Kontakt](https://policies.google.com/privacy?hl=de)
- [§ 5 DDG](https://www.gesetze-im-internet.de/ddg/__5.html)
- [DSGVO](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [INWX: DNS-Verwaltung](https://www.inwx.de/de/blog/was-ist-ein-dns-eintrag)
- [INWX: CNAME anlegen](https://kb.inwx.com/en-us/3-nameserver/111-how-do-i-create-a-cname-record)
- [INWX: TXT anlegen](https://kb.inwx.com/en-us/3-nameserver/107-how-can-i-create-a-txt-record)
