"""
Lab 06 - Solved Activity 1: Iris Dataset Classification using KNN
Course: AIC354 - Machine Learning Fundamentals
Topic: K-Nearest Neighbors Classification on Fisher's Iris Dataset
Student: Muhammad Afaq (FA23-BSE-012)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def run_activity1():
    print("=" * 80)
    print("LAB 06 - SOLVED ACTIVITY 1: IRIS DATASET CLASSIFICATION USING KNN")
    print("=" * 80)

    # 1. Load Iris Dataset
    print("\n[Step 1] Loading Iris dataset from sklearn.datasets...")
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names

    print(f"Features: {feature_names}")
    print(f"Target Classes: {list(target_names)}")
    print(f"Dataset Shape: {X.shape[0]} samples, {X.shape[1]} features")

    # 2. Train-Test Split (70% Train, 30% Test as in manual)
    print("\n[Step 2] Splitting dataset into training (70%) and testing (30%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples:  {X_test.shape[0]}")

    # 3. Model Training: KNeighborsClassifier with K=5
    print("\n[Step 3] Initializing and training KNeighborsClassifier(n_neighbors=5)...")
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)
    print("Model training complete.")

    # 4. Predictions on Test Data
    print("\n[Step 4] Making predictions on test set...")
    y_pred = classifier.predict(X_test)

    # 5. Evaluation
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred, target_names=target_names)

    print(f"\nModel Accuracy: {acc * 100:.2f}%")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr)

    # 6. Plot Confusion Matrix
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=target_names, yticklabels=target_names,
        cbar=True, annot_kws={"size": 13, "weight": "bold"}
    )
    plt.title(f"Activity 1: Iris KNN Confusion Matrix (k=5)\nAccuracy: {acc * 100:.1f}%", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Predicted Species", fontsize=11, fontweight='bold')
    plt.ylabel("Actual Species", fontsize=11, fontweight='bold')
    plt.tight_layout()
    plot_path = "lab6_iris_confusion_matrix.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Confusion matrix saved to '{plot_path}'")

    return {
        "accuracy": acc,
        "confusion_matrix": cm,
        "classification_report": cr,
        "plot_path": plot_path
    }

if __name__ == "__main__":
    run_activity1()
