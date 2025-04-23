#!/bin/bash

# Stoppe und entferne vorhandenen Container
docker-compose down

# Stelle sicher, dass die .env.production aktuell ist
echo "Prüfe .env.production..."
if ! grep -q "YOUR_SERVER_IP" .env.production; then
  echo "IP-Adresse in .env.production bereits gesetzt."
else
  # Hole lokale IP-Adresse
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    IP=$(hostname -I | awk '{print $1}')
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    IP=$(ipconfig getifaddr en0)
  else
    echo "Betriebssystem nicht erkannt. Bitte trage deine IP-Adresse manuell in .env.production ein."
    exit 1
  fi
  
  echo "Ersetze Platzhalter in .env.production mit lokaler IP: $IP"
  sed -i.bak "s|YOUR_SERVER_IP|$IP|g" .env.production
fi

# Baue und starte den Container
echo "Starte Docker-Container..."
docker-compose up --build -d

echo "Container läuft im Hintergrund. Logs anzeigen mit:"
echo "docker-compose logs -f"
echo ""
echo "Teste den Bot in deinem Discord-Server mit '!ping'"
echo "Die Web-App sollte unter http://<deine-ip>:5000 erreichbar sein" 