import pickle
import os
import numpy as np

MODEL_PATH = "models/ml_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
FEATURE_LIST_PATH = "models/feature_list.txt"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(FEATURE_LIST_PATH, "r", encoding="utf-8") as f:
    feature_list = [line.strip() for line in f.readlines()]

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
    return prediction, confidence

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer
