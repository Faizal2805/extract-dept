efrom flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins

# Define department and year mappings
department_keywords = {
    r"\bartificial intelligence and data science\b": "AI&DS",
    r"\bartificial intelligence and datascience\b": "AI&DS",
    r"\baids\b": "AI&DS",
    r"\bAI DS\b": "AI&DS",
    r"\bai ds\b": "AI&DS",
    r"\bAI&DS\b": "AI&DS",
    r"\bai&ds\b": "AI&DS",
    r"\bcomputer science\b": "CSE",
    r"\bcs\b": "CSE",
    r"\belectronics and communication\b": "ECE",
    r"\bece\b": "ECE"
}

year_keywords = {
    r"\bfirst year\b": "I",
    r"\bsecond year\b": "II",
    r"\bthird year\b": "III",
    r"\bfourth year\b": "IV",
    r"\b1st year\b": "I",
    r"\b2nd year\b": "II",
    r"\b3rd year\b": "III",
    r"\b4th year\b": "IV"
}

# Function to extract Department and Year from text
def extract_department_year(text):
    text = text.strip().lower()
    extracted_department = None
    extracted_year = None

    for pattern, value in department_keywords.items():
        if re.search(pattern, text):
            extracted_department = value
            break

    for pattern, value in year_keywords.items():
        if re.search(pattern, text):
            extracted_year = value
            break

    return extracted_department, extracted_year

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    text = data.get("text", "").strip()
    
    department, year = extract_department_year(text)
    
    if department and year:
        return jsonify({"department": department, "year": year})
    else:
        return jsonify({"error": "Department or Year not found in text"}), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Use Render’s default port 5000
    app.run(host="0.0.0.0", port=port, debug=False)
