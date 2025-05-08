import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Path to your sample documents
data_dir = "training_docs"

texts = []
labels = []

# Walk through all subdirectories
for root, _, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            label = os.path.basename(root)  # Use the folder name as the label
            with open(file_path, "r", encoding="utf-8") as f:
                texts.append(f.read())
                labels.append(label)

# Convert text data to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X, labels)

# Save the model and vectorizer to disk
model_dir = os.path.join("src", "models")
os.makedirs(model_dir, exist_ok=True)

with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
    pickle.dump(clf, f)

with open(os.path.join(model_dir, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved to src/models/")
