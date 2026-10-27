# Veröffentlichungsstatus

Stand: 27.10.2026.

## GitHub-Veröffentlichung

- Repository: https://github.com/hofmann1304/hippovex-website (öffentlich).
- Initialer Website-PR #1 gemergt als `f110a9f98ebbf7f8f2eae1cf1c3e7baadaa697f4`.
- GitHub-Pages-Lauf [40483845117](https://github.com/hofmann1304/hippovex-website/actions/runs/40483845117): Build und Deployment erfolgreich für diesen Commit.
- Vor der Domainzuordnung lieferten elf Live-URLs über `https://hofmann1304.github.io/hippovex-website/` HTTP 200 mit gültiger HTTPS-Verbindung und dem erwarteten Quellinhalt: beide Startseiten, vier Rechtstextseiten, CSS, JavaScript, robots.txt, sitemap.xml und Logo.
- Anschließend Custom Domain `hippovex.de` erfolgreich über die GitHub-Pages-API gesetzt. GitHub erzeugte die `CNAME`-Datei im Commit `51b5aa0`.
- Kanonische URLs, Sprachverweise, Social-Metadaten, Sitemap und 404-Ziel sind auf `https://hippovex.de/` umgestellt.

## Lokal geprüft

- Deutsche und englische Startseite sowie Impressum und Datenschutz.
- HTML-Metadaten, genau eine Hauptüberschrift je Seite, lokale Links und Sprungmarken, gegenseitige Sprachverweise, JSON-LD und Sitemap.
- JavaScript-Syntax, CSS-Struktur und Git-Whitespace.
- Eigene Assets; keine Tracker, eingebetteten Fremdinhalte, externen Fonts oder Formulardienste.

## Visuelle und interaktive Einschränkung

Die automatisierte Browserprüfung auf diesem Windows-Rechner wurde vom Computer-Use-Werkzeug gestoppt: `browser URL policy enforcement is not yet supported for the current Windows browser`. Die erste In-App-Browser-Anfrage lief zuvor in ein Zeitlimit. Deshalb wurden Desktop-/Mobilansicht und tatsächliche Maus-/Tastaturinteraktionen nicht visuell abgenommen. Responsive Regeln und Bedienlogik sind implementiert; eine bestandene visuelle Prüfung wird nicht behauptet.

## Domain und Zertifikat: erfolgreich verifiziert

Abschlussprüfung am **27.10.2026 um 13:38 Uhr Europe/Berlin**:

- INWX: Hauptdomain mit allen vier GitHub-A-Adressen; `www` als CNAME auf `hofmann1304.github.io`. Autoritativer Nameserver und öffentlicher Resolver bestätigten die Ziele.
- GitHub Pages: `cname: hippovex.de`, `https_enforced: true`, Zertifikatsstatus `approved`. Hosting weiterhin `main`, `/`, Build-Typ `legacy` analog zu den beiden Referenzwebsites.
- Gültiges Let's-Encrypt-Zertifikat für **hippovex.de und www.hippovex.de**, TLS 1.3 bei den Prüfverbindungen, Gültigkeitsende 25.01.2027. GitHub verwaltet das Zertifikat.
- Elf HTTPS-URLs lieferten HTTP 200 und den erwarteten Quellinhalt: beide Sprach-Startseiten, vier Rechtstextseiten, CSS, JavaScript, robots.txt, sitemap.xml und Logo.
- HTTP-Hauptdomain leitet auf HTTPS um; HTTPS-www leitet auf die Hauptdomain um. HTTP-www führt über die HTTP-Hauptdomain ebenfalls zur HTTPS-Hauptdomain. Sprachpfade bleiben erhalten.
- Nicht vorhandene URL liefert HTTP 404 mit eigener Hippovex-Fehlerseite.
- Geprüfter Website-Quellstand: `9548a97455eaf3d063710ffdf9ebc1b4b274b33f`; zugehöriger erfolgreicher Pages-Lauf [40497533831](https://github.com/hofmann1304/hippovex-website/actions/runs/40497533831).
- Maschinenlesbarer Nachweis: [verification/live-check-2026-10-27.json](verification/live-check-2026-10-27.json). Wiederholbar mit `python scripts/check_live.py`.

Nach der DNS-Umstellung war zunächst noch kein passendes Zertifikat verfügbar. Die Domain wurde entsprechend GitHubs dokumentiertem Verfahren einmal entfernt und wieder hinzugefügt. Daraufhin wurde das Zertifikat für beide Namen ausgestellt. Nach Aktivierung von Enforce HTTPS wurde die Website erneut bereitgestellt und die Weiterleitungskette geprüft. Alle beschriebenen technischen Abschlussprüfungen bestehen.

Die optionale GitHub-Konto-Domainverifikation per TXT wurde nicht durchgeführt; sie ist von der erfolgreichen DNS-, TLS- und Live-Verifikation zu unterscheiden. Die visuelle Browserabnahme bleibt wegen der oben beschriebenen Werkzeuggrenze offen. Weder App-Produktionsreife noch eine rechtliche Abnahme werden aus diesen Website-Prüfungen abgeleitet.
