# 🤖 Coder – Dein Coding Challenge Discord Bot

**Coder** ist ein Lernprojekt und Discord Bot, der dir beim Einstieg ins Programmieren hilft – interaktiv, herausfordernd und direkt über Discord.  
Perfekt für alle, die spielerisch Python lernen wollen, indem sie Coding Challenges lösen.

---

## 🚀 Features

- 📤 Postet zufällige Coding Challenges via `!challenge`
- 🌐 Integrierte Web-IDE für das Lösen von Challenges
- ✅ Automatisierte Überprüfung und Feedback zu Einreichungen
- 📬 Benachrichtigungen im Discord-Channel nach Einreichung von Lösungen
- 🔍 Zeigt Beispielantworten & Lösungen an
- 📈 Motiviert zum täglichen Üben (Gamification geplant)

---

## 🛠️ Setup

### 1. Projekt klonen oder lokal erstellen

```bash
git clone https://github.com/BayramWilson/coding_discord_bot && 
cd coding_discord_bot && 
python3 -m venv .venv && 
source .venv/bin/activate &&
pip install -r requirements.txt &&
cp .env.example .env
```

### 2. .env Datei konfigurieren
Die .env-Datei sollte mindestens folgende Einträge haben:
```
TOKEN=dein-discord-bot-token
DISCORD_CHANNEL_ID=channel-id-für-benachrichtigungen
WEB_APP_URL=http://localhost:5000
```

### 3. Bot starten
Mit dem neuen Start-Skript wird sowohl der Bot als auch die Web-App gestartet:

```bash
python start.py
```

---

## 🧠 Beispielkommandos

| Befehl       | Beschreibung                                       |
|--------------|---------------------------------------------------|
| `!ping`      | Testet, ob der Bot online ist                      |
| `!challenge` | Gibt dir eine zufällige Challenge mit Web-IDE-Link |
| `!submit`    | Reicht Code direkt über Discord ein                |
| `!help`      | Zeigt alle verfügbaren Befehle                     |

---

## 🌐 Web-IDE Nutzung

1. Klicke auf den Link aus dem `!challenge` Befehl
2. Schreibe deine Lösung im Online-Editor
3. Teste deinen Code mit dem "Code ausführen" Button
4. Gib deinen Discord-Benutzernamen ein (optional)
5. Klicke auf "Code einreichen", um deine Lösung zu überprüfen
6. Das Ergebnis wird dir sowohl im Browser als auch im Discord-Channel angezeigt

---

## 📚 Technologien

- **Python 3.10+**
- [`discord.py`](https://discordpy.readthedocs.io/)
- **Flask** für die Web-App
- **Monaco Editor** für die Web-IDE
- `.env` via [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- **Lernziel:** sauberes Bot-Design & Challenge-Logik

---

## 🙋‍♂️ Warum dieses Projekt?

Weil der beste Weg zu lernen **"bauen durch machen"** ist.  
Dieser Bot wurde als Lernreise erstellt – Schritt für Schritt baust du Funktionen, arbeitest mit APIs und entwickelst ein Gefühl für sauberen Python-Code.

---

## ✨ To-Do / Roadmap

- [x] Antwortprüfung für Coding-Challenges  
- [x] Web-IDE-Integration
- [ ] Punkte- oder Levelsystem  
- [ ] Nutzerstatistiken  
- [ ] Mehrsprachige Challenges  
- [ ] Website-Dashboard (optional)

---

## 🧑‍💻 Lizenz

Dieses Projekt ist **Open Source** – nutze es gerne als Lernbasis oder baue es weiter aus!
