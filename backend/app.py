from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, json
from dotenv import load_dotenv
import google.generativeai as genai  # Gemini import
import os 
from app import app 

load_dotenv()

# === Setup paths for templates and static folders ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    # template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
    # static_folder=os.path.join(BASE_DIR, "frontend", "static")
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
)
CORS(app)

# === Configure Gemini API ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Home route ===
@app.route("/")
def home():
    return render_template("index.html")

# === About page ===

@app.route("/about")
def about():
    return render_template("about.html")

# === History page ===

@app.route('/history')
def history():
    return render_template("history.html")

# === Analyze food route ===
@app.route("/analyze", methods=["POST"])
def analyze_food():
    data = request.get_json()
    food_name = data.get("food", "").strip()

    if not food_name:
        return jsonify({"error": "Please provide a food name"}), 400

    try:
        prompt = f"""
        You are a food nutrition expert. Give approximate nutritional information for "{food_name}".
        Respond ONLY in valid JSON format, like this (no markdown, no text outside JSON):
        {{
          "calories": "210 kcal",
          "protein": "5 g",
          "carbs": "27 g",
          "fat": "8 g"
        }}
        """

        # --- Call Gemini ---
        model = genai.GenerativeModel("gemini-2.5-flash")  
        response = model.generate_content(prompt)
        reply = response.text.strip()

        print("Gemini raw reply:\n", reply)  # print the selected output in your terminal

        # Try parsing JSON response
        import re, json

        # Remove Markdown code block if present (```json ... ```)
        clean_reply = re.sub(r"^```(?:json)?|```$", "", reply, flags=re.MULTILINE).strip()
        # Extract JSON from the cleaned reply
        json_text = re.search(r"\{.*\}", clean_reply, re.DOTALL)
        
        try:
            nutrition_data = json.loads(reply)
        except json.JSONDecodeError:
            nutrition_data = {"raw_response": reply}

        return jsonify(nutrition_data)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


# === Run the app ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)