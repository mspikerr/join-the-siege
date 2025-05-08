# Document Classifier

![Python CI](https://github.com/mspikerr/join-the-siege/actions/workflows/python-ci.yml/badge.svg)
[![Render](https://img.shields.io/badge/deployed-on%20Render-00c7d4)](https://document-classifier-b3k7.onrender.com)

A Flask-based document classification app with ML and OCR support.

## Running with Docker

You can also run the application using Docker. Ensure you have Docker installed on your system.

1.  **Build the Docker image**:

    Navigate to the root directory of the project (where the `Dockerfile` is located) and run:

    ```bash
    docker build -t document-classifier .
    ```

    * `-t document-classifier`: This tags the image with the name "document-classifier".
    * `.`: This specifies that the build context is the current directory.

2.  **Run the Docker container**:

    To run the built image and map the application's port (5000) to your host machine's port 5000, use:

    ```bash
    docker run -p 5000:5000 document-classifier
    ```

    * `-p 5000:5000`: This maps the host's port 5000 to the container's port 5000.

Visit `http://localhost:5000` in your browser to access the application.

**Using `curl` to test the `/classify_file` endpoint from your host machine**:

Assuming you have a file named `example.pdf` in your current directory:

```bash
curl -F "file=@example.pdf" http://localhost:5000/classify_file
```

**Using `curl` to add a category from your host machine**:

Assuming you have text files named `contract_example1.txt` and `contract_example2.txt` in your current directory:

```bash
curl -X POST http://localhost:5000/add_category \
  -F "category_name=Contract" \
  -F 'keywords=["agreement", "terms", "signature", "clause"]' \
  -F "files=@contract_example1.txt" \
  -F "files=@contract_example2.txt"
  ```


## 🌐 Deployment on Render

This application is deployed on Render and can be accessed at: [https://document-classifier-b3k7.onrender.com](https://document-classifier-b3k7.onrender.com).

Please note that this deployment might experience slower initial loading times due to the free tier. Performance with larger files may also be limited.

Future improvements to the deployment strategy are discussed in the "Future Considerations" section.

---

## 🔮 Future Considerations

Here are some potential areas for future development:

-   **Improved Machine Learning Model**: Explore more advanced NLP models for better classification accuracy.
-   **More File Type Support**: Investigate support for additional document and image formats.
-   **User Interface Enhancements**: Improve the web UI for a more intuitive user experience.
-   **Scalability**: Implement features to handle a larger volume of documents and user requests more efficiently.
-   **Deployment Improvements**: Explore more robust and scalable deployment options beyond the Render free tier (as mentioned earlier), such as cloud platforms with better resource management.
-   **User Authentication**: Add user accounts and authentication for managing categories and data.
-   **More Granular Keyword Control**: Allow users to specify the matching sensitivity for keywords.

---



# Heron Coding Challenge - File Classifier

## Overview

At Heron, we’re using AI to automate document processing workflows in financial services and beyond. Each day, we handle over 100,000 documents that need to be quickly identified and categorised before we can kick off the automations.

This repository provides a basic endpoint for classifying files by their filenames. However, the current classifier has limitations when it comes to handling poorly named files, processing larger volumes, and adapting to new industries effectively.

**Your task**: improve this classifier by adding features and optimisations to handle (1) poorly named files, (2) scaling to new industries, and (3) processing larger volumes of documents.

This is a real-world challenge that allows you to demonstrate your approach to building innovative and scalable AI solutions. We’re excited to see what you come up with! Feel free to take it in any direction you like, but we suggest:


### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?
- How might you extend the classifier with additional technologies, capabilities, or features?


### Part 2: Productionising the Classifier 

- How can you ensure the classifier is robust and reliable in a production environment?
- How can you deploy the classifier to make it accessible to other services and users?

We encourage you to be creative! Feel free to use any libraries, tools, services, models or frameworks of your choice

### Possible Ideas / Suggestions
- Train a classifier to categorize files based on the text content of a file
- Generate synthetic data to train the classifier on documents from different industries
- Detect file type and handle other file formats (e.g., Word, Excel)
- Set up a CI/CD pipeline for automatic testing and deployment
- Refactor the codebase to make it more maintainable and scalable

## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?


## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.app
    ```

4. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```

5. Run tests:
   ```shell
    pytest
    ```

## Submission

Please aim to spend 3 hours on this challenge.

Once completed, submit your solution by sharing a link to your forked repository. Please also provide a brief write-up of your ideas, approach, and any instructions needed to run your solution. 
