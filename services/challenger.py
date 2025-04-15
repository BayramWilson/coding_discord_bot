import openai
import json 

file_path = "./public/easyChallenges/coding_challenges.json"

def create_coding_challenge():
    """This function creates an easy coding challenge in python!"""
    with open(file_path, encoding="utf-8") as f:
        challenge = json.load(f)

    title = challenge[0]["title"]
    description = challenge[0]["description"]
    function_signature = challenge[0]["function_signature"]
    examples = challenge[0]["examples"]
    
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