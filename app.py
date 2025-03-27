# app.py (Flask backend)
from flask import Flask, request, jsonify
from flask_cors import CORS
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re
import os
import glob
from datetime import datetime

app = Flask(__name__)
CORS(app)

def extract_text_with_all_empty_lines(pdf_path):
    elements = []
    for page_layout in extract_pages(pdf_path):
        page_height = page_layout.height
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                y_pos = page_height - element.y0
                elements.append((text, y_pos))
    elements.sort(key=lambda x: x[1])
    if len(elements) >= 2:
        height_diffs = [elements[i+1][1] - elements[i][1] for i in range(len(elements)-1)]
        avg_line_height = sum(height_diffs) / len(height_diffs)
        min_line_height = avg_line_height * 0.7
    else:
        min_line_height = 10

    result_lines = []
    if not elements:
        return result_lines
    result_lines.append(elements[0][0])
    for i in range(len(elements)-1):
        current_y = elements[i][1]
        next_y = elements[i+1][1]
        gap = next_y - current_y
        if gap > min_line_height:
            empty_lines = int(round(gap / min_line_height)) - 1
            for _ in range(empty_lines):
                result_lines.append("")
        result_lines.append(elements[i+1][0])
    return result_lines

def extract_only_numbers(lines):
    all_numbers = []
    for line in lines:
        numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', line)
        for num in numbers:
            formatted_num = float(num.replace(",", "")) if '.' in num else int(num.replace(",", ""))
            all_numbers.append(formatted_num)
    return all_numbers

def get_latest_pdf(folder_path="model/tymo"):
    """Get the most recent PDF file from the specified folder"""
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        return None
    
    # Get all PDF files in the folder
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        return None
    
    # Get the most recent file based on modification time
    latest_pdf = max(pdf_files, key=os.path.getmtime)
    
    return latest_pdf

@app.route("/get-tymo-values", methods=["POST"])
def get_tymo_values():
    # Get the most recent PDF file
    latest_pdf = get_latest_pdf()
    
    if not latest_pdf:
        return jsonify({"error": "No PDF files found in the tymo folder"}), 404
    
    # Log which file is being processed
    print(f"Processing latest PDF: {latest_pdf}")
    
    lines = extract_text_with_all_empty_lines(latest_pdf)
    numbers = extract_only_numbers(lines)
    
    # Adjust indices to be 0-based
    target_indices = [75, 76, 77, 65, 70, 84, 85, 86, 87, 124, 127]
    
    # For debugging
    print(f"Found {len(numbers)} numbers in the PDF")
    
    result_values = [numbers[i] if i < len(numbers) else None for i in target_indices]
    return jsonify({
        "values": result_values,
        "source_file": os.path.basename(latest_pdf),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(debug=True)
