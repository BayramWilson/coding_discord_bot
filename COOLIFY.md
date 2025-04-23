# Bereitstellung des Discord Coding Bots in Coolify

Diese Anleitung beschreibt, wie du den Discord Coding Bot in Coolify bereitstellen kannst, wobei IP-Adressen statt DNS-Namen verwendet werden.

## Voraussetzungen

1. Ein laufender Coolify-Server mit einer festen IP-Adresse
2. Einen Discord Bot-Token (https://discord.com/developers/applications)
3. Ein Discord-Server, auf dem du Administratorrechte hast

## Schritte zur Bereitstellung in Coolify

### 1. Projekt in Coolify importieren

1. Öffne das Coolify-Dashboard
2. Klicke auf "Create new Resource" > "Application"
3. Wähle die Git-Quelle (z.B. GitHub, GitLab)
4. Wähle das entsprechende Repository aus

### 2. Umgebungsvariablen konfigurieren

Die folgenden Umgebungsvariablen müssen in Coolify gesetzt werden:

```
TOKEN=dein_discord_bot_token
LEVEL_UP_CHANNEL=dein_channel_id
DISCORD_CHANNEL_ID=dein_channel_id
DISCORD_WEBHOOK_URL=deine_webhook_url
WEB_APP_URL=http://deine_server_ip:5000
OPENAI_API_KEY=dein_openai_api_key (optional)
OPENAI_MODEL=gpt-4 (optional)
OPENAI_TEMPERATURE=0.7 (optional)
OPENAI_MAX_TOKENS=1000 (optional)
```

**Wichtig:** Ersetze `deine_server_ip` mit der tatsächlichen IP-Adresse deines Coolify-Servers.

### 3. Docker-Einstellungen

Coolify sollte automatisch die Dockerfile erkennen und verwenden. Stelle sicher, dass Port 5000 freigegeben ist.

### 4. Bereitstellung starten

1. Klicke auf "Save" und dann auf "Deploy"
2. Warte, bis die Bereitstellung abgeschlossen ist

### 5. Bot testen

Nach erfolgreicher Bereitstellung kannst du den Bot auf deinem Discord-Server testen:

1. Gib den Befehl `!ping` ein, um zu prüfen, ob der Bot antwortet
2. Gib den Befehl `!challenge` ein, um eine Coding-Challenge zu starten

## Fehlerbehebung

### Web-App ist nicht erreichbar

Stelle sicher, dass:
- Port 5000 in deiner Firewall freigegeben ist
- Die Umgebungsvariable `WEB_APP_URL` auf die richtige IP-Adresse gesetzt ist
- Der Container läuft (`docker ps` im Terminal)

### Discord-Befehle funktionieren nicht

Stelle sicher, dass:
- Der Bot-Token korrekt ist
- Der Bot die richtigen Berechtigungen hat
- Der Bot dem richtigen Discord-Kanal hinzugefügt wurde

## Links in Discord korrekt anzeigen

Damit Discord-Nutzer auf die Challenge-Links klicken können, muss in den Bot-Nachrichten die IP-Adresse statt `localhost` verwendet werden:

```python
challenge_url = f"{WEB_APP_URL}/challenge/{challenge_id}?code={starter_code}"
```

Die Variable `WEB_APP_URL` muss auf `http://deine_server_ip:5000` gesetzt sein. 