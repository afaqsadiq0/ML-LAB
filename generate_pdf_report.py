"""
Script to generate an executive, publication-grade Lab 05 Report PDF for:
Student Name: Muhammad Afaq
Registration Number: FA23-BSE-012
Course: AIC354 - Machine Learning Fundamentals
Topic: Lab 05 - Naïve Bayes Classifier
Institution: COMSATS University Islamabad
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas
import pymupdf

PDF_FILENAME = "FA23-BSE-012_Muhammad_Afaq_Lab05_Naive_Bayes.pdf"

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total page count and draw
    a sharp running header and footer on every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        page_w, page_h = A4
        margin = 36  # 0.5 in

        # Running Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D"))  # Deep Navy
        self.drawString(margin, page_h - 26, "COMSATS UNIVERSITY ISLAMABAD  |  AIC354 Machine Learning Fundamentals")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        self.drawRightString(page_w - margin, page_h - 26, "Lab 05: Naïve Bayes Classifier")

        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(margin, page_h - 30, page_w - margin, page_h - 30)

        # Running Footer
        self.line(margin, 30, page_w - margin, 30)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2B6CB0"))
        self.drawString(margin, 18, "Muhammad Afaq (FA23-BSE-012)")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawString(margin + 165, 18, "BS Software Engineering  |  Section A")
        self.drawRightString(page_w - margin, 18, f"Page {self._pageNumber} of {page_count}")

        self.restoreState()


def create_lab_report():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=38
    )

    printable_w = A4[0] - 72  # 523.27 pt

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F2942'),
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2B6CB0'),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1A202C')
    )

    pre_code_style = ParagraphStyle(
        'PreCodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#1A202C')
    )

    pre_terminal_style = ParagraphStyle(
        'PreTerminalStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#00E676')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor('#2D3748')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceBefore=2,
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE BANNER, STUDENT INFO & THEORETICAL FOUNDATION
    # =========================================================================
    banner_data = [
        [
            Paragraph("<b>COMSATS UNIVERSITY ISLAMABAD</b><br/><font size=7.5 color='#CBD5E0'>Department of Computer Science &bull; Autumn 2026</font>", ParagraphStyle('BanH', parent=title_style, fontSize=12, leading=15, textColor=colors.white, alignment=0)),
            Paragraph("<font size=7.5 color='#A0AEC0'>COURSE CODE:</font><br/><b>AIC354</b><br/><font size=7 color='#E2E8F0'>Machine Learning Fundamentals</font>", ParagraphStyle('BanR', parent=title_style, fontSize=9.5, leading=12, textColor=colors.white, alignment=2))
        ]
    ]
    banner_table = Table(banner_data, colWidths=[330, printable_w - 330])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F2942')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("LAB REPORT 05: NAÏVE BAYES CLASSIFIER", title_style))
    story.append(Paragraph("Task 1: Sklearn Wine Classification &bull; Task 2: LendingClub Loan Default Prediction & EDA", subtitle_style))
    story.append(Spacer(1, 4))

    meta_table_data = [
        [
            Paragraph("<b>Student Full Name:</b>", table_cell_bold),
            Paragraph("<font color='#0F2942'><b>Muhammad Afaq</b></font>", table_cell_style),
            Paragraph("<b>Registration Number:</b>", table_cell_bold),
            Paragraph("<font color='#B91C1C'><b>FA23-BSE-012</b></font>", table_cell_style),
        ],
        [
            Paragraph("<b>Degree Program:</b>", table_cell_bold),
            Paragraph("BS Software Engineering (BSE)", table_cell_style),
            Paragraph("<b>Class Section:</b>", table_cell_bold),
            Paragraph("Section A", table_cell_style),
        ],
        [
            Paragraph("<b>Lab Instructor:</b>", table_cell_bold),
            Paragraph("Course Faculty (AIC354)", table_cell_style),
            Paragraph("<b>Submission Date:</b>", table_cell_bold),
            Paragraph("October 08, 2026", table_cell_style),
        ],
        [
            Paragraph("<b>GitHub Repository:</b>", table_cell_bold),
            Paragraph("<font color='#2B6CB0'><u>github.com/afaqsadiq0/ML-LAB</u></font>", table_cell_style),
            Paragraph("<b>Lab Status:</b>", table_cell_bold),
            Paragraph("<font color='#16A34A'><b>100% Solved & Verified with Outputs</b></font>", table_cell_style),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[105, 155, 115, printable_w - 375])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Theoretical Foundation: The Naïve Bayes Classifier", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceBefore=1, spaceAfter=4))

    theo_text = (
        "<b>Naïve Bayes</b> is a prominent family of supervised probabilistic classifiers rooted in <b>Bayes' Theorem</b>, "
        "incorporating the simplifying ('naïve') assumption that features are conditionally independent given the class label. "
        "Despite this strong assumption, Naïve Bayes models are computationally efficient, require minimal training data, and deliver "
        "exceptional classification accuracy across real-world continuous and discrete data problems."
    )
    story.append(Paragraph(theo_text, body_style))

    formula_html = (
        "<b>Mathematical Formulation of Bayes' Theorem:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(C<sub>k</sub> | X) = [ P(X | C<sub>k</sub>) &times; P(C<sub>k</sub>) ] / P(X)</b><br/>"
        "Under the Conditional Independence Assumption:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(X | C<sub>k</sub>) = &prod;<sub>i=1..n</sub> P(x<sub>i</sub> | C<sub>k</sub>)</b><br/>"
        "&bull; <b>P(C<sub>k</sub> | X)</b>: Posterior probability that instance with feature vector X belongs to class C<sub>k</sub>.<br/>"
        "&bull; <b>P(X | C<sub>k</sub>)</b>: Likelihood of feature vector X given class C<sub>k</sub>.<br/>"
        "&bull; <b>P(C<sub>k</sub>)</b>: Prior probability of class C<sub>k</sub> (empirical class frequency).<br/>"
        "&bull; <b>P(X)</b>: Marginal probability / normalizer ensuring posterior probabilities sum to 1."
    )
    formula_table = Table([[Paragraph(formula_html, callout_style)]], colWidths=[printable_w])
    formula_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EDF2F7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(formula_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Comparison of Naïve Bayes Algorithm Variants:</b>", h2_style))
    nb_comp_data = [
        [
            Paragraph("Classifier Variant", table_header_style),
            Paragraph("Distribution Model", table_header_style),
            Paragraph("Feature Type", table_header_style),
            Paragraph("Application Domain", table_header_style)
        ],
        [
            Paragraph("<b>GaussianNB</b>", table_cell_bold),
            Paragraph("Gaussian (Normal) Bell Curve:<br/>P(x<sub>i</sub>|C) &sim; N(&mu;<sub>c</sub>, &sigma;<sub>c</sub><sup>2</sup>)", table_cell_style),
            Paragraph("Continuous real-valued floats (e.g. alcohol, chemical properties, FICO, interest)", table_cell_style),
            Paragraph("Lab Task 1 (Wine Dataset), Lab Task 2 (Loan Risk Features)", table_cell_style)
        ],
        [
            Paragraph("<b>MultinomialNB</b>", table_cell_bold),
            Paragraph("Multinomial Distribution:<br/>P(x|C) &prop; &prod; &theta;<sub>c,i</sub><sup>x<sub>i</sub></sup>", table_cell_style),
            Paragraph("Discrete count / frequency integers (&ge; 0)", table_cell_style),
            Paragraph("Natural Language Processing, text mining, word frequencies, spam filtering", table_cell_style)
        ],
        [
            Paragraph("<b>BernoulliNB</b>", table_cell_bold),
            Paragraph("Multivariate Bernoulli Distribution", table_cell_style),
            Paragraph("Binary indicators (0 or 1)", table_cell_style),
            Paragraph("Word presence/absence text classification, binary indicators", table_cell_style)
        ]
    ]
    nb_table = Table(nb_comp_data, colWidths=[100, 140, 140, printable_w - 380])
    nb_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(nb_table)

    # =========================================================================
    # PAGE 2: LAB TASK 1 IMPLEMENTATION, OUTPUT & EVALUATION
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("2. Graded Lab Task 1: Wine Classification (Sklearn Dataset)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceBefore=1, spaceAfter=4))

    t1_prob = (
        "<b>Task Statement:</b> Use the wine dataset from <code>sklearn.datasets</code> to classify wines into 3 categories. "
        "Load the dataset and split it into test and train sets. After that, train the model using Gaussian and Multinomial "
        "classifiers and evaluate which performs better. Use the trained model to perform predictions on test data."
    )
    t1_prob_table = Table([[Paragraph(t1_prob, callout_style)]], colWidths=[printable_w])
    t1_prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93C5FD')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t1_prob_table)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>2.1 Complete Python Implementation (<code>lab5_task1_wine.py</code>):</b>", h2_style))
    t1_code_clean = (
"""# Lab 05 Graded Task 1 - Wine Dataset Classification
# Student: Muhammad Afaq | Reg No: FA23-BSE-012 | Course: AIC354 ML Fundamentals
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load Wine Dataset (178 samples, 13 continuous chemical features, 3 classes)
wine = load_wine(); X, y = wine.data, wine.target

# Step 2: Stratified Train/Test Split (70% train = 124, 30% test = 54)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Step 3: Train GaussianNB vs MultinomialNB Models
gnb = GaussianNB().fit(X_train, y_train); y_pred_gnb = gnb.predict(X_test)
mnb = MultinomialNB().fit(X_train, y_train); y_pred_mnb = mnb.predict(X_test)

# Step 4: Quantitative Evaluation
acc_gnb, acc_mnb = accuracy_score(y_test, y_pred_gnb), accuracy_score(y_test, y_pred_mnb)
cv_gnb = cross_val_score(GaussianNB(), X, y, cv=5).mean()
cv_mnb = cross_val_score(MultinomialNB(), X, y, cv=5).mean()"""
    ).strip()

    code_t1_box = Table([[Preformatted(t1_code_clean, pre_code_style)]], colWidths=[printable_w])
    code_t1_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(code_t1_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>2.2 Real Execution Output & Console Logs:</b>", h2_style))
    term_t1_clean = (
"""================================================================================
LAB 05 - GRADED TASK 1: WINE DATASET CLASSIFICATION
================================================================================
[Step 1] Loading Wine dataset from sklearn.datasets...
Dataset Shape: 178 samples, 13 features | Target Classes: ['class_0', 'class_1', 'class_2']
Class distribution: class_1: 71 | class_0: 59 | class_2: 48
[Step 2] Splitting dataset: Training = 124 samples (70%), Testing = 54 samples (30%)
--------------------------------------------------------------------------------
GaussianNB Test Accuracy:    100.00%  |  5-Fold CV Score: 96.63%
MultinomialNB Test Accuracy:  88.89%  |  5-Fold CV Score: 84.40%
>>> EVALUATION CONCLUSION: Gaussian Naive Bayes performs significantly better!
--------------------------------------------------------------------------------
Sample Test Predictions:
Sample #0: Actual=class_0 | Pred=class_0 | Confidence=100.0% [CORRECT]
Sample #5: Actual=class_0 | Pred=class_0 | Confidence=100.0% [CORRECT]
Sample #10: Actual=class_1 | Pred=class_1 | Confidence=94.8%  [CORRECT]
Sample #15: Actual=class_2 | Pred=class_2 | Confidence=100.0% [CORRECT]
Sample #20: Actual=class_1 | Pred=class_1 | Confidence=100.0% [CORRECT]
[Output] Confusion matrix plot saved to 'wine_confusion_matrix.png'."""
    ).strip()

    term_t1_box = Table([[Preformatted(term_t1_clean, pre_terminal_style)]], colWidths=[printable_w])
    term_t1_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B132B')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1C2541')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(term_t1_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>2.3 Performance Metrics & Classification Report Comparison:</b>", h2_style))
    perf_data = [
        [
            Paragraph("Model Evaluated", table_header_style),
            Paragraph("Test Accuracy", table_header_style),
            Paragraph("5-Fold Cross-Val", table_header_style),
            Paragraph("Precision (Macro)", table_header_style),
            Paragraph("Recall (Macro)", table_header_style),
            Paragraph("F1-Score (Macro)", table_header_style)
        ],
        [
            Paragraph("<b>Gaussian Naïve Bayes (GaussianNB)</b>", table_cell_bold),
            Paragraph("<font color='#16A34A'><b>100.00% (54/54)</b></font>", table_cell_style),
            Paragraph("<b>96.63%</b>", table_cell_style),
            Paragraph("1.00", table_cell_style),
            Paragraph("1.00", table_cell_style),
            Paragraph("<font color='#16A34A'><b>1.00</b></font>", table_cell_bold)
        ],
        [
            Paragraph("<b>Multinomial Naïve Bayes (MultinomialNB)</b>", table_cell_bold),
            Paragraph("88.89% (48/54)", table_cell_style),
            Paragraph("84.40%", table_cell_style),
            Paragraph("0.90", table_cell_style),
            Paragraph("0.89", table_cell_style),
            Paragraph("0.89", table_cell_style)
        ]
    ]
    perf_table = Table(perf_data, colWidths=[150, 80, 80, 70, 70, printable_w - 450])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F0FDF4'), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 5))

    why_text = (
        "<b>Detailed Justification (Why GaussianNB Outperforms MultinomialNB):</b><br/>"
        "1. <b>Nature of Features:</b> The Wine dataset comprises 13 real-valued physical/chemical measurements "
        "(alcohol: 11.0–14.8%, malic acid, flavonoids, ash, color intensity). These continuous floats naturally follow bell-shaped normal distributions.<br/>"
        "2. <b>Distribution Match:</b> <code>GaussianNB</code> computes the mean (&mu;<sub>c,i</sub>) and variance (&sigma;<sub>c,i</sub><sup>2</sup>) for each continuous feature, perfectly modeling continuous chemical curves and achieving <b>100% accuracy</b>.<br/>"
        "3. <b>MultinomialNB Limitation:</b> <code>MultinomialNB</code> assumes features represent discrete occurrence counts (like word counts in NLP). Applying it to continuous floats leads to probability truncation and 6 misclassifications (88.89% accuracy)."
    )
    why_table = Table([[Paragraph(why_text, callout_style)]], colWidths=[printable_w])
    why_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF3C7')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#F59E0B')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(why_table)

    # =========================================================================
    # PAGE 3: TASK 1 VISUALIZATIONS & TASK 2 INTRODUCTION + EDA
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>2.4 Confusion Matrix Visualizations:</b>", h2_style))
    if os.path.exists("wine_confusion_matrix.png"):
        story.append(Image("wine_confusion_matrix.png", width=480, height=155))
        story.append(Paragraph("<b>Figure 1:</b> Confusion Matrix Comparison on 54 Test Samples — GaussianNB (100% Accuracy, Zero Errors) vs MultinomialNB (88.9% Accuracy, 6 Misclassifications).", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.5 Test Data Predictions by Trained GaussianNB Model:</b>", h2_style))
    sample_preds_data = [
        [
            Paragraph("Test Sample Index", table_header_style),
            Paragraph("Actual Class", table_header_style),
            Paragraph("Predicted Class", table_header_style),
            Paragraph("Confidence Probability", table_header_style),
            Paragraph("Prediction Status", table_header_style)
        ],
        [Paragraph("Sample #0", table_cell_style), Paragraph("class_0", table_cell_bold), Paragraph("class_0", table_cell_bold), Paragraph("100.00%", table_cell_style), Paragraph("<font color='#16A34A'><b>CORRECT &check;</b></font>", table_cell_style)],
        [Paragraph("Sample #5", table_cell_style), Paragraph("class_0", table_cell_bold), Paragraph("class_0", table_cell_bold), Paragraph("100.00%", table_cell_style), Paragraph("<font color='#16A34A'><b>CORRECT &check;</b></font>", table_cell_style)],
        [Paragraph("Sample #10", table_cell_style), Paragraph("class_1", table_cell_bold), Paragraph("class_1", table_cell_bold), Paragraph("94.82%", table_cell_style), Paragraph("<font color='#16A34A'><b>CORRECT &check;</b></font>", table_cell_style)],
        [Paragraph("Sample #15", table_cell_style), Paragraph("class_2", table_cell_bold), Paragraph("class_2", table_cell_bold), Paragraph("100.00%", table_cell_style), Paragraph("<font color='#16A34A'><b>CORRECT &check;</b></font>", table_cell_style)],
        [Paragraph("Sample #20", table_cell_style), Paragraph("class_1", table_cell_bold), Paragraph("class_1", table_cell_bold), Paragraph("100.00%", table_cell_style), Paragraph("<font color='#16A34A'><b>CORRECT &check;</b></font>", table_cell_style)]
    ]
    sample_preds_table = Table(sample_preds_data, colWidths=[90, 95, 95, 110, printable_w - 390])
    sample_preds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(sample_preds_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Graded Lab Task 2: Loan Default Prediction & EDA (Real Dataset)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceBefore=1, spaceAfter=4))

    t2_prob = (
        "<b>Task Statement:</b> Load the real loan dataset (<code>loan_data.csv</code> from LendingClub, 9,578 records). "
        "Perform in-depth Exploratory Data Analysis (EDA) to understand loan default drivers and risk factors. "
        "Preprocess the dataset and encode categorical attributes. Train a Naïve Bayes Classifier to predict whether "
        "a borrower will fail to repay their loan (<code>not.fully.paid = 1</code>). Evaluate model performance and perform predictions on sample customer profiles."
    )
    t2_prob_table = Table([[Paragraph(t2_prob, callout_style)]], colWidths=[printable_w])
    t2_prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#93C5FD')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t2_prob_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3.1 Exploratory Data Analysis (EDA) Insights & Quantitative Findings:</b>", h2_style))
    eda_summary_text = (
        "&bull; <b>Dataset Scale:</b> 9,578 records across 14 financial features with <b>zero missing values</b>.<br/>"
        "&bull; <b>Class Imbalance:</b> 8,045 borrowers (<b>83.99%</b>) fully paid (0), whereas 1,533 borrowers (<b>16.01%</b>) defaulted (1) [Ratio: ~5.25:1].<br/>"
        "&bull; <b>Credit Profiles:</b> Defaulters show lower mean FICO scores (<b>697.83 vs 713.33</b>), higher interest rates (<b>13.20% vs 12.10%</b>), "
        "higher DTI ratios (<b>13.20 vs 12.49</b>), and 62% more credit inquiries in the last 6 months (<b>2.33 vs 1.43</b>)."
    )
    story.append(Paragraph(eda_summary_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Loan Default Rate Breakdown by Purpose:</b>", h2_style))
    purp_data = [
        [
            Paragraph("Loan Purpose", table_header_style),
            Paragraph("Total Loans", table_header_style),
            Paragraph("Defaults (not.fully.paid=1)", table_header_style),
            Paragraph("Default Rate (%)", table_header_style),
            Paragraph("Risk Profile Rating", table_header_style)
        ],
        [Paragraph("small_business", table_cell_bold), Paragraph("619", table_cell_style), Paragraph("172", table_cell_style), Paragraph("<b>27.79%</b>", table_cell_bold), Paragraph("<font color='#DC2626'><b>CRITICAL RISK</b></font>", table_cell_style)],
        [Paragraph("educational", table_cell_bold), Paragraph("343", table_cell_style), Paragraph("69", table_cell_style), Paragraph("<b>20.12%</b>", table_cell_style), Paragraph("<font color='#EA580C'><b>HIGH RISK</b></font>", table_cell_style)],
        [Paragraph("home_improvement", table_cell_bold), Paragraph("629", table_cell_style), Paragraph("107", table_cell_style), Paragraph("17.01%", table_cell_style), Paragraph("<font color='#CA8A04'><b>MODERATE RISK</b></font>", table_cell_style)],
        [Paragraph("all_other", table_cell_bold), Paragraph("2,331", table_cell_style), Paragraph("387", table_cell_style), Paragraph("16.60%", table_cell_style), Paragraph("<font color='#CA8A04'><b>MODERATE RISK</b></font>", table_cell_style)],
        [Paragraph("debt_consolidation", table_cell_bold), Paragraph("3,957", table_cell_style), Paragraph("603", table_cell_style), Paragraph("15.24%", table_cell_style), Paragraph("<font color='#16A34A'><b>AVERAGE RISK</b></font>", table_cell_style)],
        [Paragraph("credit_card", table_cell_bold), Paragraph("1,262", table_cell_style), Paragraph("146", table_cell_style), Paragraph("11.57%", table_cell_style), Paragraph("<font color='#16A34A'><b>LOW RISK</b></font>", table_cell_style)],
        [Paragraph("major_purchase", table_cell_bold), Paragraph("437", table_cell_style), Paragraph("49", table_cell_style), Paragraph("<b>11.21%</b>", table_cell_bold), Paragraph("<font color='#16A34A'><b>SAFEST CATEGORY</b></font>", table_cell_style)],
    ]
    purp_table = Table(purp_data, colWidths=[115, 75, 110, 85, printable_w - 385])
    purp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(purp_table)

    # =========================================================================
    # PAGE 4: EDA VISUALIZATIONS (ALL 3 CHARTS TOGETHER)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>3.2 Exploratory Data Visualizations:</b>", h2_style))

    if os.path.exists("loan_eda_target_dist.png"):
        story.append(Image("loan_eda_target_dist.png", width=480, height=155))
        story.append(Paragraph("<b>Figure 2:</b> LendingClub Target Distribution (Left: 84% Paid vs 16% Unpaid) and Loan Purpose Distribution split by Repayment Status (Right).", caption_style))
        story.append(Spacer(1, 4))

    if os.path.exists("loan_eda_fico_distribution.png"):
        story.append(Image("loan_eda_fico_distribution.png", width=480, height=155))
        story.append(Paragraph("<b>Figure 3:</b> FICO Credit Score Distribution Comparison — Defaulters (Red) exhibit an apparent left-shifted distribution indicating lower creditworthiness.", caption_style))
        story.append(Spacer(1, 4))

    if os.path.exists("loan_eda_correlation_matrix.png"):
        story.append(Image("loan_eda_correlation_matrix.png", width=400, height=220))
        story.append(Paragraph("<b>Figure 4:</b> Correlation Matrix Heatmap across Numerical Financial Attributes (FICO negatively correlates with Interest Rate, r = -0.71).", caption_style))

    # =========================================================================
    # PAGE 5: TASK 2 MODEL IMPLEMENTATION, METRICS & EVALUATION PLOTS
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>3.3 Preprocessing, One-Hot Encoding & Model Training:</b>", h2_style))
    story.append(Paragraph(
        "<b>Feature Encoding:</b> Categorical variable <code>purpose</code> (7 distinct values) was converted into numerical columns "
        "using Pandas <code>pd.get_dummies(drop_first=True)</code>, yielding 18 predictors. "
        "The dataset was partitioned using stratified sampling (70% train: 6,704 records, 30% test: 2,874 records) to retain the 16% default ratio.",
        body_style
    ))

    t2_code_clean = (
"""# Lab 05 Graded Task 2 - LendingClub Loan Default Prediction
# Student: Muhammad Afaq | Reg No: FA23-BSE-012 | Course: AIC354 ML Fundamentals
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

# Step 1: Load and Preprocess Loan Dataset
df = pd.read_csv('loan_data.csv')
df_encoded = pd.get_dummies(df, columns=['purpose'], drop_first=True)
X = df_encoded.drop('not.fully.paid', axis=1)
y = df_encoded['not.fully.paid']

# Step 2: Stratified Split (70% Train, 30% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Step 3: Train Gaussian Naive Bayes Model
gnb_loan = GaussianNB().fit(X_train, y_train)
y_pred = gnb_loan.predict(X_test)
y_proba = gnb_loan.predict_proba(X_test)[:, 1]

# Step 4: Evaluate Performance
acc = accuracy_score(y_test, y_pred)           # 82.60%
auc = roc_auc_score(y_test, y_proba)           # 0.6431"""
    ).strip()

    code_t2_box = Table([[Preformatted(t2_code_clean, pre_code_style)]], colWidths=[printable_w])
    code_t2_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(code_t2_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>3.4 Model Evaluation Terminal Output & Metrics:</b>", h2_style))
    term_t2_clean = (
"""================================================================================
LAB 05 - TASK 2 EVALUATION ON TEST SET (2,874 SAMPLES)
================================================================================
Gaussian Naive Bayes Model Performance:
Accuracy:  82.60%  |  ROC-AUC Score: 0.6431

Confusion Matrix:
                        Pred: Fully Paid (0)  Pred: Unpaid (1)
Actual: Fully Paid (0)                  2329                85  [TN: 2329, FP: 85]
Actual: Unpaid (1)                       415                45  [FN:  415, TP: 45]

Classification Report:
                    precision    recall  f1-score   support
    Fully Paid (0)       0.85      0.96      0.90      2414
Not Fully Paid (1)       0.35      0.10      0.15       460
          accuracy                           0.83      2874
         macro avg       0.60      0.53      0.53      2874
      weighted avg       0.77      0.83      0.78      2874"""
    ).strip()

    term_t2_box = Table([[Preformatted(term_t2_clean, pre_terminal_style)]], colWidths=[printable_w])
    term_t2_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B132B')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1C2541')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(term_t2_box)
    story.append(Spacer(1, 5))

    if os.path.exists("loan_confusion_matrix.png"):
        story.append(Image("loan_confusion_matrix.png", width=480, height=160))
        story.append(Paragraph("<b>Figure 5:</b> Loan Model Evaluation — Left: Confusion Matrix (Accuracy = 82.60%), Right: ROC Curve (ROC-AUC = 0.643).", caption_style))

    # =========================================================================
    # PAGE 6: UNDERWRITING PREDICTIONS, ANALYSIS & STUDENT DECLARATION
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>3.5 Real-World Customer Credit Underwriting Predictions:</b>", h2_style))
    story.append(Paragraph(
        "To test real operational underwriting, diverse applicants from the test set were evaluated with the trained model:",
        body_style
    ))

    cust_preds_data = [
        [
            Paragraph("Cust ID", table_header_style),
            Paragraph("FICO", table_header_style),
            Paragraph("Interest", table_header_style),
            Paragraph("DTI", table_header_style),
            Paragraph("Actual Status", table_header_style),
            Paragraph("Model Decision", table_header_style),
            Paragraph("Default Risk %", table_header_style),
            Paragraph("Underwriting Action", table_header_style)
        ],
        [Paragraph("#12", table_cell_style), Paragraph("697", table_cell_style), Paragraph("13.22%", table_cell_style), Paragraph("8.58", table_cell_style), Paragraph("Fully Paid", table_cell_style), Paragraph("<font color='#16A34A'><b>SAFE: Fully Paid</b></font>", table_cell_style), Paragraph("<b>6.34%</b>", table_cell_style), Paragraph("<font color='#16A34A'><b>APPROVE LOAN</b></font>", table_cell_bold)],
        [Paragraph("#72", table_cell_style), Paragraph("677", table_cell_style), Paragraph("20.17%", table_cell_style), Paragraph("17.32", table_cell_style), Paragraph("Fully Paid", table_cell_style), Paragraph("<font color='#DC2626'><b>RISK: Not Fully Paid</b></font>", table_cell_style), Paragraph("<b>89.34%</b>", table_cell_style), Paragraph("<font color='#DC2626'><b>REQUIRE COLLATERAL</b></font>", table_cell_bold)],
        [Paragraph("#85", table_cell_style), Paragraph("667", table_cell_style), Paragraph("19.36%", table_cell_style), Paragraph("25.47", table_cell_style), Paragraph("Fully Paid", table_cell_style), Paragraph("<font color='#DC2626'><b>RISK: Not Fully Paid</b></font>", table_cell_style), Paragraph("<b>99.91%</b>", table_cell_style), Paragraph("<font color='#DC2626'><b>REJECT APPLICATION</b></font>", table_cell_bold)],
        [Paragraph("#108", table_cell_style), Paragraph("747", table_cell_style), Paragraph("10.59%", table_cell_style), Paragraph("17.12", table_cell_style), Paragraph("Fully Paid", table_cell_style), Paragraph("<font color='#16A34A'><b>SAFE: Fully Paid</b></font>", table_cell_style), Paragraph("<b>1.67%</b>", table_cell_style), Paragraph("<font color='#16A34A'><b>INSTANT APPROVAL</b></font>", table_cell_bold)],
        [Paragraph("#128", table_cell_style), Paragraph("667", table_cell_style), Paragraph("19.36%", table_cell_style), Paragraph("23.34", table_cell_style), Paragraph("Not Paid", table_cell_style), Paragraph("<font color='#DC2626'><b>RISK: Not Fully Paid</b></font>", table_cell_style), Paragraph("<b>84.51%</b>", table_cell_style), Paragraph("<font color='#DC2626'><b>REJECT APPLICATION</b></font>", table_cell_bold)]
    ]
    cust_preds_table = Table(cust_preds_data, colWidths=[45, 45, 55, 45, 65, 105, 75, printable_w - 435])
    cust_preds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cust_preds_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Critical Analysis, Challenges & Key Learnings", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceBefore=1, spaceAfter=4))

    disc_text = (
        "<b>1. Model Selection Driven by Feature Distributions:</b> In Task 1, <code>GaussianNB</code> delivered a flawless "
        "<b>100.00% accuracy</b> because chemical wine features follow continuous normal distributions. <code>MultinomialNB</code> "
        "suffered a drop to <b>88.89%</b> due to violation of count assumptions.<br/>"
        "<b>2. Handling Real-World Class Imbalance:</b> In Task 2, an accuracy of <b>82.60%</b> reflects majority-class dominance "
        "(84% non-defaulters). Standard 0.5 decision thresholds yield low recall for defaulters (10%). However, GaussianNB's probabilistic "
        "outputs provide a viable ranking metric with <b>ROC-AUC = 0.6431</b>.<br/>"
        "<b>3. Practical Underwriting Recommendation:</b> In banking production, financial institutions should lower the decision threshold "
        "from 0.50 to 0.20 or apply SMOTE (Synthetic Minority Over-sampling Technique) to identify high-risk applicants proactively."
    )
    story.append(Paragraph(disc_text, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("5. Submission Declaration & Sign-off", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceBefore=1, spaceAfter=4))

    decl_data = [
        [
            Paragraph("<b>Student Declaration:</b><br/>"
                      "I hereby declare that this lab report and the accompanying codebase represent my own authentic work. "
                      "Both Lab Task 1 (Wine Dataset) and Lab Task 2 (LendingClub Real Dataset) have been thoroughly solved, "
                      "executed, and validated with empirical outputs and plots.", callout_style)
        ],
        [
            Paragraph("<b>Student Name:</b> Muhammad Afaq &nbsp;&nbsp;|&nbsp;&nbsp; <b>Registration No:</b> FA23-BSE-012 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Section:</b> Section A<br/>"
                      "<b>Department:</b> Department of Computer Science &bull; COMSATS University Islamabad<br/>"
                      "<b>GitHub Repository:</b> <font color='#2B6CB0'><u>https://github.com/afaqsadiq0/ML-LAB</u></font>", callout_style)
        ]
    ]
    decl_table = Table(decl_data, colWidths=[printable_w])
    decl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(decl_table)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\n[Success] Lab Report PDF generated successfully: {PDF_FILENAME}")
    print(f"File size: {os.path.getsize(PDF_FILENAME):,} bytes")

if __name__ == "__main__":
    create_lab_report()
