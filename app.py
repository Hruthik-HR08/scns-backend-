import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        message = data.get("message", "").strip()
        role = data.get("role", "Guest")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Groq AI API call
        headers = {
            "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",  # Super fast model
            "messages": [
                {
                    "role": "system", 
                    "content": "You are SCNS - Smart Campus Navigation assistant for NIE Mysore. Answer about campus navigation, buildings (A-E), library, canteen, classrooms, events. Be concise and helpful."
                },
                {"role": "user", "content": message}
            ],
            "max_tokens": 150
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            reply_text = response.json()["choices"][0]["message"]["content"]
        else:
            reply_text = f"SCNS: Working on '{message}' - full campus AI coming soon!"

        return jsonify({"reply": reply_text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
