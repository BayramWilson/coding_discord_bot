from flask import Flask, request, render_template, jsonify
import sys, io
import json
import os
import requests

# Importiere die Prüffunktion aus dem Hauptprojekt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.challenger import check_solution

app = Flask(__name__)

# Discord bot webhook für Benachrichtigungen
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "")

# Lade die Challenges
with open("../public/easyChallenges/coding_challenges.json", "r", encoding="utf-8") as f:
    challenges = json.load(f)

@app.route("/")
def home():
    """Zeigt eine Übersicht aller verfügbaren Challenges"""
    challenges_preview = []
    for i, challenge in enumerate(challenges):
        challenges_preview.append({
            "id": i,
            "title": challenge["title"],
            "description": challenge["description"][:100] + "..." if len(challenge["description"]) > 100 else challenge["description"]
        })
    return render_template("challenge.html", challenges_list=challenges_preview)

@app.route("/challenge/<int:challenge_id>")
def challenge(challenge_id):
    """Zeigt eine spezifische Challenge an"""
    if challenge_id < 0 or challenge_id >= len(challenges):
        return "Challenge nicht gefunden", 404
    
    return render_template("challenge.html", 
                          challenge=challenges[challenge_id],
                          challenge_id=challenge_id)

@app.route("/run", methods=["POST"])
def run():
    """Führt den Code aus und gibt die Ausgabe zurück (ohne Validierung)"""
    data = request.get_json()
    user_code = data.get("code", "")
    stdout = io.StringIO()

    try:
        sys.stdout = stdout
        exec(user_code, {}, {})
    except Exception as e:
        return jsonify({ "output": f"❌ Fehler: {str(e)}" })

    output = stdout.getvalue()
    return jsonify({ "output": output or "✅ Kein Fehler, aber keine Ausgabe." })

@app.route("/submit", methods=["POST"])
def submit():
    """Prüft den Code gegen die Testfälle und benachrichtigt optional Discord"""
    data = request.get_json()
    if not data:
        data = request.form
    
    user_code = data.get("code", "")
    challenge_id = int(data.get("challenge_id", 1))
    discord_username = data.get("discord_username", "")
    
    # Code mit der check_solution Funktion prüfen
    result = check_solution(user_code, challenge_id)
    
    # Wenn ein Discord-Username angegeben wurde und wir einen Webhook haben,
    # senden wir das Ergebnis an Discord
    discord_notification = False
    if discord_username and DISCORD_WEBHOOK_URL:
        challenge = challenges[challenge_id]
        discord_notification = send_to_discord(
            discord_username, 
            challenge["title"], 
            result,
            user_code
        )
    
    # Füge Information über erfolgreiche Discord-Benachrichtigung hinzu
    result["discord_notification"] = discord_notification
    
    return jsonify(result)

def send_to_discord(username, challenge_title, result, code):
    """Sendet das Ergebnis an Discord über einen Webhook"""
    if not DISCORD_WEBHOOK_URL:
        return False
        
    status_emoji = "🎉" if result["status"] == "success" else "❌"
    
    # Formatiere die Nachricht für Discord
    message = f"{status_emoji} **{username}** hat die Challenge **{challenge_title}** eingereicht!\n\n"
    message += f"**Ergebnis:** {result['message']}\n\n"
    
    # Füge Details hinzu, wenn vorhanden
    if "details" in result and result["details"]:
        message += "**Details:**\n"
        for detail in result["details"]:
            status = "✅" if detail.get("passed", False) else "❌"
            expected = detail.get("expected", "?")
            actual = detail.get("actual", "?")
            test = detail.get("test", "?")
            
            message += f"{status} {test} → Erwartet: `{expected}`, Erhielt: `{actual}`\n"
    
    # Füge den Code hinzu
    message += "\n**Code:**\n```python\n" + code + "\n```"
    
    # Sende die Nachricht an Discord
    try:
        payload = {
            "content": message,
            "username": "Web-Coding-Challenge"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        return response.status_code == 204
    except Exception as e:
        print(f"Fehler beim Senden an Discord: {e}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
