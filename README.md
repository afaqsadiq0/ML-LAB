# Machine Learning Fundamentals (AIC354) - Laboratory Portfolio
## Department of Computer Science &bull; COMSATS University Islamabad

---

- **Student Name:** Muhammad Afaq
- **Registration Number:** FA23-BSE-012
- **Degree Program:** BS Software Engineering (BSE) - Section A
- **Course:** AIC354 - Machine Learning Fundamentals
- **Instructor:** Course Faculty (AIC354)
- **Institution:** COMSATS University Islamabad

---

## 📚 Completed Labs Overview

| Lab # | Topic / Algorithm | Solved Activities | Graded Tasks | Official Report PDF |
| :---: | :--- | :--- | :--- | :--- |
| **Lab 05** | **Naïve Bayes Classifier** | Iris (GaussianNB), Text (MultinomialNB) | Task 1: Sklearn Wine<br/>Task 2: LendingClub Loan Default EDA | [`FA23-BSE-012_Muhammad_Afaq_Lab05_Naive_Bayes.pdf`](file:///d:/github/ML-LAB/FA23-BSE-012_Muhammad_Afaq_Lab05_Naive_Bayes.pdf) |
| **Lab 06** | **K-Nearest Neighbors (KNN)** | Activity 1: Iris Classification<br/>Activity 2: Breast Cancer 2D Space | Task 1: Digits Recognition & K-Optimization<br/>Task 2: Sea Slug (Abalone) Non-Invasive Age Prediction | [`FA23-BSE-012_Muhammad_Afaq_Lab06_KNN.pdf`](file:///d:/github/ML-LAB/FA23-BSE-012_Muhammad_Afaq_Lab06_KNN.pdf) |

---

# 🔬 Lab 06: K-Nearest Neighbor (KNN) Algorithm

### 📁 Lab 06 File Structure:
- [`FA23-BSE-012_Muhammad_Afaq_Lab06_KNN.pdf`](file:///d:/github/ML-LAB/FA23-BSE-012_Muhammad_Afaq_Lab06_KNN.pdf) : **Publication-Grade Submission PDF Report** (Exact 5 pages, numbered header/footer, student metadata, theoretical foundation, activity walkthroughs, graded task results, high-res figures, and architectural conclusions).
- [`generate_lab6_pdf_report.py`](file:///d:/github/ML-LAB/generate_lab6_pdf_report.py) : Script used to compile the executive ReportLab PDF report.
- [`Lab_06_KNN.ipynb`](file:///d:/github/ML-LAB/Lab_06_KNN.ipynb) : Complete interactive Jupyter Notebook covering all 4 tasks (Activity 1, Activity 2, Graded Task 1, Graded Task 2).
- [`lab6_activity1_iris.py`](file:///d:/github/ML-LAB/lab6_activity1_iris.py) : Standalone Python script for **Solved Activity 1** (Iris dataset classification using KNN with $k=5$).
- [`lab6_activity2_cancer.py`](file:///d:/github/ML-LAB/lab6_activity2_cancer.py) : Standalone Python script for **Solved Activity 2** (Breast Cancer classification in 2D space with scatter plots and decision boundary).
- [`lab6_task1_digits.py`](file:///d:/github/ML-LAB/lab6_task1_digits.py) : Standalone Python script for **Graded Task 1** (Handwritten Digits classification with manual $K$ exploration, `GridSearchCV`, confusion matrix heatmap, and classification report).
- [`lab6_task2_abalone.py`](file:///d:/github/ML-LAB/lab6_task2_abalone.py) : Standalone Python script for **Graded Task 2** (Sea slug age prediction via KNN Regression on the UCI Abalone dataset, EDA, feature scaling, uniform vs distance weighting, and non-invasive sample predictions).
- [`abalone.data`](file:///d:/github/ML-LAB/abalone.data) : UCI Machine Learning Abalone dataset (4,177 instances).
- **Generated Figures & Visualizations:**
  - `lab6_iris_confusion_matrix.png`
  - `lab6_cancer_scatter_plots.png`
  - `lab6_cancer_decision_boundary.png`
  - `lab6_digits_k_optimization.png`
  - `lab6_digits_confusion_matrix.png`
  - `lab6_digits_classification_report.png`
  - `lab6_digits_samples.png`
  - `lab6_abalone_eda_correlation.png`
  - `lab6_abalone_k_vs_rmse.png`
  - `lab6_abalone_actual_vs_predicted.png`
  - `lab6_abalone_residuals.png`

---

## 📌 Lab 06 Activity Tasks

### 🌸 Activity 1: Iris Classification with KNN
- **Dataset:** Fisher's Iris (150 samples, 4 continuous features: sepal/petal lengths & widths, 3 classes: *Setosa, Versicolor, Virginica*).
- **Split:** 70% Train (105 samples), 30% Test (45 samples).
- **Configuration:** `KNeighborsClassifier(n_neighbors=5)`.
- **Results:**
  - **Accuracy:** **97.78%** (44 / 45 correct test predictions).
  - **Setosa:** 100% Precision, 100% Recall, 1.00 F1-score.
  - **Versicolor:** 94% Precision, 100% Recall, 0.97 F1-score.
  - **Virginica:** 100% Precision, 93% Recall, 0.97 F1-score.

### 🎗️ Activity 2: Breast Cancer 2D Classification
- **Dataset:** Breast Cancer Wisconsin (569 samples).
- **Features Selected:** Restricted 2-feature subset `['mean area', 'mean compactness']`.
- **Target:** Malignant (0) vs Benign (1) binary classification.
- **Split:** 75% Train (426 samples), 25% Test (143 samples) with `random_state=1`.
- **Configuration:** `KNeighborsClassifier(n_neighbors=5, metric='euclidean')`.
- **Results:**
  - **Accuracy:** **84.62%** (**121 / 143** correct predictions, exactly matching the manual benchmark).
  - Generated ground truth vs predicted class scatter plots and non-linear 2D decision boundary.

---

## 📌 Lab 06 Graded Tasks

### 🔢 Graded Task 1: Handwritten Digits Classification & K-Optimization
- **Dataset:** `sklearn.datasets.load_digits` (1,797 samples, 64 features representing $8 \times 8$ pixel grayscale intensities, classes 0 to 9).
- **Methodology:**
  1. Split dataset into 75% training (1,347 samples) and 25% testing (450 samples).
  2. Evaluated $k \in [1, 25]$ with 5-fold cross-validation.
  3. Conducted `GridSearchCV` over parameters: `n_neighbors`, `weights` (uniform vs distance), and `metric` (Euclidean vs Manhattan).
  4. Plotted annotated Confusion Matrix heatmap, per-digit classification report bar chart, and test digits visualization.
- **Results:**
  - **Optimal Hyperparameters:** `metric='euclidean'`, `n_neighbors=1`, `weights='uniform'` (also $k=3$ achieves identical top performance).
  - **5-Fold Cross-Validation Accuracy:** **99.11%**.
  - **Final Unseen Test Accuracy:** **98.44%** (**443 / 450** correct predictions).
  - **Perfect Recall & Precision (100%):** Digits 0, 2, 6, and 7 had zero misclassifications.

### 🐌 Graded Task 2: Sea Slug (Abalone) Non-Invasive Age Prediction
- **Problem Statement:** In sea slugs / abalones, age is conventionally determined by cutting the shell and counting the rings under a microscope ($Age = Rings + 1.5$ years). This destructive process is labor-intensive and damages specimen value. The task is to predict age non-invasively using purely non-destructive physical measurements.
- **Dataset:** UCI Machine Learning Repository Abalone dataset (4,177 instances, 9 attributes).
- **Methodology:**
  1. Exploratory Data Analysis (EDA) & correlation heatmap (Shell weight has the highest correlation with age, $r = 0.63$).
  2. Preprocessing: One-hot encoded categorical `Sex` column (`M`, `F`, `I`), added $Age = Rings + 1.5$.
  3. Standardized continuous physical features using `StandardScaler` (critical for distance-based KNN).
  4. Tuned `KNeighborsRegressor` across $k \in [1, 40]$ comparing `weights='uniform'` vs `weights='distance'`.
  5. Evaluated test predictions against a baseline mean predictor.
- **Results:**
  - **Optimal Configuration:** $k = 15$ with distance weighting (`weights='distance'`).
  - **Test RMSE:** **2.2546 years** (down from 3.2906 years baseline &rarr; **31.49% error reduction**).
  - **Test MAE:** **1.5616 years**.
  - **$R^2$ Score:** **0.5304** (explains 53.04% of age variance non-invasively).
  - Demonstrated non-invasive predictions on 5 sample abalones with error as low as 0.15 years.

---

## 🚀 How to Run Lab 06 Solutions

### Run Activity 1 (Iris Classification):
```bash
python lab6_activity1_iris.py
```

### Run Activity 2 (Breast Cancer Classification):
```bash
python lab6_activity2_cancer.py
```

### Run Graded Task 1 (Digits Classification & K-Optimization):
```bash
python lab6_task1_digits.py
```

### Run Graded Task 2 (Sea Slug / Abalone Age Prediction):
```bash
python lab6_task2_abalone.py
```

### Recompile Official Lab 06 PDF Report:
```bash
python generate_lab6_pdf_report.py
```

### Interactive Notebook:
Open [`Lab_06_KNN.ipynb`](file:///d:/github/ML-LAB/Lab_06_KNN.ipynb) in VS Code or Jupyter Lab.

---

# 🔬 Lab 05: Naïve Bayes Classifier (Summary)
- **Graded Task 1:** Wine Classification using `GaussianNB` (100% test accuracy) vs `MultinomialNB` (88.89%).
- **Graded Task 2:** LendingClub Loan Default Prediction (`loan_data.csv`) with full EDA and 82.60% accuracy.
- **Official Report PDF:** [`FA23-BSE-012_Muhammad_Afaq_Lab05_Naive_Bayes.pdf`](file:///d:/github/ML-LAB/FA23-BSE-012_Muhammad_Afaq_Lab05_Naive_Bayes.pdf)
