"""
Lab 05 - Graded Lab Task 1: Wine Classification using Naive Bayes
Course: AIC354 - Machine Learning Fundamentals
Topic: Gaussian Naive Bayes vs Multinomial Naive Bayes on Sklearn Wine Dataset
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

def run_task1():
    print("=" * 80)
    print("LAB 05 - GRADED TASK 1: WINE DATASET CLASSIFICATION")
    print("=" * 80)

    # 1. Load the Wine dataset
    print("\n[Step 1] Loading Wine dataset from sklearn.datasets...")
    wine = load_wine()
    X = wine.data
    y = wine.target
    feature_names = wine.feature_names
    target_names = wine.target_names

    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    df['class_name'] = [target_names[i] for i in y]

    print(f"Dataset Shape: {df.shape[0]} samples, {df.shape[1] - 2} features")
    print(f"Target Classes: {list(target_names)}")
    print("\nClass distribution:")
    print(df['class_name'].value_counts())

    print("\nSample features overview (first 3 rows):")
    print(df[feature_names[:5]].head(3))

    # 2. Train-Test Split
    print("\n" + "-" * 50)
    print("[Step 2] Splitting dataset into training (70%) and testing (30%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples:  {X_test.shape[0]}")

    # 3. Model Training: GaussianNB vs MultinomialNB
    print("\n" + "-" * 50)
    print("[Step 3] Training Naive Bayes Models...")

    # A. Gaussian Naive Bayes
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    y_pred_gnb = gnb.predict(X_test)
    acc_gnb = accuracy_score(y_test, y_pred_gnb)

    # B. Multinomial Naive Bayes
    mnb = MultinomialNB()
    mnb.fit(X_train, y_train)
    y_pred_mnb = mnb.predict(X_test)
    acc_mnb = accuracy_score(y_test, y_pred_mnb)

    # 4. Evaluation and Comparison
    print("\n" + "-" * 50)
    print("[Step 4] Evaluating and Comparing Model Performances...")
    print(f"GaussianNB Test Accuracy:    {acc_gnb * 100:.2f}%")
    print(f"MultinomialNB Test Accuracy: {acc_mnb * 100:.2f}%")

    # Cross-validation
    cv_gnb = cross_val_score(GaussianNB(), X, y, cv=5).mean()
    cv_mnb = cross_val_score(MultinomialNB(), X, y, cv=5).mean()
    print(f"GaussianNB 5-Fold CV Score:    {cv_gnb * 100:.2f}%")
    print(f"MultinomialNB 5-Fold CV Score: {cv_mnb * 100:.2f}%")

    print("\n--- GaussianNB Classification Report ---")
    print(classification_report(y_test, y_pred_gnb, target_names=target_names))

    print("--- MultinomialNB Classification Report ---")
    print(classification_report(y_test, y_pred_mnb, target_names=target_names))

    # Evaluation conclusion
    better_model = "Gaussian Naive Bayes" if acc_gnb >= acc_mnb else "Multinomial Naive Bayes"
    print(f"\n>>> EVALUATION CONCLUSION: {better_model} performs better.")
    print("Explanation: The Wine dataset consists of continuous, real-valued chemical features")
    print("(e.g., alcohol content, malic acid, flavonoids). GaussianNB assumes continuous features")
    print("follow a normal distribution, making it well-suited for this dataset. In contrast,")
    print("MultinomialNB is designed for discrete count features (such as word counts in text).")

    # 5. Predictions on Test Data
    print("\n" + "-" * 50)
    print("[Step 5] Performing Sample Predictions on Test Data (using best model: GaussianNB)...")
    sample_indices = [0, 5, 10, 15, 20]
    sample_X = X_test[sample_indices]
    sample_y = y_test[sample_indices]
    sample_pred = gnb.predict(sample_X)
    sample_proba = gnb.predict_proba(sample_X)

    pred_comparison = pd.DataFrame({
        'Sample Index': sample_indices,
        'Actual Class': [target_names[i] for i in sample_y],
        'Predicted Class': [target_names[i] for i in sample_pred],
        'Confidence': [f"{np.max(p)*100:.1f}%" for p in sample_proba],
        'Match': ['CORRECT' if a == p else 'INCORRECT' for a, p in zip(sample_y, sample_pred)]
    })
    print(pred_comparison.to_string(index=False))

    # 6. Save Confusion Matrix plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    cm_gnb = confusion_matrix(y_test, y_pred_gnb)
    cm_mnb = confusion_matrix(y_test, y_pred_mnb)

    disp1 = ConfusionMatrixDisplay(confusion_matrix=cm_gnb, display_labels=target_names)
    disp1.plot(ax=axes[0], cmap='Blues', colorbar=False)
    axes[0].set_title(f"GaussianNB (Accuracy: {acc_gnb*100:.1f}%)", fontsize=12, fontweight='bold')

    disp2 = ConfusionMatrixDisplay(confusion_matrix=cm_mnb, display_labels=target_names)
    disp2.plot(ax=axes[1], cmap='Oranges', colorbar=False)
    axes[1].set_title(f"MultinomialNB (Accuracy: {acc_mnb*100:.1f}%)", fontsize=12, fontweight='bold')

    plt.suptitle("Wine Classification - Confusion Matrix Comparison", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('wine_confusion_matrix.png', dpi=150)
    plt.close()
    print("\n[Output] Confusion matrix plot saved to 'wine_confusion_matrix.png'.")
    print("=" * 80)

if __name__ == "__main__":
    run_task1()
