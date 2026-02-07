#Run By Google Colab and the model is saved as final_high_acc_model.pkl in the folder

!pip install kagglehub

import kagglehub
import pandas as pd
import re
import glob
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from google.colab import files

# 1. Download Dataset
path = kagglehub.dataset_download("vinit119/sms-scam-detection-dataset-merged")
csv_file = glob.glob(f"{path}/*.csv")[0]
df = pd.read_csv(csv_file)

# 2. Intelligent Cleaning Function
def clean_text(text):
    text = str(text).lower() # Lowercase everything
    text = re.sub(r'http\S+|www\S+|https\S+', 'URL', text, flags=re.MULTILINE) # Normalize links
    text = re.sub(r'\d+', 'NUMBER', text) # Normalize numbers
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    return text

# Apply cleaning and drop empty rows
df = df.dropna(subset=['text', 'label'])
df['text'] = df['text'].apply(clean_text)
df['target'] = df['label'].map({'ham': 0, 'spam': 1, 'scam': 1})

# Add this BEFORE splitting your data
df['message_len'] = df['text'].apply(len)

# You will need to use a 'ColumnTransformer' to combine text features and length
# 3. Split Data
# Ensure 'target' column has no NaN values and is of integer type before splitting
df.dropna(subset=['target'], inplace=True)
df['target'] = df['target'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['target'], test_size=0.2, random_state=42, stratify=df['target']
)

import string

# 1. Create new numerical features
def get_features(df):
    df['char_count'] = df['text'].apply(len)
    df['word_count'] = df['text'].apply(lambda x: len(x.split()))
    df['punc_count'] = df['text'].apply(lambda x: len([c for c in x if c in string.punctuation]))
    return df

df = get_features(df)

# 2. Update the Vectorizer to ignore rare noise
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 3),
    max_df=0.8,  # Ignore words in >80% of messages
    min_df=10    # Ignore words that appear fewer than 10 times
)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 5. Optimized Random Forest
# Using 300 trees for more stability and better accuracy
model = RandomForestClassifier(
    n_estimators=300,
    class_weight='balanced',
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1 # Uses all CPU cores for speed
)

model.fit(X_train_tfidf, y_train)

# 7. Save and Download
with open('final_high_acc_model.pkl', 'wb') as f:
    pickle.dump((model, vectorizer), f)
files.download('final_high_acc_model.pkl')

# 6. Apply Intelligent Threshold
probs = model.predict_proba(X_test_tfidf)[:, 1]
y_pred = (probs >= 0.42).astype(int)

print(f"New Accuracy: {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred))

from sklearn.metrics import classification_report, confusion_matrix

# 1. Get the raw probabilities for the Scam class (index 1)
y_probs = model.predict_proba(X_test_tfidf)[:, 1]

# 2. Apply your Intelligent Threshold of 0.42
y_pred_intelligent = (y_probs >= 0.42).astype(int)

# 3. Print the results to see the improvement
print("--- Results with Intelligent Threshold (0.42) ---")
print(classification_report(y_test, y_pred_intelligent))

# 1. Create a DataFrame of the test results
results = pd.DataFrame({
    'Message': X_test,
    'Actual': y_test,
    'Predicted': y_pred
})

# 2. Filter for mistakes
errors = results[results['Actual'] != results['Predicted']]
print("Total Errors:", len(errors))
print(errors.head(10))
