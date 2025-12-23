from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # allow all origins

# Do NOT create global client with extra options.
# Just read the key from env when needed.

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json or {}
        message = data.get("message", "")
        role = data.get("role", "Guest")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return jsonify({"error": "OPENAI_API_KEY not set"}), 500

        client = OpenAI(api_key=api_key)

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SCNS AI assistant for NIE Mysore college. "
                        f"Help {role} users with campus navigation, rooms, blocks, floors and facilities. "
                        "Keep answers short and student‑friendly."
                    ),
                },
                {"role": "user", "content": message},
            ],
        )

        return jsonify({"reply": resp.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render sets PORT env var; default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
