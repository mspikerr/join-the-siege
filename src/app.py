from flask import Flask, request, jsonify, render_template
from src.classifier import classify_file

app = Flask(__name__)

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
