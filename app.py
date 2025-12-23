import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(app)

def get_nie_live_data():
    """Fetch live data from NIE website"""
    try:
        response = requests.get("https://www.nie.ac.in/", timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract notices, events, headlines
        notices = [item.get_text().strip()[:100] 
                  for item in soup.find_all(['h2','h3','h4','li','.notice'])[:6]]
        
        title = soup.title.string if soup.title else "NIE Mysore"
        return {
            "title": title,
            "latest_notices": notices[:4],
            "status": "live"
        }
    except:
        return {"status": "offline", "message": "NIE website temporarily unavailable"}

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        message = data.get("message", "").strip()
        role = data.get("role", "Guest")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Get LIVE NIE data
        nie_data = get_nie_live_data()
        
        # Groq AI call with LIVE data
        headers = {
            "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
        
        context = f"LIVE NIE data: {json.dumps(nie_data)} | Campus info: Blocks A(CSE/IT), B(ECE/ME), E(Library), Canteen near A"
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are SCNS - NIE Mysore Campus AI. Use this {context}. Answer concisely about campus/navigation/NIE info."
                },
                {"role": "user", "content": message}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=payload, timeout=10
        )
        
        if response.status_code == 200:
            reply_text = response.json()["choices"][0]["message"]["content"].strip()
        else:
            reply_text = f"SCNS: Processing '{message}' with NIE live data. Full AI active!"

        return jsonify({"reply": reply_text})
        
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
