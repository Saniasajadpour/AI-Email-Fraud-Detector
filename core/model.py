import pickle
import os
import numpy as np

MODEL_PATH = "models/ml_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
FEATURE_LIST_PATH = "models/feature_list.txt"

# === Load Model and Vectorizer ===
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(FEATURE_LIST_PATH, "r", encoding="utf-8") as f:
    feature_list = [line.strip() for line in f.readlines()]


def fraud_boost_layer(text: str, score: float) -> float:
    """
    Boosts fraud probability based on rule-based triggers in the email text.
    Only applied when ML model predicts fraud (label == 1).
    """
    boost_keywords = [
        "verify your account", "click here", "final warning", "suspended", "login to resolve",
        "reset your password", "you have been selected", "winner", "claim your reward",
        "paypal", "microsoft", "amazon", "netflix", "dhl", "urgent", "security alert",
        "account locked", "confirm identity", "free iphone", "identity verification",
        "unauthorized access", "payment failure", "action required"
    ]

    boost_score = score
    lowered = text.lower()
    for keyword in boost_keywords:
        if keyword in lowered:
            boost_score += 0.05  # Add 5% per trigger keyword

    return min(boost_score, 1.0)


def predict_email(cleaned_text: str) -> tuple:
    """
    Predicts whether the input email text is fraudulent.
    Returns the label (0 or 1) and the confidence score.
    """
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

    # Apply boost logic if prediction is fraud
    if prediction == 1:
        confidence = fraud_boost_layer(cleaned_text, confidence)

    return prediction, confidence


def load_model():
    """
    Reloads and returns the ML model and vectorizer.
    """
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer
