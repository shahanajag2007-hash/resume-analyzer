from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from openai import OpenAI


# -------------------
# Setup
# -------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

# -------------------
# Home
# -------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------
# Analyze Resume
# -------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    resume_text = request.json.get("resume", "")

    prompt = f"""
You are an expert resume reviewer and interviewer.

TASKS:
1. Convert the resume into clear, professional resume bullet points.
2. For EACH bullet:
   - Decide if it is provable in an interview.
   - If NOT provable, explain what is missing.
   - Give a clear suggestion to improve it.
3. Generate 2–3 realistic interviewer questions.

RETURN JSON ONLY in this format:

{{
  "bullets": [
    {{
      "text": "resume bullet",
      "provable": true/false,
      "reason": "why not provable (empty if provable)",
      "suggestion": "how the user can fix or improve this bullet"
    }}
  ],
  "questions": [
    "question 1",
    "question 2"
  ]
}}

RESUME:
{resume_text}
"""


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return jsonify(json.loads(content))
    except:
        return jsonify({"error": "Invalid AI response", "raw": content}), 500
@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer():
    question = request.json.get("question", "")
    answer = request.json.get("answer", "")

    prompt = f"""
Evaluate the following interview answer.

QUESTION:
{question}

ANSWER:
{answer}

Say if the answer is:
- Strong
- Average
- Weak

Explain briefly what is missing or how to improve.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return jsonify({
        "evaluation": response.choices[0].message.content
    })

# -------------------
# Run App
# -------------------
if __name__ == "__main__":
    app.run()
