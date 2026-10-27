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

## Domain und Zertifikat

Die Betreiberin hat den Kauf von `hippovex.de` bei INWX bestätigt. Öffentlich verifiziert: NS `ns.inwx.de`, `ns2.inwx.de`, `ns3.inwx.eu`; der A-Eintrag zeigte beim letzten Abruf noch auf `185.181.104.242`. Über den autoritativen Nameserver waren keine Web-AAAA- oder www-CNAME-Antworten vorhanden. Die angemeldete INWX-Verwaltung konnte wegen der gestoppten Browserbedienung nicht eingesehen oder verändert werden.

**Noch offen:** DNS-Ziele bei INWX ändern, Zertifikatsausstellung, Enforce HTTPS und Live-Prüfung der Custom Domain einschließlich www- und HTTP-Weiterleitungen. GitHub meldete direkt nach der Domainzuordnung `https_enforced: false`; die vorherige HTTPS-Prüfung der GitHub-Adresse bestätigt kein Zertifikat für `hippovex.de`.

Die Betreiberin erhielt die fünf minimal erforderlichen Website-Einträge. Details, zusätzliche optionale IPv6-Einträge und Quellen stehen in `DNS.md`. Eine optionale GitHub-Konto-Domainverifikation per TXT wurde noch nicht durchgeführt.
