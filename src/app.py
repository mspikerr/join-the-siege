from flask import Flask, request, jsonify

from src.classifier import classify_file
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'txt', 'docx', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/classify_file', methods=['POST'])
def classify_file_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    #file = request.files['file']
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

        file_class = classify_file(file)  # Classify the file
        results.append({"file_name": file.filename, "file_class": file_class})

    return jsonify({"results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
