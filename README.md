# Hippovex Website

Öffentliche Informationswebsite zur Hippovex-App in Entwicklung. Deutsche und englische Startseite, illustrative Produktansicht mit fiktiven Daten, Kontakt per E-Mail, Impressum, Datenschutz und eigene 404-Seite. Kein App-Download, keine Anmeldung, keine Käufe und kein Tracking.

## Architektur

Analog zu `hofmann1304/sarahofmann-website` und `hofmann1304/robutrace-website`:

- Öffentlicher GitHub-Quellcode, statisches HTML/CSS/JavaScript ohne Paketinstallation.
- GitHub Pages veröffentlicht den Branch `main`, Verzeichnis `/`.
- `.nojekyll` verhindert unnötige Jekyll-Verarbeitung.
- Jeder Push auf `main` löst die GitHub-Pages-Veröffentlichung aus.
- Registrar/DNS: **INWX**, laut Betreiberin am 27.10.2026 gekauft. Kein IONOS-Hosting.
- Zieladresse: **https://hippovex.de/**, mit Weiterleitung von `www` und erzwungenem HTTPS nach Zertifikatsausstellung.
- Die vorherige Projektadresse https://hofmann1304.github.io/hippovex-website/ wird nach der Domainzuordnung auf die Custom Domain umgeleitet. Solange DNS nicht umgestellt ist, ist dies keine unabhängig nutzbare Ersatzadresse.

## Lokal ansehen und prüfen

```powershell
python -m http.server 8765 --bind 127.0.0.1
python scripts/check_site.py
node --check site.js
git diff --check
```

Danach http://127.0.0.1:8765/ öffnen. Mobilmenü und Produkt-Tabs sind mit Tastatur bedienbar; die Tab-Auswahl unterstützt Pfeiltasten, Pos1 und Ende. Ohne JavaScript bleiben Navigation und erste Produktansicht zugänglich.

## Änderungen veröffentlichen

Website-Dateien bearbeiten, lokal prüfen, committen und auf `main` pushen. Größere Änderungen über einen Branch und Pull Request prüfen. Danach den Pages-Lauf für den exakten Commit und die betroffenen Live-URLs kontrollieren.

## Quellen und inhaltliche Grenzen

Die Funktionen und Grenzen wurden am 27.10.2026 anhand der lokalen Hippovex-Dokumentation `README.md`, `docs/BRANDING.md` und `docs/VALIDATION.md` abgeglichen. Das App-Logo ist die vorhandene, unveränderte Hippovex-Marke. App-Quellcode, APKs, Originalkataloge und private Nutzerdaten sind nicht Bestandteil dieses öffentlichen Repositorys. Betreiberangaben stammen aus dem bestehenden Impressum von sarahofmann.de und wurden von der Betreiberin für Hippovex bestätigt.

Die dargestellte Produktansicht ist eine als solche gekennzeichnete Illustration mit fiktiven Daten, kein App-Screenshot. Keine Behauptung einer veröffentlichten oder auf echten Geräten abgenommenen App. Website-Prüfungen bestätigen keine medizinische, rechtliche oder native App-Abnahme.

Domain-/DNS-Schritte und Primärquellen: [DNS.md](DNS.md). Veröffentlichungsnachweis: [RELEASE.md](RELEASE.md).
