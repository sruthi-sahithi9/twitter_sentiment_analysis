import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import pickle
import os

print("Loading dataset...")
dataset_path = r'C:\Users\User\OneDrive\Desktop\Twitter Sentiments.csv'
df = pd.read_csv(dataset_path)

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for word in r:
        input_txt = re.sub(word, "", input_txt)
    return input_txt

print("Cleaning data...")
# Remove twitter handles
df['clean_tweet'] = np.vectorize(remove_pattern)(df['tweet'], "@[\w]*")

# Remove special characters
df['clean_tweet'] = df['clean_tweet'].str.replace("[^a-zA-Z#]", " ", regex=True)

# Remove short words
df['clean_tweet'] = df['clean_tweet'].apply(
    lambda x: " ".join([w for w in str(x).split() if len(w) > 3])
)

print("Training TF-IDF Vectorizer...")
tfidf = TfidfVectorizer(stop_words='english')
X = tfidf.fit_transform(df['clean_tweet'])

print("Training SVM Model...")
svm_model = LinearSVC()
# We train on the entire dataset for the final model
svm_model.fit(X, df['label'])

print("Saving models...")
# Output paths relative to where script is run
with open("svm_model.pkl", "wb") as f:
    pickle.dump(svm_model, f)
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(tfidf, f)
    
print("Done!")
