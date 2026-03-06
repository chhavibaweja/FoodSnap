from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os, json, re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# === Setup Flask ===
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

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
@app.route("/history")
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
        Respond ONLY in valid JSON format:
        {{
          "calories": "210 kcal",
          "protein": "5 g",
          "carbs": "27 g",
          "fat": "8 g"
        }}
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        reply = response.text.strip()

        print("Gemini raw reply:", reply)

        clean_reply = re.sub(r"^```(?:json)?|```$", "", reply).strip()

        try:
            nutrition_data = json.loads(clean_reply)
        except:
            nutrition_data = {"raw_response": clean_reply}

        return jsonify(nutrition_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# === Run the app ===
if __name__ == "__main__":
    app.run(debug=True)