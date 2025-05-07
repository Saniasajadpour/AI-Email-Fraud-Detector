# test_prediction.py

import os
from core.model import load_model, predict_email
from core.preprocess import preprocess_email
from utils.file_handler import read_email_file

PASSED = 0
FAILED = 0

def run_test(email_text: str, expected_label: int = None, label_name: str = None):
    global PASSED, FAILED
    print("=" * 60)
    print(f"🔍 Testing: {label_name or 'Unnamed Case'}")

    try:
        model, vectorizer = load_model()
        clean_text = preprocess_email(email_text)
        label, proba = predict_email(clean_text, model, vectorizer)

        result = "✅ SAFE" if label == 0 else "⚠️ FRAUDULENT"
        print(f"→ Prediction: {result} ({proba:.2f}% confidence)")

        if expected_label is not None:
            if label == expected_label:
                print("✅ Expected result matched.")
                PASSED += 1
            else:
                print("❌ Expected:", "SAFE" if expected_label == 0 else "FRAUDULENT")
                FAILED += 1
        else:
            PASSED += 1  # no expected label means we just assume it passed
    except Exception as e:
        print("❌ ERROR:", e)
        FAILED += 1


def test_from_file(file_path, expected_label=None, label_name=None):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        email_text = read_email_file(f)

    run_test(email_text, expected_label, label_name)


if __name__ == "__main__":
    print("\n📦 Running Full Email Fraud Detection Test Suite...\n")

    # Sample realistic tests
    run_test(
        email_text="Your PayPal account has been restricted. Please verify your identity by clicking here: http://fakeurl.com/login",
        expected_label=1,
        label_name="Phishing PayPal Scam"
    )

    run_test(
        email_text="Welcome to our newsletter! We’re excited to share updates with you every week. No action is required.",
        expected_label=0,
        label_name="Safe Newsletter"
    )

    run_test(
        email_text="",
        expected_label=0,
        label_name="Empty Email Input"
    )

    run_test(
        email_text="Congratulations! You’ve been selected to win a FREE iPhone. Act now!",
        expected_label=1,
        label_name="Fake Prize Offer"
    )

    run_test(
        email_text="hello hello hello hello hello hello hello hello",
        expected_label=1,
        label_name="Spam Word Repetition"
    )

    run_test(
        email_text="💰💰🔥🔥👀👀!!!",
        expected_label=1,
        label_name="Emoji Spam"
    )

    test_from_file(
        file_path="data/sample_safe_email.txt",
        expected_label=0,
        label_name="Sample Legit Email (.txt)"
    )

    test_from_file(
        file_path="data/sample_fraud_email.eml",
        expected_label=1,
        label_name="Spoofed Email (.eml)"
    )

    # Summary
    print("\n🧪 Test Summary:")
    print(f"✅ Passed: {PASSED}")
    print(f"❌ Failed: {FAILED}")
    print(f"📊 Total: {PASSED + FAILED}")
