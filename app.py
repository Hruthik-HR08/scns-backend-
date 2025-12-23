import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# allow all origins (Netlify frontend, college site, etc.)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        message = data.get("message", "")
        role = data.get("role", "Guest")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # SIMPLE ECHO REPLY FOR TESTING
        reply_text = f"Echo from SCNS backend ({role}): {message}"
        return jsonify({"reply": reply_text})
    except Exception as e:
        # if anything unexpected happens, return an error field
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render sets PORT automatically; default 5000 for local runs
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
