from flask import Flask, request, jsonify, render_template
from src.classifier import classify_file
import os
import json
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from src.classifier import save_category
from src.classifier import load_categories

app = Flask(__name__)

@app.route("/categories", methods=["GET"])
def get_categories():
    try:
        categories = load_categories()
        return jsonify({"categories": list(categories.keys())})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

TRAINING_DIR = "training_docs"

@app.route("/add_category", methods=["POST"])
def add_category():
    category_name = request.form["category_name"]
    keywords = json.loads(request.form["keywords"])
    files = request.files.getlist("files")

    # Save keywords
    save_category(category_name, keywords)

    # Create new training_docs subfolder
    category_dir = os.path.join(TRAINING_DIR, secure_filename(category_name))
    os.makedirs(category_dir, exist_ok=True)

    # Save uploaded .txt files
    for file in files:
        if file and file.filename.endswith(".txt"):
            file_path = os.path.join(category_dir, secure_filename(file.filename))
            file.save(file_path)

    # Retrain model by calling train.py
    try:
        subprocess.run(["python", "src/train.py"], check=True)
    except subprocess.CalledProcessError:
        return jsonify({"error": "Training failed"}), 500

    return jsonify({"message": "Category added and model retrained!"})

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'txt', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist('file')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    results = []

    for file in files:
        if file.filename == '':
            results.append({"error": "No selected file"})
            continue

        if not allowed_file(file.filename):
            results.append({"error": f"File type not allowed: {file.filename}"})
            continue

        try:
            file_class = classify_file(file)
            results.append({"file_name": file.filename, "file_class": file_class})
        except Exception as e:
            results.append({"file_name": file.filename, "error": str(e)})

    # Check if the request expects HTML (form upload) or JSON (API)
    if request.accept_mimetypes['text/html'] > request.accept_mimetypes['application/json']:
        return render_template('index.html', results=results)
    else:
        return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
