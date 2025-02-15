from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins

# Define department and year mappings
department_keywords = {
    "artificial intelligence and data science": "AI&DS",
    "artificial intelligence and datascience": "AI&DS",
    "aids": "AI&DS",
    "Artificial Intelligence and Data Science": "AI&DS",
    "Artificial Intelligence and Datascience": "AI&DS",
    "AI DS": "AI&DS",
    "ai ds": "AI&DS",
    "AI&DS": "AI&DS",
    "ai&ds": "AI&DS",
    "Artificial Intelligence and DataScience": "AI&DS",
    "computer science": "CSE",
    "cs": "CSE",
    "electronics and communication": "ECE",
    "ece": "ECE"
}

year_keywords = {
    "first year": "I",
    "second year": "II",
    "Second year": "II",
    "third year": "III",
    "Third year": "III",
    "fourth year": "IV",
    "Fourth year": "IV",
    "1st year": "I",
    "2nd year": "II",
    "3rd year": "III",
    "4th year": "IV"
}

# Function to extract Department and Year from text
def extract_department_year(text):
    extracted_department = None
    extracted_year = None

    for key, value in department_keywords.items():
        if key in text.lower():
            extracted_department = value
            break

    for key, value in year_keywords.items():
        if key in text.lower():
            extracted_year = value
            break

    return extracted_department, extracted_year

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    text = data.get("text", "")
    
    department, year = extract_department_year(text)
    
    if department and year:
        return jsonify({"department": department, "year": year})
    else:
        return jsonify({"error": "Department or Year not found in text"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
