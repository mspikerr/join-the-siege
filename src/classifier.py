# from src.utils.pdf_extraction import extract_text_from_pdf
# from src.utils.ocr import extract_text_from_image
# from src.utils.file_type_detection import get_mime_type
# from src.utils.text_classification import classify_text
# from werkzeug.datastructures import FileStorage



# def classify_file(file: FileStorage):
#     filename = file.filename.lower()
#     file_bytes = file.read()
#     mime_type = get_mime_type(file_bytes)

#     if mime_type == "application/pdf":
#         text = extract_text_from_pdf(file_bytes)
#     elif mime_type.startswith("image/"):
#         text = extract_text_from_image(file_bytes)
#     else:
#         return "unsupported format"

#     return classify_text(text)


from werkzeug.datastructures import FileStorage
from pdfminer.high_level import extract_text
from docx import Document
import openpyxl
from PIL import Image
import pytesseract
import magic
import io
import pickle
import os

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

#TO DO: print statement to see if its actually falling back to ML
# Load ML model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

def extract_text_from_pdf(file_bytes):
    with open("temp.pdf", "wb") as f:
        f.write(file_bytes)
    return extract_text("temp.pdf")

def extract_text_from_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image)

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_xlsx(file_bytes):
    workbook = openpyxl.load_workbook(io.BytesIO(file_bytes))
    text = ""
    for sheet in workbook.sheetnames:
        worksheet = workbook[sheet]
        for row in worksheet.iter_rows(values_only=True):
            text += " ".join([str(cell) for cell in row if cell]) + "\n"
    return text

def classify_text(text):
    text = text.lower()
    if "drivers license" in text or "driver's license" in text:
        print("not ML: drivers")
        return "drivers_licence"
    if "bank account" in text or "statement" in text:
        print("not ML: bank statement")
        return "bank_statement"
    if "invoice" in text or "amount due" in text:
        print("not ML: invoice")
        return "invoice"
    return "unknown file"

def ml_classify_text(text):
    X = vectorizer.transform([text])
    prediction = model.predict(X)
    return prediction[0]

def classify_file(file: FileStorage):
    filename = file.filename.lower()
    file_bytes = file.read()
    mime_type = magic.from_buffer(file_bytes, mime=True)

    if mime_type == "application/pdf":
        text = extract_text_from_pdf(file_bytes)
    elif mime_type.startswith("image/"):
        text = extract_text_from_image(file_bytes)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    elif filename.endswith(".xlsx"):
        text = extract_text_from_xlsx(file_bytes)
    elif mime_type == "text/plain":
        text = file_bytes.decode("utf-8")
    else:
        return "unsupported format"

    label = classify_text(text)
    if label == "unknown file":
        print("falling back to ML model")
        label = ml_classify_text(text)
    return label
