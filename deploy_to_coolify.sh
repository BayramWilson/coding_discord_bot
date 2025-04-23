#!/bin/bash

# Skript zur Vorbereitung der Bereitstellung in Coolify

# Prüfen, ob IP-Adresse als Parameter übergeben wurde
if [ $# -eq 0 ]; then
  echo "Bitte gib die IP-Adresse deines Coolify-Servers an:"
  echo "Beispiel: ./deploy_to_coolify.sh 192.168.1.100"
  exit 1
fi

COOLIFY_IP=$1

# Prüfen, ob der String eine IP-Adresse sein könnte
if ! [[ $COOLIFY_IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Die angegebene IP-Adresse '$COOLIFY_IP' scheint keine gültige IP-Adresse zu sein."
  echo "Format sollte wie folgt sein: xxx.xxx.xxx.xxx"
  exit 1
fi

echo "Bereite Bereitstellung für Coolify-Server mit IP $COOLIFY_IP vor..."

# .env.production aktualisieren
echo "Aktualisiere .env.production..."
sed -i.bak "s|YOUR_SERVER_IP|$COOLIFY_IP|g" .env.production

echo "Stelle sicher, dass du folgende Schritte ausführst:"
echo "1. Pushe deine Änderungen zu deinem Git-Repository:"
echo "   git add ."
echo "   git commit -m \"Vorbereitung für Coolify-Deployment\""
echo "   git push"
echo ""
echo "2. Gehe zum Coolify-Dashboard und erstelle eine neue Anwendung"
echo "3. Wähle dein Git-Repository und den Branch"
echo "4. Stelle sicher, dass folgende Umgebungsvariablen gesetzt sind (wie in .env.production):"
echo "   - TOKEN=dein_discord_bot_token"
echo "   - WEB_APP_URL=http://$COOLIFY_IP:5000"
echo "   - DISCORD_CHANNEL_ID=dein_channel_id"
echo "   - DISCORD_WEBHOOK_URL=deine_webhook_url (optional)"
echo ""
echo "5. Klicke auf 'Speichern' und 'Bereitstellen'"
echo ""
echo "6. Nach erfolgreicher Bereitstellung teste den Bot mit '!ping' in deinem Discord-Server" 