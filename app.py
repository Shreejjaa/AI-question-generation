from flask import Flask, render_template, request
import google.generativeai as genai
import os
import markdown

# API Key (best practice: set via environment variable, fallback to direct key for testing)
API_KEY = os.getenv("GOOGLE_API_KEY", "Shreeja Sarkar")
MODEL_ID = "gemini-1.5-flash"  # Updated to match current API format

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name=MODEL_ID)

# Flask app
app = Flask(__name__)

# Function to create the prompt
def generate_prompt(subject, chapter, num_q, difficulty, qtype):
    return (
        f"Generate {num_q} {difficulty}-level {qtype} questions "
        f"for the subject '{subject}', chapter '{chapter}'.\n\n"
        "Number the questions clearly."
    )

# Home route
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Generate questions route
@app.route("/generate", methods=["POST"])
def generate():
    subject    = request.form["subject"]
    chapter    = request.form["chapter"]
    num_q      = request.form["num_questions"]
    difficulty = request.form["difficulty"]
    qtype      = request.form["qtype"]

    prompt = generate_prompt(subject, chapter, num_q, difficulty, qtype)

    try:
        # Generate content using Gemini
        response = model.generate_content(prompt)
        questions_md = response.text

        # Convert Markdown to HTML
        questions_html = markdown.markdown(
            questions_md,
            extensions=["fenced_code", "nl2br"]
        )
    except Exception as e:
        questions_html = f"<p><strong>Error calling Gemini API:</strong> {e}</p>"

    return render_template("index.html", questions=questions_html)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
