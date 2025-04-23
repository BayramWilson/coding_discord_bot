from flask import Flask, request, render_template, jsonify
import sys, io
import json
import os
import requests

# Importiere die Prüffunktion aus dem Hauptprojekt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.challenger import check_solution

app = Flask(__name__, static_url_path='/static')

# Discord bot webhook für Benachrichtigungen
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "")
BOT_TOKEN = os.getenv("TOKEN", "")  # Bot-Token aus der Hauptapp verwenden

# Überprüfen Sie, ob DISCORD_WEBHOOK_URL gesetzt ist, wenn nicht, erstellen Sie einen Webhook
if not DISCORD_WEBHOOK_URL and DISCORD_CHANNEL_ID and BOT_TOKEN:
    print("WARNUNG: DISCORD_WEBHOOK_URL ist nicht gesetzt. Die Benachrichtigungen an Discord werden möglicherweise nicht funktionieren.")
    print("Bitte setzen Sie DISCORD_WEBHOOK_URL in der .env-Datei.")

# Lade die Challenges
def load_challenges():
    """Lädt die Challenges aus der JSON-Datei mit Fallbacks für verschiedene Pfade"""
    possible_paths = [
        "../public/easyChallenges/coding_challenges.json",  # Relativer Pfad von webapp/
        "./public/easyChallenges/coding_challenges.json",   # Relativer Pfad vom Hauptverzeichnis
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                     "public/easyChallenges/coding_challenges.json")  # Absoluter Pfad
    ]
    
    for path in possible_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                print(f"Challenges geladen von: {path}")
                return json.load(f)
        except FileNotFoundError:
            continue
    
    # Fallback: Leere Challenge-Liste zurückgeben
    print("WARNUNG: Keine Challenge-Datei gefunden!")
    return []

challenges = load_challenges()

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
    
    # Startercode aus URL-Parameter übernehmen, falls vorhanden
    starter_code = request.args.get("code", challenges[challenge_id]["function_signature"])
    
    return render_template("challenge.html", 
                          challenge=challenges[challenge_id],
                          challenge_id=challenge_id,
                          starter_code=starter_code)

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
    
    # Stelle sicher, dass die Challenge-ID gültig ist
    if challenge_id < 0 or challenge_id >= len(challenges):
        return jsonify({
            "status": "error",
            "message": f"Ungültige Challenge-ID: {challenge_id}",
            "discord_notification": False
        })
    
    print(f"Code-Einreichung: Challenge {challenge_id} von Benutzer {discord_username or 'anonym'}")
    print(f"Eingereichte Lösung:\n{user_code}")
    
    # Code mit der check_solution Funktion prüfen
    result = check_solution(user_code, challenge_id)
    print(f"Ergebnis: {result}")
    
    # Wenn ein Discord-Username angegeben wurde, senden wir das Ergebnis an Discord
    discord_notification = False
    if discord_username:
        try:
            challenge = challenges[challenge_id]
            print(f"Versuche Discord-Benachrichtigung zu senden für Challenge '{challenge['title']}'")
            discord_notification = send_to_discord(
                discord_username, 
                challenge["title"], 
                result,
                user_code
            )
            print(f"Discord-Benachrichtigung {'erfolgreich' if discord_notification else 'fehlgeschlagen'}")
        except Exception as e:
            print(f"Fehler beim Versuch, Discord-Benachrichtigung zu senden: {str(e)}")
            discord_notification = False
    
    # Füge Information über erfolgreiche Discord-Benachrichtigung hinzu
    result["discord_notification"] = discord_notification
    
    return jsonify(result)

def send_to_discord(username, challenge_title, result, code):
    """Sendet das Ergebnis an Discord über einen Webhook oder direkt über die Bot-API"""
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
        print(f"Sende Discord-Benachrichtigung für Benutzer {username}...")
        
        # Prüfe, ob die erforderlichen Tokens vorhanden sind
        if not BOT_TOKEN or not DISCORD_CHANNEL_ID:
            print(f"Fehlende Konfiguration: BOT_TOKEN={bool(BOT_TOKEN)}, CHANNEL_ID={bool(DISCORD_CHANNEL_ID)}")
            if DISCORD_WEBHOOK_URL:
                print("Verwende Fallback auf Webhook...")
            else:
                print("Keine Discord-Integration möglich: Weder Bot noch Webhook konfiguriert")
                return False
                
        # Versuche zuerst, den Bot direkt zu verwenden
        if BOT_TOKEN and DISCORD_CHANNEL_ID:
            try:
                headers = {
                    "Authorization": f"Bot {BOT_TOKEN}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "content": message
                }
                url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages"
                print(f"Sende API-Anfrage an Discord (URL: {url})")
                
                response = requests.post(url, headers=headers, json=payload)
                print(f"Discord API Antwort: Status {response.status_code}")
                
                if response.status_code in [200, 201, 204]:
                    print("Benachrichtigung erfolgreich gesendet")
                    return True
                else:
                    print(f"Fehler beim Senden an Discord API: {response.text}")
                    # Bei 401/403-Fehlern: Warnung über fehlende Berechtigungen anzeigen
                    if response.status_code in [401, 403]:
                        print("WARNUNG: Der Bot hat keine Berechtigungen für diesen Kanal oder das Token ist ungültig.")
                    # Bei 405-Fehler: Möglicherweise falsche Methode
                    elif response.status_code == 405:
                        print("WARNUNG: Methode nicht erlaubt. Siehe Discord API-Dokumentation.")
            except Exception as e:
                print(f"Ausnahme bei Discord API-Anfrage: {str(e)}")
                # Weitermachen zum Webhook-Fallback
                
        # Fallback auf Webhook, wenn direkte API-Anfrage fehlschlägt oder Tokens fehlen
        if DISCORD_WEBHOOK_URL:
            try:
                print(f"Versuche Webhook-Benachrichtigung für Discord: {DISCORD_WEBHOOK_URL}")
                payload = {
                    "content": message,
                    "username": "Web-Coding-Challenge"
                }
                
                response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
                print(f"Discord Webhook Antwort: Status {response.status_code}")
                
                if response.status_code == 204:
                    print("Webhook-Benachrichtigung erfolgreich gesendet")
                    return True
                else:
                    print(f"Fehler beim Senden an Discord Webhook: {response.text}")
            except Exception as e:
                print(f"Ausnahme bei Webhook-Anfrage: {str(e)}")
                
        print("Alle Discord-Benachrichtigungsversuche fehlgeschlagen")
        return False
    except Exception as e:
        print(f"Unerwarteter Fehler beim Senden an Discord: {e}")
        return False

@app.route("/test-webhook", methods=["GET"])
def test_webhook():
    """Testet die Discord-Webhook-Integration"""
    if not DISCORD_WEBHOOK_URL:
        return jsonify({"success": False, "message": "Kein Webhook konfiguriert"})
    
    try:
        # Sende eine Testnachricht an Discord
        message = "✅ **Test erfolgreich!** Der Webhook für die Coding Challenge App funktioniert."
        
        payload = {
            "content": message,
            "username": "Web-Coding-Challenge"
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        success = response.status_code == 204
        
        return jsonify({
            "success": success,
            "status_code": response.status_code,
            "message": "Webhook-Test erfolgreich" if success else f"Webhook-Test fehlgeschlagen: {response.text}"
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Fehler: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
