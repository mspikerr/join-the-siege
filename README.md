# Document Classifier

![Python CI](https://github.com/mspikerr/join-the-siege/actions/workflows/python-ci.yml/badge.svg)
[![Render](https://img.shields.io/badge/deployed-on%20Render-00c7d4)](https://document-classifier-b3k7.onrender.com)

A Flask-based document classification app with ML and OCR support.

## Deployment on Render

This application is deployed on Render and can be accessed at: [https://document-classifier-b3k7.onrender.com](https://document-classifier-b3k7.onrender.com).

Please note that this deployment might experience slower initial loading times due to the free tier. Performance with larger files may also be limited. The preferred method is to run the app locally using Docker. Those steps are listed in the next section. 

Future improvements to the deployment strategy are discussed in the "Future Considerations" section.

## Running with Docker (recommended)

You can also run the application using Docker. Ensure you have Docker installed on your system.

1.  **Clone the repository**:


    ```bash
    git clone https://github.com/mspikerr/join-the-siege
    cd join-the-siege
    ```

2.  **Build the Docker image**:


    ```bash
    docker build -t document-classifier .
    ```

3.  **Run the app in the Docker container**:

    To run the built image and map the application's port (5000) to your host machine's port 5000, use:

    ```bash
    docker run -p 5000:5000 document-classifier
    ```

    Once the container is running, you have two ways to interact with the application:

    ### a. Use the web interface (recommended)

    Visit [http://localhost:5000](http://localhost:5000) in your browser to access the user-friendly upload and classification tool.

    ### b. Use `curl` from the command line

    - **Classify a file**  
      Assuming you have a file named `example.pdf` in your current directory:

      ```bash
      curl -F "file=@example.pdf" http://localhost:5000/classify_file
      ```

    - **Add a new category**  
      Assuming you have text files named `contract_example1.txt` and `contract_example2.txt`:

      ```bash
      curl -X POST http://localhost:5000/add_category -F "category_name=Contract" -F 'keywords=["agreement", "terms", "signature", "clause"]' -F "files=@contract_example1.txt" -F "files=@contract_example2.txt"
      ```

    Make sure the files you're referencing exist in your current directory when running the `curl` commands.


## Project Overview

This project is a content-based document classification tool designed to automatically categorize uploaded files using a machine learning model trained on labeled text samples. This tool currently supports the following file types: PDF, PNG, JPG, TXT, DOCX, and XLSX. The application features a web interface and API endpoints that allow users to upload documents for classification, as well as extend the model by adding new categories with sample files and keywords. It is designed for rapid prototyping and easy deployment via Docker.

### Classification Flow

When a document is uploaded via the `/classify_file` endpoint, the classification process follows this flow:

1. **Extract Text**  
   The app extracts raw text content from the uploaded file using various file-type-aware methods. For PDF files, it uses the pdfminer library to extract text. For images, it utilizes OCR (Optical Character Recognition) with pytesseract to convert any text present in the image into machine-readable format. For .docx files, it reads the text from paragraphs using the python-docx library. For .xlsx files, it extracts text by reading the content of each cell in the spreadsheet using openpyxl. If the file is a plain text file, the raw content is directly decoded. This ensures that the system can process a variety of file types, including scanned images and different document formats.

2. **Fuzzy Keyword Matching**  
   It first attempts to classify the document by matching the extracted text with predefined keyword sets for each category using fuzzy string comparison.

3. **ML Model Fallback**  
   If keyword matching is inconclusive or below a confidence threshold, the system falls back to a trained machine learning model (a Naive Bayes classifier with TF-IDF features) to predict the category.

4. **Return Result**  
   The application returns the predicted category.

This two-tiered approach increases reliability by favoring simple, interpretable logic first, then falling back to the model when needed.

### Add Category Flow

When a new category is submitted via the `/add_category` endpoint, the application performs the following steps:

1. **Receive Category Data**  
   The request includes a category name, a list of keywords (used for fuzzy matching), and one or more example documents for training.

2. **Check for Similarity Conflicts**  
   Before saving, the system checks whether the submitted category name or any of its keywords are too similar to existing ones using fuzzy matching. If conflicts are found, the request is rejected with a list of specific conflicts and no changes are made.

3. **Store Keywords**  
   If no conflicts are found, the keywords are saved to an internal mapping used by the fuzzy matcher during classification.

4. **Retrain Model**  
   The example documents are vectorized and appended to the training dataset. The TF-IDF vectorizer and Naive Bayes model are retrained with the updated data.

5. **Update Model Files**  
   The updated model and vectorizer are saved to disk (`src/models/model.pkl` and `vectorizer.pkl`) for immediate use in subsequent classifications.


### File Structure & Key Components

Below is a quick overview of the most relevant files and directories:

- **`app.py`**  
  The main Flask application. Defines routes for uploading, classifying, and extending categories via API.

- **`classifier.py`**  
  Contains the core logic for file classification, including text extraction from different file types, fuzzy matching with predefined keywords, and using a machine learning model for classification when necessary.

- **`train.py`**  
  A standalone script used to train the initial machine learning model from labeled text documents.

- **`src/models/`**  
  Contains the saved `model.pkl` and `vectorizer.pkl` which are generated by train.py and used by the application for classification..

- **`training_docs/`**  
  Includes sample training documents organized by category (e.g., invoices, bank statements).

- **`Dockerfile`**  
  Defines the container configuration to run the app in an isolated Docker environment.

- **`.github/workflows/python-ci.yml`** 
  Defines the GitHub Actions workflow for running tests on every push or pull request to the `main` branch, ensuring code quality through automated CI.

  

## Limitations and Future Considerations

While the current version of this document classifier is functional, there are several areas where it can be improved. Below are some of the key limitations and future considerations:

### 1. **Improve Deployment Beyond Free Tier on Render**  
The application is currently deployed using the free tier of [Render](https://render.com), which introduces limitations such as cold starts, limited uptime, and reduced compute power. Future improvements include moving to a more robust cloud platform or upgrading to a paid tier for improved reliability, performance, and autoscaling capabilities. Implementing CI/CD with GitHub Actions and potentially container orchestration with Kubernetes would further streamline and strengthen the deployment process.

### 2. **Comprehensive Testing**  
Beyond basic functional testing, more thorough unit and integration tests are needed. These should cover edge cases, different file formats, error handling, and performance under load. This will ensure the system is reliable and robust in real-world use cases.

### 3. **Add Synthetic .txt Files for User to Skip Upload**  
The current "add category" functionality requires users to upload `.txt` files manually. In the future, it could support generating synthetic `.txt` files from predefined templates or sample data, allowing users to add categories without needing to manually upload files, streamlining the process.

### 4. **Train with More Data and File Types**  
The model is presently trained on a limited number of `.txt` files. To improve accuracy, the system should be trained on a broader, more diverse dataset that includes `.pdf`, `.docx`, `.xlsx`, and image-based documents. This will enhance generalization and allow for more accurate predictions across formats.

### 5. **Confidence Score and Human Review Loop**  
Introducing a confidence score for each classification would help surface uncertain predictions. Documents falling below a configurable confidence threshold could be flagged for human review, creating a feedback loop that enhances trust and allows users to refine or override the model’s decision.

### 6. **Optimizing Performance for Large Files**  
For scalability, the application will need better handling larger files or a higher volume of concurrent requests. This could involve asynchronous processing, chunked reads, or background task queues to avoid blocking the main thread and improve responsiveness.

### 7. **Scalability and Load Balancing**  
To support increased demand, future versions should incorporate horizontal scaling and load balancing, possibly through cloud-native platforms like AWS ECS, Google Cloud Run, or Kubernetes, to ensure the app performs well under concurrent usage.

### 8. **Use LLMs or More Advanced NLP Models**  
The current classification approach relies on traditional machine learning with a vectorizer and basic model. In the future, the system could be enhanced using more advanced NLP models like BERT, RoBERTa, or large language models (LLMs) such as GPT. These models can better capture semantic meaning and context, enabling more accurate classification — even for unseen or nuanced categories. LLMs could also enable zero-shot or few-shot classification without requiring retraining.
