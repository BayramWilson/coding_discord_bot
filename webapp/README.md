# 🌐 WebApp – Mini IDE für Coding Challenges

Diese WebApp ist Teil des Gesamtprojekts **Coder Discord Bot**.  
Sie stellt eine kleine browserbasierte Umgebung bereit, in der Nutzer ihre Python-Lösungen schreiben, testen und absenden können – passend zu den vom Bot generierten Coding Challenges.

---

## 🛠️ Features

- 💡 Anzeige einer einzelnen Coding Challenge per URL (`/challenge/<id>`)
- 🧑‍💻 Code-Editor im Browser (CodeMirror-basiert)
- 🚀 Button zum Absenden des Codes
- ✅ Rückmeldung über Erfolg oder Fehler direkt im Browser
- 🔗 Optional: Integration mit Discord Bot (`!challenge` → Link generieren)

---

## 📁 Ordnerstruktur

```text
webapp/
├── app.py                  # Flask-Backend
├── templates/
│   └── challenge.html      # HTML-Seite mit Code-Editor
├── static/
│   ├── editor.js           # JS zum Initialisieren des Editors
│   └── style.css           # Styling der Seite
```

## 🚀 Lokales Setup

### 🔧 Voraussetzungen

- Python 3.10 oder neuer
- Flask (`pip install flask`)
- Optional: Virtuelle Umgebung (`venv`)

### 📦 Installation

1. In den `webapp/`-Ordner wechseln:

```bash
cd webapp
```

2. Optional: Virtuelle Umgebung erstellen:

```bash
python -m venv venv
source venv/bin/activate      # auf Windows: venv\Scripts\activate
```

3. Flask installieren:

```bash
pip install flask
```

Oder global über das Hauptprojekt mit:

```bash
pip install -r ../requirements.txt
```

### ▶️ App starten

```bash
python app.py
```

Die Anwendung läuft jetzt auf:
🔗 http://localhost:5000

## 📌 Verfügbare Endpunkte

| Route             | Funktion                                          |
|-------------------|-------------------------------------------------- |
| `/challenge/<id>` | Zeigt die Coding Challenge mit entsprechender ID  |
| `/submit` (POST)  | Empfängt eingereichten Python-Code zur Auswertung |

## ⚙️ Empfohlene Entwicklungsstruktur

Nutze `templates/` für HTML-Dateien (z. B. `challenge.html`)
und `static/` für JavaScript, CSS & Editor-Komponenten.

Du kannst CodeMirror direkt per CDN in dein HTML einbinden oder über `editor.js` konfigurieren.

## 🧪 Testen & Debuggen

- Nutze `print()` im Backend, um Code & Ergebnisse zu loggen
- Bei Flask mit `debug=True` starten für automatisches Reloading
- Browser-DevTools für JS-Fehler prüfen (F12)

## 🧠 Nächste Schritte

- [ ] Testfälle im Backend implementieren
- [ ] Ausführung absichern (`exec()` nur mit leerem Scope)
- [ ] Fehler elegant im Frontend anzeigen
- [ ] (Optional) Lösung an Discord zurücksenden via Webhook/API

## 🔐 Sicherheitshinweis

Der Python-Code wird aktuell lokal mit `exec()` ausgeführt – das ist nur für Lern- und Entwicklungszwecke geeignet!
Für produktive Umgebungen sollte eine abgesicherte Ausführung (z. B. mit Docker oder Piston API) verwendet werden.

## ✨ To-Do

- [ ] Rückgabe visuell schöner gestalten
- [ ] Feedback auf Discord zurückschicken (optional)
- [ ] Speichern von gelösten Challenges
- [ ] Challenge-Bewertungssystem

## 🙏 Credits

Teile dieser Webanwendung basieren auf der Arbeit von:

🔗 [codingshiksha.com – VSCode IDE mit Monaco Editor](https://codingshiksha.com/javascript/build-a-vscode-coding-ide-with-syntax-highlighting-using-monaco-editor-in-browser-using-js/)  
👨‍💻 by [geekygautam1997]

Vielen Dank für die Inspiration!
## 🧑‍💻 Lizenz

Dieses Projekt ist Teil des Lernprojekts "Coder" und Open Source.
Feel free to build upon it!