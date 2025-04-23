import discord
import os
import random
import threading
from discord.ext import commands
from dotenv import load_dotenv
from services.challenger import create_coding_challenge, check_solution
load_dotenv() 

TOKEN = os.getenv("TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:5000")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "")

# Starte die Webapp in einem separaten Thread
def start_webapp():
    from webapp.app import app
    app.run(debug=False, host='0.0.0.0', port=5000)

# Webapp im Hintergrund starten
webapp_thread = threading.Thread(target=start_webapp, daemon=True)
webapp_thread.start()
print("Webapp gestartet auf http://localhost:5000")

# Initialize Bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist online als {bot.user}')

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name="challenge")
async def challenge(ctx):
    """Sendet eine Coding Challenge an den Channel"""
    # Zufällige Challenge auswählen
    with open("./public/easyChallenges/coding_challenges.json", "r", encoding="utf-8") as f:
        import json
        challenges = json.load(f)
        challenge_id = random.randint(0, len(challenges) - 1)
    
    # Challenge-Informationen
    challenge = challenges[challenge_id]
    
    # Erstelle einen Link mit den Challenge-Informationen
    import urllib.parse
    starter_code = urllib.parse.quote(challenge["function_signature"])
    challenge_url = f"{WEB_APP_URL}/challenge/{challenge_id}?code={starter_code}"
    
    # Erstelle einen Embed mit den Challenge-Informationen
    embed = discord.Embed(
        title=f"🧠 {challenge['title']}",
        description=f"{challenge['description']}\n\n[In der Web-IDE öffnen]({challenge_url})",
        color=0x3498db
    )
    
    # Beispiele hinzufügen
    example_text = "\n".join([f"• `{example}`" for example in challenge['examples']])
    embed.add_field(name="Beispiele", value=example_text, inline=False)
    
    embed.set_footer(text="Tipp: Du kannst deinen Discord-Namen in der IDE eingeben, um eine Benachrichtigung zu erhalten!")
    
    await ctx.send(embed=embed)

@bot.command(name="web")
async def web_challenge(ctx, challenge_id=None):
    """Generiert einen Link zur Web-IDE für die Challenge"""
    if challenge_id is None:
        # Zufällige Challenge auswählen
        with open("./public/easyChallenges/coding_challenges.json", "r", encoding="utf-8") as f:
            import json
            challenges = json.load(f)
            challenge_id = random.randint(0, len(challenges) - 1)
    
    # Link zur Web-IDE generieren
    challenge_url = f"{WEB_APP_URL}/challenge/{challenge_id}"
    
    embed = discord.Embed(
        title="🌐 Web Coding Challenge",
        description=f"Klicke den Link um die Challenge im Browser zu lösen!\n\n[Challenge öffnen]({challenge_url})",
        color=0x3498db
    )
    embed.set_footer(text="Tipp: Du kannst deinen Discord-Namen angeben, um eine Benachrichtigung zu erhalten!")
    
    await ctx.send(embed=embed)

@bot.command(name="submit")
async def submit(ctx, *, code=None):
    """Prüft eine eingesendete Lösung"""
    if not code:
        await ctx.send("❌ Du musst deinen Code nach dem Befehl einfügen, z.B.:\n```!submit def begruessung(name):\n    return f\"Hallo {name}!\"```")
        return
    
    # Formatierung des Codes (falls in Discord-Codeblöcken)
    if code.startswith("```python") and code.endswith("```"):
        code = code[9:-3].strip()
    elif code.startswith("```") and code.endswith("```"):
        code = code[3:-3].strip()
    
    # Code prüfen
    result = check_solution(code)
    
    if result["status"] == "success":
        await ctx.send(f"{ctx.author.mention} {result['message']}")
    elif result["status"] == "fail":
        # Details in einem Codeblock anzeigen
        details = "\n".join([f"{d['test']} → Erwartet: {d['expected']}, Erhielt: {d['actual']} {d['status']}" for d in result["details"]])
        await ctx.send(f"{ctx.author.mention} {result['message']}\n```\n{details}\n```")
    else:
        await ctx.send(f"{ctx.author.mention} {result['message']}")

bot.run(TOKEN)