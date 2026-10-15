"""
Lab 06 - Solved Activity 2: Breast Cancer Classification using KNN
Course: AIC354 - Machine Learning Fundamentals
Topic: K-Nearest Neighbors on 2-Feature Breast Cancer Dataset
Student: Muhammad Afaq (FA23-BSE-012)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

def run_activity2():
    print("=" * 80)
    print("LAB 06 - SOLVED ACTIVITY 2: BREAST CANCER CLASSIFICATION USING KNN")
    print("=" * 80)

    # 1. Load Breast Cancer Dataset
    print("\n[Step 1] Loading Breast Cancer dataset from sklearn.datasets...")
    breast_cancer = load_breast_cancer()
    X_full = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)

    # Select two features as specified in manual: ['mean area', 'mean compactness']
    X = X_full[['mean area', 'mean compactness']].copy()
    y_cat = pd.Categorical.from_codes(breast_cancer.target, breast_cancer.target_names)
    y = pd.get_dummies(y_cat, drop_first=True) # 1 = benign, 0 = malignant
    target_series = y.iloc[:, 0].astype(int)

    print(f"Total samples: {X.shape[0]}")
    print(f"Selected 2 Features: {list(X.columns)}")
    print(f"Target distribution (0: malignant, 1: benign):\n{target_series.value_counts()}")

    # 2. Train-Test Split (25% Test, random_state=1 as in manual)
    print("\n[Step 2] Splitting data into train (75%) and test (25%) with random_state=1...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, target_series, test_size=0.25, random_state=1
    )
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples:  {X_test.shape[0]}")

    # 3. Fit KNeighborsClassifier(n_neighbors=5, metric='euclidean')
    print("\n[Step 3] Training KNeighborsClassifier(n_neighbors=5, metric='euclidean')...")
    knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
    knn.fit(X_train, y_train)
    print("Model fitted successfully.")

    # 4. Predictions & Evaluation
    print("\n[Step 4] Predicting on test set...")
    y_pred = knn.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    cr = classification_report(y_test, y_pred, target_names=['malignant', 'benign'])

    correct = cm[0, 0] + cm[1, 1]
    total = len(y_test)
    print(f"\nConfusion Matrix:")
    print(cm)
    print(f"\nGiven our confusion matrix, our model has an accuracy of {correct}/{total} = {acc * 100:.1f}%.")
    print("\nClassification Report:")
    print(cr)

    # 5. Visualizations: True vs Predicted Scatter Plots (Side by Side)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # Plot 1: True Labels
    scatter_df = X_test.copy()
    scatter_df['True Class'] = ['Benign (1)' if val == 1 else 'Malignant (0)' for val in y_test]
    sns.scatterplot(
        x='mean area',
        y='mean compactness',
        hue='True Class',
        palette={'Benign (1)': '#2B6CB0', 'Malignant (0)': '#E53E3E'},
        data=scatter_df,
        ax=axes[0],
        alpha=0.85,
        s=60,
        edgecolor='k'
    )
    axes[0].set_title("Ground Truth Test Samples\n(Benign vs Malignant)", fontsize=12, fontweight='bold', pad=10)
    axes[0].set_xlabel("Mean Area", fontsize=10, fontweight='bold')
    axes[0].set_ylabel("Mean Compactness", fontsize=10, fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Plot 2: Predicted Labels
    scatter_pred_df = X_test.copy()
    scatter_pred_df['Predicted Class'] = ['Benign (1)' if val == 1 else 'Malignant (0)' for val in y_pred]
    sns.scatterplot(
        x='mean area',
        y='mean compactness',
        hue='Predicted Class',
        palette={'Benign (1)': '#3182CE', 'Malignant (0)': '#DD6B20'},
        data=scatter_pred_df,
        ax=axes[1],
        alpha=0.85,
        s=60,
        edgecolor='k'
    )
    axes[1].set_title(f"KNN (k=5) Predicted Labels\nAccuracy: {acc * 100:.1f}% ({correct}/{total})", fontsize=12, fontweight='bold', pad=10)
    axes[1].set_xlabel("Mean Area", fontsize=10, fontweight='bold')
    axes[1].set_ylabel("Mean Compactness", fontsize=10, fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    scatter_path = "lab6_cancer_scatter_plots.png"
    plt.savefig(scatter_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Scatter comparison saved to '{scatter_path}'")

    # 6. Decision Boundary Visualization
    plt.figure(figsize=(8, 6))
    h = 2.0  # mesh step size
    x_min, x_max = X['mean area'].min() - 50, X['mean area'].max() + 50
    y_min, y_max = X['mean compactness'].min() - 0.05, X['mean compactness'].max() + 0.05
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, 5.0),
        np.arange(y_min, y_max, 0.005)
    )
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.25, cmap=plt.cm.coolwarm)
    scatter = plt.scatter(
        X_test['mean area'], X_test['mean compactness'],
        c=y_test, cmap=plt.cm.coolwarm, edgecolors='k', s=55, alpha=0.85
    )
    plt.title(f"Activity 2: KNN Decision Boundary (k=5, 2 Features)\nTest Accuracy: {acc * 100:.1f}%", fontsize=12, fontweight='bold')
    plt.xlabel("Mean Area", fontsize=11, fontweight='bold')
    plt.ylabel("Mean Compactness", fontsize=11, fontweight='bold')
    plt.colorbar(scatter, ticks=[0, 1], label='Class (0: Malignant, 1: Benign)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    boundary_path = "lab6_cancer_decision_boundary.png"
    plt.savefig(boundary_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Decision boundary saved to '{boundary_path}'")

    return {
        "accuracy": acc,
        "confusion_matrix": cm,
        "correct": correct,
        "total": total,
        "scatter_path": scatter_path,
        "boundary_path": boundary_path
    }

if __name__ == "__main__":
    run_activity2()
