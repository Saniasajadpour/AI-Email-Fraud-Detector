# 📧 Email Fraud Detection System using Machine Learning

Hi! This is a machine learning-based desktop app I developed to detect fraudulent emails — including phishing, spam, and social engineering attacks. The system works **entirely offline**, with a beautiful PyQt6 user interface, and analyzes email content using both an ML model and custom rule-based logic.

This project was built for my bachelor’s thesis at the European University of Armenia (2025), and I’m proud to say it’s fully functional and ready to use.

---

## 🔍 What the App Does

- Detects email fraud using a trained **Logistic Regression** model
- Supports **pasted email text**, as well as **uploaded `.txt` and `.eml` files**
- Displays a clean **pie chart** showing fraud vs safe probability
- Explains the reasoning behind the prediction
- Provides simple, clear advice on what action to take
- Works **completely offline**
- Has a **dark/light mode toggle** with smooth animated buttons
- Includes a smart **fraud booster** to catch obvious scam patterns

---

## 🧠 How It Works: Hybrid Architecture

This system uses a **hybrid approach** to detect fraudulent emails, combining both machine learning and rule-based intelligence:

1. **ML Model (Supervised Learning)**  
   The core model is a **Logistic Regression** classifier trained using **TF-IDF** vectorization. It learns from a labeled dataset of fraudulent and legitimate emails, detecting statistical patterns and keywords associated with scams.

2. **Post-Model Rule Layer**  
   After the ML prediction, the system applies two intelligent logic layers:
   - 🔴 `fraud_boost_layer()` increases fraud probability if scam-like patterns are found (e.g., “verify account”, “click here”, “account suspended”, etc.).
   - 🟢 `safe_reduce_layer()` lowers the fraud score if professional and trustworthy phrases are detected (e.g., “attached is the agenda”, “team meeting”, “best regards”, etc.).

This hybrid setup improves accuracy, reduces false positives, and maintains high interpretability. It's ideal for desktop use and academic review because it balances machine learning with human-readable decision logic.

---

## ⚙️ How to Run

You have two options:

### 1. Run the `.exe` (no setup needed)
A fully built Windows `.exe` is included.  
Just double-click the file to launch the app instantly.  
No installation, no terminal, and no Python required.

### 2. Run from Python source

If you’d rather run the app from code:

```bash
pip install -r requirements.txt
python app.py
