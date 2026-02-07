import pickle
import re

# Load your 76% accuracy model
with open('final_high_acc_model.pkl', 'rb') as f:
    model, vectorizer = pickle.load(f)

# Your fixed keywords
SPAM_KEYWORDS = ["urgent", "otp", "bank", "blocked", "prize", "win", "kyc"]

def get_rule_score(text):
    text = text.lower()
    hits = sum(1 for word in SPAM_KEYWORDS if word in text)
    return min(hits / 3, 1.0)

def classify_message(message):
    rule_score = get_rule_score(message)
    
    # ML Prediction
    vec = vectorizer.transform([message.lower()])
    ml_prob = model.predict_proba(vec)[0][1]
    
    # Logic Splitter
    if rule_score >= 0.8 or ml_prob >= 0.7:
        return "SCAMMER", ml_prob
    elif rule_score >= 0.3 or ml_prob >= 0.42:
        return "SUSPICIOUS", ml_prob
    else:
        return "HAM", ml_prob
