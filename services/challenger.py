import openai
import json 

file_path = "./public/easyChallenges/coding_challenges.json"

def create_coding_challenge():
    """This function creates an easy coding challenge in python!"""
    with open(file_path, encoding="utf-8") as f:
        challenge = json.load(f)

    title = challenge[1]["title"]
    description = challenge[1]["description"]
    function_signature = challenge[1]["function_signature"]
    examples = challenge[1]["examples"]
    
    # Format für Discord Markdown ohne unerwünschte Einrückungen
    message_md_format = f"""# 🧠 {title}
## Beschreibung
{description}
## Startercode
```python
{function_signature}
```
## Beispiele"""

    # Beispiele ohne Einrückung hinzufügen
    for example in examples:
        message_md_format += f"\n• `{example}`"
        
    return message_md_format

print(create_coding_challenge())

user_code = ""

def check_solution(solution):
    """This function checks a solution, written in the discord "level up" channel, and proves it wrong or right."""

    return