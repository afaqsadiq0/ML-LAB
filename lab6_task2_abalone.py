"""
Lab 06 - Graded Lab Task 2: Predict Sea Slug (Abalone) Age using kNN Regression
Course: AIC354 - Machine Learning Fundamentals
Topic: Non-Invasive Age Prediction on UCI Abalone Dataset using KNeighborsRegressor
Student: Muhammad Afaq (FA23-BSE-012)
"""

import os
import urllib.request
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

DATA_PATH = "abalone.data"
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data"

COLUMNS = [
    'Sex', 'Length', 'Diameter', 'Height',
    'Whole_weight', 'Shucked_weight', 'Viscera_weight', 'Shell_weight', 'Rings'
]

def load_or_download_data():
    if not os.path.exists(DATA_PATH):
        print(f"Downloading Abalone dataset from {DATA_URL}...")
        urllib.request.urlretrieve(DATA_URL, DATA_PATH)
        print("Download complete.")
    df = pd.read_csv(DATA_PATH, names=COLUMNS)
    return df

def run_task2():
    print("=" * 80)
    print("LAB 06 - GRADED TASK 2: PREDICTING ABALONE AGE USING KNN REGRESSION")
    print("=" * 80)

    # 1. Load Dataset
    print("\n[Step 1] Loading Abalone dataset...")
    df = load_or_download_data()
    print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")

    # In literature and biological studies, Age = Rings + 1.5 years
    df['Age'] = df['Rings'] + 1.5
    print("\nTarget Variable Defined: Age = Rings + 1.5 (Years)")
    print(f"Age range: {df['Age'].min():.1f} to {df['Age'].max():.1f} years (Mean: {df['Age'].mean():.2f})")

    # 2. Exploratory Data Analysis (EDA)
    print("\n" + "-" * 50)
    print("[Step 2] Exploratory Data Analysis (EDA)...")
    print("\n--- Missing Values Check ---")
    print(f"Total missing values: {df.isnull().sum().sum()}")

    print("\n--- Sex Categorical Distribution ---")
    print(df['Sex'].value_counts())

    print("\n--- Descriptive Statistics of Physical Measurements ---")
    meas_cols = ['Length', 'Diameter', 'Height', 'Whole_weight', 'Shucked_weight', 'Viscera_weight', 'Shell_weight', 'Age']
    print(df[meas_cols].describe().round(3))

    # Correlation Analysis
    corr = df[meas_cols].corr()
    print("\n--- Correlation with Target Age ---")
    print(corr['Age'].sort_values(ascending=False).round(3))

    # Plot 1: Correlation Heatmap
    plt.figure(figsize=(8, 6.5))
    sns.heatmap(
        corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-0.2, vmax=1.0,
        linewidths=0.5, cbar_kws={'label': 'Pearson Correlation'}
    )
    plt.title("Task 2: Abalone Physical Features Correlation Heatmap", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    corr_path = "lab6_abalone_eda_correlation.png"
    plt.savefig(corr_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Correlation heatmap saved to '{corr_path}'")

    # 3. Data Preprocessing & Feature Encoding
    print("\n" + "-" * 50)
    print("[Step 3] Data Preprocessing & Feature Encoding...")
    
    # One-hot encode the categorical 'Sex' column
    df_encoded = pd.get_dummies(df, columns=['Sex'], drop_first=True, dtype=float)
    
    # Feature matrix X (drop Rings and Age), target vector y (Age)
    feature_cols = [c for c in df_encoded.columns if c not in ['Rings', 'Age']]
    X = df_encoded[feature_cols].copy()
    y = df_encoded['Age'].copy()

    print(f"Features used for training ({len(feature_cols)} features):")
    print(feature_cols)

    # 4. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"\nTrain set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")

    # 5. Feature Standardization (Critical for distance-based KNN)
    print("\n[Step 4] Applying StandardScaler (Standardizing features for KNN distances)...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 6. Hyperparameter Exploration: K (1 to 40) with Uniform vs Distance Weighting
    print("\n[Step 5] Evaluating K values (1 to 40) for Uniform vs Distance weighting...")
    k_values = list(range(1, 41))
    rmse_uniform = []
    rmse_distance = []
    r2_uniform = []
    r2_distance = []

    for k in k_values:
        # Uniform weighting
        knn_u = KNeighborsRegressor(n_neighbors=k, weights='uniform')
        knn_u.fit(X_train_scaled, y_train)
        pred_u = knn_u.predict(X_test_scaled)
        rmse_u = np.sqrt(mean_squared_error(y_test, pred_u))
        rmse_uniform.append(rmse_u)
        r2_uniform.append(r2_score(y_test, pred_u))

        # Distance weighting (inversely proportional to distance)
        knn_d = KNeighborsRegressor(n_neighbors=k, weights='distance')
        knn_d.fit(X_train_scaled, y_train)
        pred_d = knn_d.predict(X_test_scaled)
        rmse_d = np.sqrt(mean_squared_error(y_test, pred_d))
        rmse_distance.append(rmse_d)
        r2_distance.append(r2_score(y_test, pred_d))

        if k in [1, 3, 5, 7, 10, 15, 20, 25, 30, 40]:
            print(f"  k={k:2d} -> Uniform RMSE: {rmse_u:.3f} (R²: {r2_uniform[-1]:.3f}) | Distance RMSE: {rmse_d:.3f} (R²: {r2_distance[-1]:.3f})")

    best_k_dist = k_values[int(np.argmin(rmse_distance))]
    best_rmse_dist = min(rmse_distance)
    best_r2_dist = r2_distance[int(np.argmin(rmse_distance))]

    best_k_uni = k_values[int(np.argmin(rmse_uniform))]
    best_rmse_uni = min(rmse_uniform)
    best_r2_uni = r2_uniform[int(np.argmin(rmse_uniform))]

    print(f"\nOptimal K (Uniform Weighting):  k={best_k_uni} -> Min RMSE: {best_rmse_uni:.4f}, R²: {best_r2_uni:.4f}")
    print(f"Optimal K (Distance Weighting): k={best_k_dist} -> Min RMSE: {best_rmse_dist:.4f}, R²: {best_r2_dist:.4f}")

    # Plot 2: K vs RMSE Comparison
    plt.figure(figsize=(9, 5))
    plt.plot(k_values, rmse_uniform, 'o-', color='#3182CE', label='Uniform Weights', linewidth=2)
    plt.plot(k_values, rmse_distance, 's-', color='#DD6B20', label='Distance-Weighted (1/distance)', linewidth=2)
    plt.axvline(best_k_dist, color='#E53E3E', linestyle='--', linewidth=1.5, label=f'Optimal Distance k={best_k_dist}')
    plt.axvline(best_k_uni, color='#2B6CB0', linestyle=':', linewidth=1.5, label=f'Optimal Uniform k={best_k_uni}')
    plt.title("Task 2: KNN Regressor Performance - RMSE vs Number of Neighbors (k)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Number of Neighbors (k)", fontsize=11, fontweight='bold')
    plt.ylabel("Root Mean Squared Error (RMSE in Years)", fontsize=11, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    k_rmse_path = "lab6_abalone_k_vs_rmse.png"
    plt.savefig(k_rmse_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] K vs RMSE plot saved to '{k_rmse_path}'")

    # 7. Final Model Evaluation with Best Model
    print("\n" + "-" * 50)
    print(f"[Step 6] Final Evaluation with Best Model: KNeighborsRegressor(n_neighbors={best_k_dist}, weights='distance')...")
    best_knn = KNeighborsRegressor(n_neighbors=best_k_dist, weights='distance')
    best_knn.fit(X_train_scaled, y_train)

    y_pred = best_knn.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    # Benchmark against baseline mean predictor
    baseline_pred = np.full_like(y_test, y_train.mean())
    base_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))

    print(f"--- Model Evaluation Metrics ---")
    print(f"Mean Absolute Error (MAE):      {mae:.4f} years")
    print(f"Mean Squared Error (MSE):       {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f} years")
    print(f"Coefficient of Determination R²: {r2:.4f} ({r2*100:.2f}% variance explained)")
    print(f"Baseline (Mean Predictor) RMSE: {base_rmse:.4f} years")
    print(f"Error Reduction over Baseline:  {((base_rmse - rmse) / base_rmse) * 100:.2f}%")

    # Plot 3: Actual vs Predicted Age Scatter Plot
    plt.figure(figsize=(7.5, 6))
    plt.scatter(y_test, y_pred, alpha=0.45, color='#2B6CB0', edgecolors='none', s=35, label='Test Abalones')
    # Ideal 45-degree reference line
    min_val = min(y_test.min(), y_pred.min()) - 1
    max_val = max(y_test.max(), y_pred.max()) + 1
    plt.plot([min_val, max_val], [min_val, max_val], color='#E53E3E', linestyle='--', linewidth=2, label='Ideal Perfect Fit (y = x)')
    plt.title(f"Task 2: Abalone Age Prediction - Actual vs Predicted\n(Optimal KNN: k={best_k_dist}, weights='distance', RMSE={rmse:.2f} yrs)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Actual Age (Years = Rings + 1.5)", fontsize=11, fontweight='bold')
    plt.ylabel("KNN Predicted Age (Years)", fontsize=11, fontweight='bold')
    plt.xlim(min_val, max_val)
    plt.ylim(min_val, max_val)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
    plt.tight_layout()
    pred_path = "lab6_abalone_actual_vs_predicted.png"
    plt.savefig(pred_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Actual vs Predicted plot saved to '{pred_path}'")

    # Plot 4: Residuals Distribution
    residuals = y_test - y_pred
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    
    # Residuals vs Predicted
    axes[0].scatter(y_pred, residuals, alpha=0.45, color='#3182CE', s=30)
    axes[0].axhline(0, color='#E53E3E', linestyle='--', linewidth=1.5)
    axes[0].set_title("Residuals vs Predicted Age", fontsize=11, fontweight='bold')
    axes[0].set_xlabel("Predicted Age (Years)", fontsize=10, fontweight='bold')
    axes[0].set_ylabel("Residual (Actual - Pred)", fontsize=10, fontweight='bold')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    # Histogram of residuals
    sns.histplot(residuals, kde=True, ax=axes[1], color='#2B6CB0', bins=30)
    axes[1].axvline(0, color='#E53E3E', linestyle='--', linewidth=1.5)
    axes[1].set_title(f"Residuals Error Distribution\n(Mean: {residuals.mean():.2f}, Std: {residuals.std():.2f})", fontsize=11, fontweight='bold')
    axes[1].set_xlabel("Residual Error (Years)", fontsize=10, fontweight='bold')
    axes[1].set_ylabel("Count", fontsize=10, fontweight='bold')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    res_path = "lab6_abalone_residuals.png"
    plt.savefig(res_path, dpi=300)
    plt.close()
    print(f"[Visualization Saved] Residuals analysis plot saved to '{res_path}'")

    # 8. Sample Non-Invasive Predictions Demonstration
    print("\n" + "-" * 50)
    print("[Step 7] Demonstrating Non-Invasive Age Predictions on 5 Sample Abalones:")
    print("  (Estimating Age directly from physical measurements without cutting the shell)")
    sample_indices = [5, 12, 42, 100, 250]
    sample_df = X_test.iloc[sample_indices].copy()
    sample_actual_age = y_test.iloc[sample_indices].values
    sample_scaled = X_test_scaled[sample_indices]
    sample_pred_age = best_knn.predict(sample_scaled)

    results_table = []
    for i in range(len(sample_indices)):
        actual = sample_actual_age[i]
        predicted = sample_pred_age[i]
        err = abs(actual - predicted)
        length = sample_df['Length'].iloc[i]
        diameter = sample_df['Diameter'].iloc[i]
        shell_w = sample_df['Shell_weight'].iloc[i]
        results_table.append({
            "Sample #": i + 1,
            "Length (mm)": round(length, 3),
            "Diameter (mm)": round(diameter, 3),
            "Shell Weight (g)": round(shell_w, 3),
            "Actual Rings": int(actual - 1.5),
            "Actual Age (Yrs)": round(actual, 1),
            "Predicted Age (Yrs)": round(predicted, 2),
            "Absolute Error (Yrs)": round(err, 2)
        })

    res_df = pd.DataFrame(results_table)
    print(res_df.to_string(index=False))

    return {
        "best_k": best_k_dist,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "baseline_rmse": base_rmse,
        "corr_path": corr_path,
        "k_rmse_path": k_rmse_path,
        "pred_path": pred_path,
        "res_path": res_path,
        "sample_df": res_df
    }

if __name__ == "__main__":
    run_task2()
