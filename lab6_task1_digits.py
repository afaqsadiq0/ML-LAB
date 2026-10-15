"""
Lab 06 - Graded Lab Task 1: Handwritten Digits Classification using KNN
Course: AIC354 - Machine Learning Fundamentals
Topic: K-Optimization (Manual & GridSearchCV), Confusion Matrix & Classification Report
Student: Muhammad Afaq (FA23-BSE-012)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

def run_task1():
    print("=" * 80)
    print("LAB 06 - GRADED TASK 1: HANDWRITTEN DIGITS CLASSIFICATION USING KNN")
    print("=" * 80)

    # 1. Load Digits Dataset
    print("\n[Step 1] Loading digits dataset from sklearn.datasets...")
    digits = load_digits()
    X = digits.data
    y = digits.target
    images = digits.images

    print(f"Dataset Shape: {X.shape[0]} samples, {X.shape[1]} features (8x8 pixel intensities)")
    print(f"Target Classes: {np.unique(y)} (Digits 0 through 9)")
    print(f"Image Resolution: 8 x 8 pixels per digit")

    # 2. Train-Test Split (75% Train, 25% Test, Stratified)
    print("\n[Step 2] Splitting data into 75% train and 25% test sets...")
    X_train, X_test, y_train, y_test, img_train, img_test = train_test_split(
        X, y, images, test_size=0.25, random_state=42, stratify=y
    )
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples:  {X_test.shape[0]}")

    # 3. K Exploration: Manually trying different values of K
    print("\n[Step 3] Evaluating different values of K (1 to 25) with 5-Fold Cross Validation...")
    k_range = list(range(1, 26))
    train_scores = []
    test_scores = []
    cv_mean_scores = []
    cv_std_scores = []

    for k in k_range:
        knn_k = KNeighborsClassifier(n_neighbors=k)
        knn_k.fit(X_train, y_train)
        
        train_acc = knn_k.score(X_train, y_train)
        test_acc = knn_k.score(X_test, y_test)
        cv_scores = cross_val_score(knn_k, X_train, y_train, cv=5)
        
        train_scores.append(train_acc)
        test_scores.append(test_acc)
        cv_mean_scores.append(cv_scores.mean())
        cv_std_scores.append(cv_scores.std())
        
        if k in [1, 3, 5, 7, 9, 11, 15, 20, 25]:
            print(f"  k={k:2d} -> Train Acc: {train_acc*100:.2f}%, Test Acc: {test_acc*100:.2f}%, 5-Fold CV: {cv_scores.mean()*100:.2f}% (±{cv_scores.std()*100:.2f}%)")

    best_manual_k = k_range[int(np.argmax(cv_mean_scores))]
    best_manual_cv = max(cv_mean_scores)
    print(f"\nBest manual K based on 5-fold CV: k={best_manual_k} with {best_manual_cv*100:.2f}% validation accuracy")

    # 4. Hyperparameter Tuning using GridSearchCV
    print("\n[Step 4] Running GridSearchCV over K values, distance metrics, and weight functions...")
    param_grid = {
        'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan']
    }
    grid_search = GridSearchCV(
        KNeighborsClassifier(),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    print("\nGridSearchCV Results:")
    print(f"  Optimal Hyperparameters: {best_params}")
    print(f"  Best 5-Fold CV Accuracy: {best_cv_score * 100:.2f}%")

    # 5. Evaluate Best Model on Unseen Test Data
    print("\n[Step 5] Evaluating optimal model on unseen test set...")
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr_dict = classification_report(y_test, y_pred, output_dict=True)
    cr_text = classification_report(y_test, y_pred, digits=4)

    print(f"Final Test Accuracy: {test_accuracy * 100:.2f}% ({np.sum(y_pred == y_test)}/{len(y_test)} correct)")
    print("\nConfusion Matrix:")
    print(cm)
    print("\nClassification Report:")
    print(cr_text)

    # -------------------------------------------------------------
    # 6. PLOTS
    # -------------------------------------------------------------
    # Plot 1: K Optimization Curve
    plt.figure(figsize=(9, 5))
    plt.plot(k_range, [s * 100 for s in train_scores], 'o--', color='#E53E3E', label='Training Accuracy', alpha=0.7)
    plt.plot(k_range, [s * 100 for s in test_scores], 's-', color='#3182CE', label='Test Accuracy', linewidth=2)
    plt.plot(k_range, [s * 100 for s in cv_mean_scores], '^-', color='#2F855A', label='5-Fold CV Accuracy', linewidth=2)
    plt.axvline(best_params['n_neighbors'], color='#D69E2E', linestyle=':', linewidth=2, label=f"Optimal k={best_params['n_neighbors']}")
    plt.title("Task 1: KNN Digits Classification - Accuracy vs K Neighbors", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Number of Neighbors (k)", fontsize=11, fontweight='bold')
    plt.ylabel("Accuracy (%)", fontsize=11, fontweight='bold')
    plt.xticks(k_range)
    plt.ylim(94, 100.5)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    k_opt_path = "lab6_digits_k_optimization.png"
    plt.savefig(k_opt_path, dpi=300)
    plt.close()
    print(f"\n[Visualization Saved] K-optimization plot saved to '{k_opt_path}'")

    # Plot 2: Confusion Matrix Heatmap
    plt.figure(figsize=(8, 6.5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=range(10), yticklabels=range(10),
        cbar=True, annot_kws={"size": 11, "weight": "bold"}
    )
    plt.title(f"Task 1: Digits Confusion Matrix (Optimal KNN: k={best_params['n_neighbors']}, {best_params['weights']}, {best_params['metric']})\nTest Accuracy: {test_accuracy * 100:.2f}%", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Predicted Digit", fontsize=11, fontweight='bold')
    plt.ylabel("Actual Digit", fontsize=11, fontweight='bold')
    plt.tight_layout()
    cm_path = "lab6_digits_confusion_matrix.png"
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Confusion matrix heatmap saved to '{cm_path}'")

    # Plot 3: Classification Report Per-Digit Metrics
    digits_labels = [str(i) for i in range(10)]
    precision_vals = [cr_dict[str(i)]['precision'] * 100 for i in range(10)]
    recall_vals = [cr_dict[str(i)]['recall'] * 100 for i in range(10)]
    f1_vals = [cr_dict[str(i)]['f1-score'] * 100 for i in range(10)]

    x_indices = np.arange(len(digits_labels))
    bar_w = 0.26

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x_indices - bar_w, precision_vals, bar_w, label='Precision (%)', color='#2B6CB0')
    ax.bar(x_indices, recall_vals, bar_w, label='Recall (%)', color='#38A169')
    ax.bar(x_indices + bar_w, f1_vals, bar_w, label='F1-Score (%)', color='#DD6B20')

    ax.set_title("Task 1: Per-Digit Classification Metrics (Precision, Recall, F1-Score)", fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel("Digit Class (0 - 9)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Score (%)", fontsize=11, fontweight='bold')
    ax.set_xticks(x_indices)
    ax.set_xticklabels(digits_labels, fontweight='bold')
    ax.set_ylim(92, 102)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='lower right')
    plt.tight_layout()
    cr_path = "lab6_digits_classification_report.png"
    plt.savefig(cr_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Classification report plot saved to '{cr_path}'")

    # Plot 4: Sample Test Digits with Predictions
    fig, axes = plt.subplots(2, 5, figsize=(10, 4.5))
    for idx, ax in enumerate(axes.flat):
        img = img_test[idx]
        actual = y_test[idx]
        pred = y_pred[idx]
        ax.imshow(img, cmap=plt.cm.gray_r, interpolation='nearest')
        color = 'green' if actual == pred else 'red'
        ax.set_title(f"True: {actual} | Pred: {pred}", color=color, fontsize=10, fontweight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.suptitle("Task 1: Sample Test Handwritten Digits & KNN Predictions", fontsize=12, fontweight='bold')
    plt.tight_layout()
    samples_path = "lab6_digits_samples.png"
    plt.savefig(samples_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Sample digits predictions saved to '{samples_path}'")

    return {
        "best_params": best_params,
        "best_cv_score": best_cv_score,
        "test_accuracy": test_accuracy,
        "confusion_matrix": cm,
        "classification_report": cr_text,
        "k_opt_path": k_opt_path,
        "cm_path": cm_path,
        "cr_path": cr_path,
        "samples_path": samples_path
    }

if __name__ == "__main__":
    run_task1()
