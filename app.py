import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        message = data.get("message", "").strip().lower()
        role = data.get("role", "Guest")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # SCNS Campus Assistant replies
        if any(word in message for word in ["hello", "hi", "hey"]):
            reply_text = "Hi! I'm SCNS - your Smart Campus Navigation assistant. Ask me about NIE buildings, classrooms, or campus navigation!"
        
        elif any(word in message for word in ["building", "classroom", "room", "lab"]):
            reply_text = "NIE has 5 main academic blocks: Block A (CSE/IT), Block B (ECE/ME), Block C (Civil/CE), Block D (Labs), Block E (Library). Which building do you need?"
        
        elif "library" in message:
            reply_text = "NIE Central Library is in Block E (Ground Floor). Open 8:30 AM - 8:00 PM. Need directions?"
        
        elif "canteen" in message or "food" in message:
            reply_text = "Main Canteen is near Block A entrance. Also check VT Canteen (Block B) and Ladies Hostel Canteen."
        
        elif "directions" in message or "route" in message:
            reply_text = "Tell me your starting point and destination! Example: 'Block A to Library'"
        
        else:
            reply_text = f"Got it! Working on campus navigation for: {message.title()}. Full AI coming soon!"

        return jsonify({"reply": reply_text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
