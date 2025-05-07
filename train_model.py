# train_model.py

import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, f1_score, fbeta_score
from core.preprocess import preprocess_email

# ========== PATHS ==========
DATA_PATH_1 = "data/emails_fixed.csv"
DATA_PATH_2 = "data/my_custom_emails_100.csv"
MODEL_PATH = "models/ml_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"
FEATURE_LIST_PATH = "models/feature_list.txt"

# ========== LOAD & MERGE ==========
df1 = pd.read_csv(DATA_PATH_1)
df2 = pd.read_csv(DATA_PATH_2)
df = pd.concat([df1, df2], ignore_index=True)
df = df.dropna(subset=["label"])

# ========== CHECK REQUIRED COLUMNS ==========
if "text" not in df.columns or "label" not in df.columns:
    raise ValueError("CSV files must contain 'text' and 'label' columns.")

# ========== PREPROCESS ==========
df["clean_text"] = df["text"].apply(preprocess_email)
df["clean_text"] = df["clean_text"].astype(str)
df = df[df["clean_text"].str.strip().astype(bool)]

if df.empty:
    raise ValueError("❌ All clean_text rows are empty. Check your dataset preprocessing.")

# ========== VECTORIZE ==========
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["clean_text"]).toarray()
y = df["label"]

# ========== SAVE VECTORIZER ==========
os.makedirs("models", exist_ok=True)
with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

# ========== SAVE FEATURE LIST ==========
with open(FEATURE_LIST_PATH, "w", encoding="utf-8") as f:
    for feat in vectorizer.get_feature_names_out():
        f.write(feat + "\n")

# ========== TRAIN ==========
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ========== EVALUATE ==========
y_pred = model.predict(X_test)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Safe", "Fraudulent"]))

# 🎯 F1, F2, F3 Scores
f1 = f1_score(y_test, y_pred, pos_label=1)
f2 = fbeta_score(y_test, y_pred, beta=2, pos_label=1)
f3 = fbeta_score(y_test, y_pred, beta=3, pos_label=1)

print(f"\n🎯 F1 Score (balanced):           {f1:.2f}")
print(f"🎯 F2 Score (recall focused):     {f2:.2f}")
print(f"🎯 F3 Score (very recall focused): {f3:.2f}")

# ========== SAVE MODEL ==========
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model trained and saved to:", MODEL_PATH)
print("📦 Vectorizer saved to:", VECTORIZER_PATH)
print("📄 Feature list saved to:", FEATURE_LIST_PATH)
