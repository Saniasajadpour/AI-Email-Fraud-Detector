import pickle
import os
import numpy as np

MODEL_PATH = "models/ml_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
FEATURE_LIST_PATH = "models/feature_list.txt"

# Load model components
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(FEATURE_LIST_PATH, "r", encoding="utf-8") as f:
    feature_list = [line.strip() for line in f.readlines()]


# 🔴 Advanced fraud pattern detection
def fraud_boost_layer(text: str, base_score: float) -> float:
    text = text.lower()

    categories = {
        "social": [
            "verify your account", "login now", "reset password", "click to reactivate",
            "account has been locked", "you must confirm", "authentication required",
            "verify immediately", "please confirm", "validate your credentials"
        ],
        "financial": [
            "billing failure", "payment declined", "invoice overdue", "refund request",
            "credit card was declined", "account charged", "unauthorized transaction",
            "bank login", "billing address issue", "pending charge"
        ],
        "brands": [
            "paypal", "netflix", "dhl", "amazon", "microsoft", "apple", "facebook",
            "instagram", "fedex", "bank of america", "wells fargo", "visa", "mastercard"
        ],
        "urgency": [
            "urgent action required", "last warning", "immediate suspension", "final notice",
            "act now", "suspend your account", "failure to comply", "you’ll be blocked",
            "24-hour deadline", "emergency response needed"
        ],
        "links": [
            "http://", "https://", "click here", "verify now", "access secure portal",
            "sign in below", "update account link", "re-enter password", "login gateway"
        ],
        "visual": [
            "💰", "‼️", "🔥", "🎁", "👇", "👀", "🤑", "act fast", "win a free",
            "limited time only", "get yours now", "click below", "guaranteed winner"
        ]
    }

    weights = {
        "social": 0.035,
        "financial": 0.04,
        "brands": 0.025,
        "urgency": 0.045,
        "links": 0.05,
        "visual": 0.02
    }

    for category, phrases in categories.items():
        for phrase in phrases:
            if phrase in text:
                base_score += weights[category]

    return min(base_score, 1.0)


# 🟢 Safe behavior and formal business logic
def safe_reduce_layer(text: str, safe_score: float, fraud_score: float) -> tuple:
    text = text.lower()

    categories = {
        "structure": [
            "meeting agenda", "project update", "team sync", "calendar invite", "follow-up email",
            "status report", "attached draft", "weekly meeting", "presentation slides",
            "q2 report", "timeline", "attached spreadsheet", "slide deck enclosed"
        ],
        "polite": [
            "thank you for your time", "appreciate your help", "happy to assist", "please let me know",
            "looking forward", "glad to hear from you", "have a great day", "feel free to reach out",
            "just a quick reminder", "as discussed", "hope this helps"
        ],
        "internal": [
            "hr policy", "company announcement", "employee handbook", "approved request",
            "leave application", "internal draft", "monthly payroll", "official document",
            "timesheet attached", "reimbursement form", "training session", "welcome package"
        ],
        "closings": [
            "best regards", "sincerely", "kind regards", "cheers", "talk soon",
            "respectfully", "cc’d for visibility", "thank you again", "see you at the meeting"
        ]
    }

    weights = {
        "structure": 0.025,
        "polite": 0.02,
        "internal": 0.03,
        "closings": 0.015
    }

    for category, phrases in categories.items():
        for phrase in phrases:
            if phrase in text:
                fraud_score -= weights[category]
                safe_score += weights[category]

    # Limit adjustments
    fraud_score = max(0.0, fraud_score)
    safe_score = min(1.0, safe_score)

    # Flatten borderline false positives
    if safe_score > 0.7 and fraud_score < 0.35 and abs(fraud_score - safe_score) < 0.3:
        fraud_score = round(fraud_score * 0.7, 3)
        safe_score = round(1.0 - fraud_score, 3)

    return safe_score, fraud_score


# 🔍 Unified prediction logic
def predict_email(cleaned_text: str) -> tuple:
    if not cleaned_text.strip():
        return 0, 0.0

    vectorized_input = vectorizer.transform([cleaned_text])
    vectorized_array = vectorized_input.toarray()

    current_features = vectorizer.get_feature_names_out()
    full_vector = np.zeros((1, len(feature_list)))

    feature_index = {word: i for i, word in enumerate(current_features)}
    for i, word in enumerate(feature_list):
        if word in feature_index:
            full_vector[0, i] = vectorized_array[0, feature_index[word]]

    prediction = model.predict(full_vector)[0]
    confidence = model.predict_proba(full_vector)[0][prediction]

    fraud_score = confidence if prediction == 1 else 1 - confidence
    safe_score = 1 - fraud_score

    fraud_score = fraud_boost_layer(cleaned_text, fraud_score)
    safe_score, fraud_score = safe_reduce_layer(cleaned_text, safe_score, fraud_score)

    final_label = 1 if fraud_score > safe_score else 0
    final_confidence = max(fraud_score, safe_score)

    return final_label, round(final_confidence, 4)


# 🔄 Exportable load function
def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer
