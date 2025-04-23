import os
import subprocess
import time
import threading
import webbrowser
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

def start_bot():
    """Startet den Discord-Bot"""
    subprocess.run(["python", "app.py"])

def open_browser():
    """Öffnet den Browser mit der Webapp nach kurzer Verzögerung"""
    time.sleep(2)  # Warten, bis der Server gestartet ist
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    print("===== Coding Challenge Bot wird gestartet =====")
    print("- Discord-Bot und Webapp werden initialisiert...")
    
    # Browser öffnen (in separatem Thread)
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Bot starten (im Hauptthread)
    start_bot() 