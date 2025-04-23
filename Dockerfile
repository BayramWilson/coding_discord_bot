FROM python:3.11-slim

WORKDIR /app

# Installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Projektcode
COPY . .

# Exponiere den Port für die Web-App
EXPOSE 5000

# Starte den Bot (der dann die Web-App startet)
CMD ["python", "app.py"] 