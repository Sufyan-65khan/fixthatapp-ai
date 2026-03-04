import os
import requests

topics = [
"whatsapp not sending messages",
"instagram login error",
"youtube app buffering",
"snapchat not loading",
"netflix error code nw-2-5",
"telegram verification code not received",
"zoom microphone not working",
"capcut export failed",
"canva login error",
"amazon app not loading"
]

os.makedirs("articles", exist_ok=True)

for topic in topics:

    prompt = f"""
Write a troubleshooting guide for: {topic}

Structure:
Title
Problem description
Possible causes
Step-by-step fixes
When to contact support
FAQ

Write clearly for non-technical users.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-coder:latest",
            "prompt": prompt,
            "stream": False
        }
    )

    article = response.json()["response"]

    filename = topic.replace(" ", "-") + ".md"

    with open(f"articles/{filename}", "w", encoding="utf-8") as f:
        f.write(article)

    print("Created:", filename)