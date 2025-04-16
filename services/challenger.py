import openai
import json 
import ast
import io
import sys
from contextlib import redirect_stdout

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

def check_solution(user_code, challenge_index=1):
    """Prüft eine eingesendete Lösung auf Korrektheit.
    
    Args:
        user_code (str): Der vom Nutzer eingesendete Python-Code
        challenge_index (int): Index der Challenge im JSON-File (Standard: 1)
        
    Returns:
        dict: Ein Ergebnis-Dictionary mit Status, Nachricht und Details
    """
    # Challenge laden
    with open(file_path, encoding="utf-8") as f:
        challenges = json.load(f)
    
    if challenge_index >= len(challenges):
        return {"status": "error", "message": "Challenge nicht gefunden"}
    
    challenge = challenges[challenge_index]
    
    # Beispiele und erwartete Ergebnisse extrahieren
    test_cases = []
    for example in challenge["examples"]:
        parts = example.split(" ➞ ")
        if len(parts) != 2:
            continue
            
        # Funktionsaufruf parsen
        func_call = parts[0].strip()
        expected_result = parts[1].strip()
        
        # Anführungszeichen bei Strings erhalten
        if expected_result.startswith('"') and expected_result.endswith('"'):
            expected_result = expected_result[1:-1]
        
        test_cases.append({
            "call": func_call,
            "expected": expected_result
        })
    
    # Prüfen, ob der Code die Funktion definiert
    try:
        # Namespace für die Code-Ausführung
        local_vars = {}
        
        # Code in isolierter Umgebung ausführen
        exec(user_code, {}, local_vars)
        
        # Funktionsname aus der Signatur extrahieren
        func_name = challenge["function_signature"].split("def ")[1].split("(")[0].strip()
        
        if func_name not in local_vars:
            return {
                "status": "error",
                "message": f"Die Funktion '{func_name}' wurde nicht gefunden. Hast du sie definiert?"
            }
        
        # Alle Testfälle durchlaufen
        results = []
        all_passed = True
        
        for test in test_cases:
            # Ausgabe umleiten
            f = io.StringIO()
            with redirect_stdout(f):
                # Funktionsaufruf ausführen
                try:
                    # Funktionsaufruf vorbereiten
                    call_code = f"result = {test['call']}"
                    test_vars = local_vars.copy()
                    
                    # Ausführen und Ergebnis speichern
                    exec(call_code, {}, test_vars)
                    actual_result = test_vars["result"]
                    
                    # Erwartetes Ergebnis konvertieren
                    if expected_result.lower() == "true":
                        expected = True
                    elif expected_result.lower() == "false":
                        expected = False
                    else:
                        # Versuchen, zu einer Zahl zu konvertieren
                        try:
                            expected = int(test["expected"])
                        except ValueError:
                            try:
                                expected = float(test["expected"])
                            except ValueError:
                                # Alles andere als String behandeln
                                expected = test["expected"]
                    
                    # Ergebnis vergleichen
                    if str(actual_result) == str(expected) or actual_result == expected:
                        passed = True
                        status = "✅"
                    else:
                        passed = False
                        all_passed = False
                        status = "❌"
                    
                    results.append({
                        "test": test["call"],
                        "expected": test["expected"],
                        "actual": str(actual_result),
                        "passed": passed,
                        "status": status
                    })
                    
                except Exception as e:
                    all_passed = False
                    results.append({
                        "test": test["call"],
                        "error": str(e),
                        "passed": False,
                        "status": "❌"
                    })
        
        # Gesamtergebnis
        if all_passed:
            return {
                "status": "success",
                "message": "🎉 Alle Tests bestanden!",
                "details": results
            }
        else:
            return {
                "status": "fail",
                "message": "❌ Einige Tests sind fehlgeschlagen.",
                "details": results
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"❌ Fehler beim Ausführen deines Codes: {str(e)}"
        }

# Beispiel für Testzwecke
if __name__ == "__main__":
    test_code = """
def begruessung(name):
    return f"Hallo {name}!"
"""
    print(check_solution(test_code, 1))