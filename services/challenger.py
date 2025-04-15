import openai
import json 

file_path =  "./public/easyChallenges/coding_challenges.json"

with open(file_path, encoding="utf-8") as f:
    challenge = json.load(f)

title = challenge[0]["title"]
description = challenge[0]["description"]
function_signature = challenge[0]["function_signature"]
examples = challenge[0]["examples"]



def create_coding_challenge():
    """This function creates an easy coding challenge in python!"""
    with open(file_path, encoding="utf-8") as f:
        challenge = json.load(f)

    title = challenge[0]["title"]
    description = challenge[0]["description"]
    function_signature = challenge[0]["function_signature"]
    examples = challenge[0]["examples"]
    return title, description, function_signature, examples
