import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Path to your sample documents
data_dir = "sample_docs"

texts = []
labels = []

# Map folder names or file prefixes to labels
for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        label = filename.split("_")[0]  # invoice_1.txt -> 'invoice'
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            texts.append(f.read())
            labels.append(label)

# Convert text data to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X, labels)

# Save the model and vectorizer to disk
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved as model.pkl and vectorizer.pkl")
