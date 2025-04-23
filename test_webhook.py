import requests
import sys

# Direct webhook URL (we'll paste the URL directly into the script)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1364532618892410931/nqxBPY73HJ3PkkM_afJKcLgaMBqMQNe0lJ1OAaKxV0tXGxh5aVw5ti-xvmANIZaoIXcw"

print(f"Using webhook URL: {DISCORD_WEBHOOK_URL}")

# Prepare test message
message = "✅ **Webhook Test erfolgreich!** Die Discord-Integration funktioniert."

payload = {
    "content": message,
    "username": "Web-Coding-Challenge Bot"
}

# Send the message
try:
    print("Sending test message to Discord...")
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 204:
        print("✅ Success! Message sent to Discord.")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}") 