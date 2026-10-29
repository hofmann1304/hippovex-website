# Hippovex Website

Öffentliche Informationswebsite zur Hippovex-App in Entwicklung. Deutsche und englische Startseite, illustrative Produktansicht mit fiktiven Daten, Beta-/Kontaktformular, Impressum, Datenschutz und eigene 404-Seite. Kein App-Download, keine Konto- oder Newsletter-Anmeldung, keine Käufe und kein Tracking.

Gestaltung seit dem bestätigten Entwurf vom 27.10.2026: Kombination aus ruhiger Editorial-Gestaltung und heller Produktansicht. Warme Papierflächen, lokale Georgia-Serifenschrift, blaue Akzente, offene Funktionsabschnitte und eine Smartphone-Illustration mit den Ansichten „Heute“ und „Training“. Die Rechtstextseiten verwenden dieselbe Gestaltung; deren Inhalte bleiben erhalten.

## Architektur

Analog zu `hofmann1304/sarahofmann-website` und `hofmann1304/robutrace-website`:

- Öffentlicher GitHub-Quellcode, statisches HTML/CSS/JavaScript ohne Paketinstallation.
- GitHub Pages veröffentlicht den Branch `main`, Verzeichnis `/`.
- `.nojekyll` verhindert unnötige Jekyll-Verarbeitung.
- Jeder Push auf `main` löst die GitHub-Pages-Veröffentlichung aus.
- Registrar/DNS: **INWX**, laut Betreiberin am 27.10.2026 gekauft. Kein IONOS-Hosting.
- Live-Adresse: **https://hippovex.de/**. Custom Domain, Zertifikat für Hauptdomain und `www`, HTTPS-Erzwingung und Weiterleitungen wurden erfolgreich geprüft.
- Die vorherige Projektadresse https://hofmann1304.github.io/hippovex-website/ wird nach der Domainzuordnung auf die Custom Domain umgeleitet. Solange DNS nicht umgestellt ist, ist dies keine unabhängig nutzbare Ersatzadresse.

## Lokal ansehen und prüfen

```powershell
python -m http.server 8765 --bind 127.0.0.1
python scripts/check_site.py
python scripts/check_live.py
node --check site.js
node --check contact.js
node --test scripts/contact.test.cjs
git diff --check
```

Danach http://127.0.0.1:8765/ öffnen. Mobilmenü und Produkt-Tabs sind mit Tastatur bedienbar; die Tab-Auswahl unterstützt Pfeiltasten, Pos1 und Ende. Ohne JavaScript bleiben Navigation und erste Produktansicht zugänglich.

## Änderungen veröffentlichen

Website-Dateien bearbeiten, lokal prüfen, committen und auf `main` pushen. Größere Änderungen über einen Branch und Pull Request prüfen. Danach den Pages-Lauf für den exakten Commit und die betroffenen Live-URLs kontrollieren.

## Quellen und inhaltliche Grenzen

Die Funktionen und Grenzen wurden am 27.10.2026 anhand der lokalen Hippovex-Dokumentation `README.md`, `docs/BRANDING.md` und `docs/VALIDATION.md` abgeglichen. Das App-Logo ist die vorhandene, unveränderte Hippovex-Marke. App-Quellcode, APKs, Originalkataloge und private Nutzerdaten sind nicht Bestandteil dieses öffentlichen Repositorys. Betreiberangaben stammen aus dem bestehenden Impressum von sarahofmann.de und wurden von der Betreiberin für Hippovex bestätigt.

Die dargestellte Produktansicht ist eine als solche gekennzeichnete Illustration mit fiktiven Daten, kein App-Screenshot. Keine Behauptung einer veröffentlichten oder auf echten Geräten abgenommenen App. Website-Prüfungen bestätigen keine medizinische, rechtliche oder native App-Abnahme.

## Beta- und Kontaktformular

Das Formular sendet per POST an den bereits auf sarahofmann.de eingesetzten Form.taxi-Anschluss `https://form.taxi/s/3retq47d`. Hippovex-Sendungen sind durch einen eigenen Betreff, das Feld `Website` und das gewählte Anliegen erkennbar. Es wurde kein neuer Anbieteraccount angelegt und keine Einstellung der anderen Websites verändert.

Mit JavaScript erfolgen Versand und Rückmeldung innerhalb der Seite. Erfolg wird ausschließlich nach HTTP-Erfolg und der ausdrücklichen JSON-Bestätigung `success: true` angezeigt. Bei Fehlern bleiben die Angaben erhalten; keine automatischen Wiederholungen. Ohne JavaScript übernimmt der Formulardienst die Weiterleitung auf `danke.html` bzw. `en/danke.html`. E-Mail ist die einzige erforderliche Kontaktangabe; Name, Gerät und Nachricht sind optional. Beta-Anfragen garantieren keinen Platz und sind keine Newsletter-Anmeldung.

Die neun isolierten Tests des Formularablaufs versenden keine Nachrichten. Sie bestätigen keine Zustellung in ein echtes Postfach. Die empfangsseitige Zustellung, mögliche Domainfreigaben und der bestehende Vertrag zur Auftragsverarbeitung wurden nicht aus dem öffentlich lesbaren Formularcode abgeleitet. Die Anbieteranbindung folgt dessen [JavaScript-Dokumentation](https://docs.form.taxi/de/javascript); Datenschutzinformationen wurden entsprechend der [Anbieterinformation](https://docs.form.taxi/de/privacy) ergänzt.

Domain-/DNS-Schritte und Primärquellen: [DNS.md](DNS.md). Veröffentlichungsnachweis: [RELEASE.md](RELEASE.md).
