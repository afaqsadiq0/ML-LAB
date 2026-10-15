"""
Lab 05 - Graded Lab Task 2: Loan Default Prediction using Naive Bayes
Course: AIC354 - Machine Learning Fundamentals
Topic: Exploratory Data Analysis (EDA) and Naive Bayes Classification on Real Loan Dataset
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score,
    roc_curve
)

def run_task2():
    print("=" * 80)
    print("LAB 05 - GRADED TASK 2: LOAN DATASET EXPLORATION & DEFAULT PREDICTION")
    print("=" * 80)

    # -------------------------------------------------------------
    # 1. LOAD DATASET
    # -------------------------------------------------------------
    print("\n[Step 1] Loading loan_data.csv...")
    df = pd.read_csv("loan_data.csv")
    print(f"Dataset successfully loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

    # -------------------------------------------------------------
    # 2. EXPLORATORY DATA ANALYSIS (EDA)
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("[Step 2] Performing Exploratory Data Analysis (EDA)...")
    
    print("\n--- A. Data Information & Types ---")
    print(df.info())

    print("\n--- B. Missing Values Check ---")
    missing = df.isnull().sum()
    print(f"Total missing values across all columns: {missing.sum()}")

    print("\n--- C. First 5 Rows ---")
    print(df.head(5))

    print("\n--- D. Summary Statistics of Key Numerical Features ---")
    key_cols = ['int.rate', 'installment', 'log.annual.inc', 'dti', 'fico', 'revol.bal', 'revol.util']
    print(df[key_cols].describe().round(3))

    print("\n--- E. Target Variable Distribution ('not.fully.paid') ---")
    target_counts = df['not.fully.paid'].value_counts()
    target_pct = df['not.fully.paid'].value_counts(normalize=True) * 100
    for val in [0, 1]:
        label = "Fully Paid (0)" if val == 0 else "Not Fully Paid / Default (1)"
        print(f"  {label}: {target_counts[val]} samples ({target_pct[val]:.2f}%)")

    print("\n--- F. Default Rate by Loan Purpose ---")
    purpose_summary = df.groupby('purpose')['not.fully.paid'].agg(
        Total='count',
        Defaults='sum',
        Default_Rate=lambda x: f"{x.mean()*100:.2f}%"
    ).sort_values(by='Total', ascending=False)
    print(purpose_summary)

    print("\n--- G. Mean Feature Comparison by Repayment Status ---")
    comparison = df.groupby('not.fully.paid')[['fico', 'int.rate', 'dti', 'inq.last.6mths']].mean()
    comparison.index = ['Fully Paid (0)', 'Not Fully Paid (1)']
    print(comparison.round(3))
    print("Insight: Borrowers who did not fully pay had lower average FICO scores,")
    print("higher interest rates, higher DTI ratios, and more credit inquiries in the last 6 months.")

    # -------------------------------------------------------------
    # GENERATE AND SAVE EDA PLOTS
    # -------------------------------------------------------------
    print("\nGenerating and saving EDA visualizations...")
    sns.set_theme(style="whitegrid")

    # Plot 1: Target Distribution & Purpose Count
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(x='not.fully.paid', data=df, ax=axes[0], palette=['#2ecc71', '#e74c3c'], hue='not.fully.paid', legend=False)
    axes[0].set_title("Target Distribution (0 = Paid, 1 = Unpaid)", fontweight='bold')
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(['Fully Paid (84%)', 'Not Fully Paid (16%)'])

    sns.countplot(y='purpose', hue='not.fully.paid', data=df, ax=axes[1], palette=['#3498db', '#e67e22'])
    axes[1].set_title("Loan Purpose by Payment Status", fontweight='bold')
    axes[1].legend(['Fully Paid', 'Not Fully Paid'])
    plt.tight_layout()
    plt.savefig('loan_eda_target_dist.png', dpi=150)
    plt.close()

    # Plot 2: FICO Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(data=df, x='fico', hue='not.fully.paid', bins=30, kde=True, palette=['#2ecc71', '#e74c3c'])
    plt.title("FICO Score Distribution by Loan Repayment Status", fontweight='bold')
    plt.xlabel("FICO Score")
    plt.ylabel("Count")
    plt.legend(labels=['Not Fully Paid (1)', 'Fully Paid (0)'])
    plt.tight_layout()
    plt.savefig('loan_eda_fico_distribution.png', dpi=150)
    plt.close()

    # Plot 3: Numerical Feature Correlation Heatmap
    plt.figure(figsize=(11, 8))
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={'shrink': 0.8})
    plt.title("Correlation Matrix of Numerical Features", fontweight='bold')
    plt.tight_layout()
    plt.savefig('loan_eda_correlation_matrix.png', dpi=150)
    plt.close()

    print("Saved plots:")
    print("  - loan_eda_target_dist.png")
    print("  - loan_eda_fico_distribution.png")
    print("  - loan_eda_correlation_matrix.png")

    # -------------------------------------------------------------
    # 3. PREPROCESSING & FEATURE ENCODING
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("[Step 3] Preprocessing and Categorical Encoding...")
    # Encode categorical 'purpose' column using one-hot encoding
    df_encoded = pd.get_dummies(df, columns=['purpose'], drop_first=True)
    print(f"Features after one-hot encoding: {df_encoded.shape[1] - 1}")

    X = df_encoded.drop('not.fully.paid', axis=1)
    y = df_encoded['not.fully.paid']

    # Train/Test Split (70% train, 30% test with stratification)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set:  {X_test.shape[0]} samples")

    # -------------------------------------------------------------
    # 4. MODEL TRAINING: GAUSSIAN NAIVE BAYES
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("[Step 4] Training Naive Bayes Classifier...")
    gnb_loan = GaussianNB()
    gnb_loan.fit(X_train, y_train)
    print("Gaussian Naive Bayes model trained successfully!")

    # -------------------------------------------------------------
    # 5. MODEL EVALUATION
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("[Step 5] Evaluating Model Performance on Test Data...")
    y_pred = gnb_loan.predict(X_test)
    y_pred_proba = gnb_loan.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"ROC-AUC:   {roc_auc:.4f}")

    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(
        cm,
        index=['Actual: Fully Paid (0)', 'Actual: Unpaid (1)'],
        columns=['Pred: Fully Paid (0)', 'Pred: Unpaid (1)']
    )
    print(cm_df)

    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, target_names=['Fully Paid (0)', 'Not Fully Paid (1)']))

    # Save Confusion Matrix & ROC Curve Plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Fully Paid', 'Not Fully Paid'])
    disp.plot(ax=axes[0], cmap='Blues', colorbar=False)
    axes[0].set_title(f"Confusion Matrix (Accuracy: {acc*100:.2f}%)", fontweight='bold')

    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    axes[1].plot(fpr, tpr, color='#e74c3c', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    axes[1].set_xlabel('False Positive Rate')
    axes[1].set_ylabel('True Positive Rate')
    axes[1].set_title('Receiver Operating Characteristic (ROC)', fontweight='bold')
    axes[1].legend(loc="lower right")

    plt.tight_layout()
    plt.savefig('loan_confusion_matrix.png', dpi=150)
    plt.close()
    print("Saved evaluation plot: loan_confusion_matrix.png")

    # -------------------------------------------------------------
    # 6. SAMPLE CUSTOMER PREDICTIONS
    # -------------------------------------------------------------
    print("\n" + "-" * 50)
    print("[Step 6] Predicting Future / Sample Customers for HR / Loan Officers...")
    
    # Pick diverse sample test candidates demonstrating both safe and risky loans
    test_indices = [12, 72, 85, 108, 128]
    sample_customers = X_test.iloc[test_indices]
    actual_status = y_test.iloc[test_indices].values

    pred_status = gnb_loan.predict(sample_customers)
    pred_probs = gnb_loan.predict_proba(sample_customers)

    results = []
    for i, idx in enumerate(test_indices):
        prob_default = pred_probs[i][1]
        results.append({
            'Customer Index': idx,
            'FICO Score': sample_customers.iloc[i]['fico'],
            'Interest Rate': f"{sample_customers.iloc[i]['int.rate']*100:.2f}%",
            'DTI': sample_customers.iloc[i]['dti'],
            'Actual Status': 'Not Fully Paid' if actual_status[i] == 1 else 'Fully Paid',
            'Predicted Status': 'RISK: Not Fully Paid' if pred_status[i] == 1 else 'SAFE: Fully Paid',
            'Default Risk (%)': f"{prob_default*100:.2f}%"
        })

    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))

    print("\n" + "=" * 80)
    print("LAB 05 - TASK 2 COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    run_task2()
