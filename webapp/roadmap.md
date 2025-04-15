# 🚀 Lern-Roadmap für Web + Flask + Sandbox-Ausführung (für Coder Bot)

Diese Datei begleitet dich durch den Aufbau deiner Mini-IDE mit Webinterface, Flask-Backend und sicherer Code-Ausführung.  
Ziel: Du bleibst fokussiert, lernst nur das Nötige und baust gleichzeitig aktiv dein Projekt weiter aus.

---

## ✅ Überblick über Projektziele

- [ ] Ein Web-Interface (Editor + Submit) für Coding Challenges
- [ ] Flask-Backend zur Anzeige & Code-Entgegennahme
- [ ] Code-Ausführung (Sandboxed) inkl. Testprüfung
- [ ] Discord Bot generiert Link zur Challenge

---

## 📚 HTML/CSS Auffrischen (nur das Nötigste)

### 📌 Ziele:
- Grundlagen von HTML-Elementen
- Formulare, Inputs, Buttons
- Einfaches CSS-Layout (Flexbox, Farben, Fonts)

### 📎 Ressourcen:
- [https://web.dev/learn/html/](https://web.dev/learn/html/) (Google – super kompakt & modern)
- [https://flexboxfroggy.com/](https://flexboxfroggy.com/) (Flexbox spielerisch lernen)
- [https://css-tricks.com/snippets/css/a-guide-to-flexbox/](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) (Flexbox Referenz)

### ✅ To-Dos:
- [x] Eine einfache Seite mit `<form>`, `<textarea>` und Button bauen
- [x] Styles per CSS oder inline gestalten
- [ ] Editor später durch JS-Editor ersetzen

---

## 🧠 JavaScript-Editor einbinden (CodeMirror)

### 📌 Ziel:
- Nutze **CodeMirror** (leichter als Monaco) als eingebetteten Editor

### 📎 Ressourcen:
- [https://codemirror.net/](https://codemirror.net/)
- [https://codemirror.net/examples/](https://codemirror.net/examples/) (praktische Beispiele)
- [Einsteiger-Tutorial mit CDN](https://www.digitalocean.com/community/tutorials/how-to-use-codemirror-in-a-web-page)

### ✅ To-Dos:
- [x] `<script>` und `<link>` via CDN in HTML einbinden
- [x] Editor initialisieren
- [ ] „Submit“-Button, der Code an Flask-Backend sendet

---

## 🔥 Flask lernen & verwenden

### 📌 Ziele:
- Routing mit `@app.route()`
- HTML-Dateien über `render_template()` anzeigen
- Daten über `POST` empfangen (z. B. Code)

### 📎 Ressourcen:
- [https://flask.palletsprojects.com/en/latest/quickstart/](https://flask.palletsprojects.com/en/latest/quickstart/)
- [https://realpython.com/flask-by-example-part-1-project-setup/](https://realpython.com/flask-by-example-part-1-project-setup/)
- [Flask in 5 Minuten (YouTube)](https://www.youtube.com/watch?v=Z1RJmh_OqeA) – nur wenn du visuell arbeitest

### ✅ To-Dos:
- [ ] Flask-App in `webapp/app.py` erstellen
- [ ] `@app.route("/challenge/<id>")` → zeigt HTML mit Challenge
- [ ] `@app.route("/submit", methods=["POST"])` → empfängt Nutzereingabe
- [ ] JSON mit Challenge-Lösung verarbeiten

---

## 🔐 Python Code-Ausführung (Sandbox)

### 📌 Ziele:
- Code sicher ausführen (z. B. mit `exec`)
- Eingaben prüfen (Testfälle)
- Fehler abfangen und als Antwort geben

### 📎 Ressourcen:
- [Offizielles `exec()`-HowTo (Python Doku)](https://docs.python.org/3/library/functions.html#exec)
- [Tame `exec()`](https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html) (warum man vorsichtig sein sollte)
- (später) [https://github.com/engineer-man/piston](https://github.com/engineer-man/piston) – externe Ausführung möglich

### ✅ To-Dos:
- [ ] Code in `exec(user_code, {}, local_vars)` ausführen
- [ ] Funktion auslesen & Testcases prüfen
- [ ] Ergebnis ins Webinterface zurückgeben

---

## 🌐 Bonus – Discord Integration

### 📌 Ziele:
- Bot verschickt Link zur Web-IDE
- Später: Lösungsergebnisse vom Webserver an Bot zurückmelden

### ✅ To-Dos:
- [ ] Discord-Command `!challenge` generiert Challenge-ID + URL
- [ ] Link zeigt auf Flask-Server (z. B. `http://localhost:5000/challenge/2`)

---

## 🧩 Tipps für deinen Lernstil

- 🚦 Lerne im „Projektkontext“ – nicht durch 10 Videos ohne Anwendung
- 🧱 Fang mit Basics an und erweitere das, was du wirklich brauchst
- 📝 Notiere dir, **was du wirklich verstehen willst**
- 🤝 Frag bei konkreten Problemen (statt „Ich check nix“)

---

> Du baust etwas Reales. Nutze Lernen als Werkzeug – nicht als Ablenkung.  
> ✊ Let's go!
