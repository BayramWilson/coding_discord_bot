# 🤖 Coder – Dein Coding Challenge Discord Bot

**Coder** ist ein Lernprojekt und Discord Bot, der dir beim Einstieg ins Programmieren hilft – interaktiv, herausfordernd und direkt über Discord.  
Perfekt für alle, die spielerisch Python lernen wollen, indem sie Coding Challenges lösen.

---

## 🚀 Features

- 📤 Postet zufällige Coding Challenges via `!challenge`
- ✅ Reagiert auf Einreichungen mit Feedback (coming soon)
- 🔍 Zeigt Beispielantworten & Lösungen an
- 📈 Motiviert zum täglichen Üben (Gamification geplant)

---

## 🛠️ Setup

### 1. Projekt klonen oder lokal erstellen

```bash
git clone https://github.com/BayramWilson/coding_discord_bot && 
cd coding_discord_bot && 
python -m venv venv && 
source venv/bin/activate &&
pip install -r requirements.txt &&
cp .env.example .env
```

### 2. .env Datei konfigurieren

### 3. Bot starten

```bash
python app.py
```

---

## 🧠 Beispielkommandos

| Befehl       | Beschreibung                          |
|--------------|---------------------------------------|
| `!ping`      | Testet, ob der Bot online ist         |
| `!challenge` | Gibt dir eine zufällige Challenge     |
| `!help`      | Zeigt alle verfügbaren Befehle        |

---

## 📚 Technologien

- **Python 3.10+**
- [`discord.py`](https://discordpy.readthedocs.io/)
- `.env` via [`python-dotenv`](https://pypi.org/project/python-dotenv/)
- **Lernziel:** sauberes Bot-Design & Challenge-Logik

---

## 🙋‍♂️ Warum dieses Projekt?

Weil der beste Weg zu lernen **"bauen durch machen"** ist.  
Dieser Bot wurde als Lernreise erstellt – Schritt für Schritt baust du Funktionen, arbeitest mit APIs und entwickelst ein Gefühl für sauberen Python-Code.

---

## ✨ To-Do / Roadmap

- [ ] Antwortprüfung für Coding-Challenges  
- [ ] Punkte- oder Levelsystem  
- [ ] Nutzerstatistiken  
- [ ] Mehrsprachige Challenges  
- [ ] Website-Dashboard (optional)

---

## 🧑‍💻 Lizenz

Dieses Projekt ist **Open Source** – nutze es gerne als Lernbasis oder baue es weiter aus!
