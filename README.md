# FitnessAI Pro — Group 02 | Seven-model AI Fitness Demo

A colorful, responsive Streamlit website for a university AI/ML presentation. **One URL for seven member models, a CV-selected final predictor, model comparisons, and transparent, rule-based wellness suggestions.** All seven saved models come directly from the existing 1,979-row academic project: this deployment does **not** retrain or change them.

## Pages

1. **Home dashboard** — project metrics, all seven members, model cards, and navigation.
2. **Final AI predictor** — uses the saved winner (Logistic Regression, selected using training 5-fold CV). Single-person and CSV batch prediction, a comparison of all seven predictions, and detailed evaluation.
3. **Model leaderboard** — interactive CV/test accuracy and precision/recall/F1 charts, metrics and limitations.
4. **Wellness studio** — transparent, rule-based general wellness suggestions; not a trained model or medical guidance.
5. **Seven individual member pages** — complete prediction, CSV upload/download, hyperparameters, tuning trials and confusion matrix.

| Member | Algorithm |
|---|---|
| SM S Weerasinghe | K-Nearest Neighbors (KNN) |
| WMHS Wijethunga | Decision Tree |
| RMJN Rathnayaka | Random Forest |
| WMDS Weesinghe | Logistic Regression |
| HCJ Gunathunga | Support Vector Machine (SVM) |
| HAP Priyadarshani | Gradient Boosting |
| SKTB Senarathna | Naive Bayes |

## Project files

```text
Group2_Fitness_AI_Deployment/
├── app.py                     # Single cloud entrypoint
├── requirements.txt           # Python dependencies
├── README.md                  # This deployment guide
├── .streamlit/
│   └── config.toml            # Color theme and upload size
├── fitness_app/
│   ├── __init__.py
│   ├── core.py                 # Original bundle loading, evaluation, prediction
│   ├── ui.py                   # Premium web pages and interactive graphs
│   ├── style.py                # Responsive dashboard styling
│   └── wellness.py             # Transparent general wellness rules
├── models/                    # All seven unchanged trained .joblib bundles
│   ├── knn.joblib
│   ├── decision_tree.joblib
│   ├── random_forest.joblib
│   ├── logistic_regression.joblib
│   ├── svm.joblib
│   ├── gradient_boosting.joblib
│   └── naive_bayes.joblib
└── data/
    └── splits/
        ├── fitness_train.csv  # 1,583 rows
        └── fitness_test.csv   # 396 rows
```

## Test on your own computer (optional)

Install **Python 3.12**. Open a terminal in this folder (the same directory as `app.py`). Run:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

On macOS/Linux, replace `py -m` with `python3 -m`. Streamlit usually opens `http://localhost:8501`. You do not need to retrain any models.

## Deploy on Streamlit Community Cloud

1. Visit https://github.com/new, log into GitHub, and create a repository such as `group2-fitness-ai-pro`.
2. **Extract the ZIP**. In GitHub choose **Add file → Upload files** and upload **the contents of the extracted `Group2_Fitness_AI_Deployment` folder**, not the ZIP itself. Confirm `app.py` and `requirements.txt` are at the repository root, and the `fitness_app/`, `models/`, and `data/` directories are present. Commit changes. Hidden `.streamlit/config.toml` is optional for deployment if GitHub’s web uploader doesn't include it; the app will still work with Streamlit's default theme, but upload it to preserve our custom theme.
3. Visit https://share.streamlit.io, sign in using GitHub, and select **Create app → Deploy from your repository**.
4. Choose your GitHub repository, `main` branch, and set **main file path: `app.py`**. In advanced settings select Python **3.12** if available; preserve dependency compatibility with the included pinned scikit-learn version.
5. Deploy. Wait for dependencies and startup to finish. If successful, share the resulting `*.streamlit.app` link with the group. **Group members need only a browser, not Python or GitHub.**
6. Test Home → Final AI predictor → Single prediction, then Model leaderboard and two individual member models. To debug a failed deployment, open **Manage app → Logs** and verify that `requirements.txt`, all `.joblib` bundles and both split CSVs uploaded.

**Privacy for a public demonstration:** Use fabricated or consented non-identifying test inputs. The app does not implement an account system or persistent upload storage. Do not submit names, contact details, or identifiable medical records. Model loading uses trusted bundled joblib files only.

## Understanding the app

- The dataset classes are `0 = Not Fit`, `1 = Fit`. These are labels in the assigned dataset and **not medical fitness diagnoses**.
- All seven pipelines are pretrained using the **same 1,583 training / 396 testing** split of `fitness_preprocessed.csv` (1,979 total records).
- The final model is selected by **highest mean five-fold training cross-validation accuracy**, not by comparing held-out test results. As packaged, the winner is Logistic Regression by WMDS Weesinghe.
- Training preprocessing contained steps fitted within training folds, but the source dataset had **imputation and outlier filtering on all 2,000 original rows before splitting**. This may introduce data leakage; treat results as coursework evaluation, not validated deployment accuracy.
- The dashboard displays each model’s original saved tuning configurations, evaluation metrics, confusion matrix, and original inference pipeline.
- A classifier’s Fit-label score is **not a clinical risk estimate**. The SVM margin, if displayed, is **not** a probability.
- The **wellness studio** uses only four input fields and these simple demo heuristics: sleep under 7 hours, dataset `activity_index` below 3, dataset `nutrition_quality` below 5, and `smokes = Yes`. These cutoffs (especially the dataset-index cutoffs) are not validated clinical thresholds. They trigger general suggestions only; they are **not model explanations or a personalized medical prescription**.
- The original dataset includes binary gender coding only; that constraint and potential fairness issues are acknowledged.

## Batch CSV format

The uploader accepts a CSV with these columns, in any order:

`age,height_cm,weight_kg,heart_rate,blood_pressure,sleep_hours,nutrition_quality,activity_index,smokes,gender`

Example:

```csv
age,height_cm,weight_kg,heart_rate,blood_pressure,sleep_hours,nutrition_quality,activity_index,smokes,gender
35,175,72,64,118,8,8,4.2,No,Male
```

Upload up to 10,000 rows. Download the results from each page. The final page also adds the seven independent votes to the resulting CSV. The uploader does not save the uploaded CSV to application disk.

## Troubleshooting

- **ModuleNotFoundError: streamlit** — run `py -m pip install -r requirements.txt` in your local environment.
- **Missing trained model or data split** — confirm `models/*.joblib` and `data/splits/*.csv` exist with their original names.
- **Saved model version error** — the included bundles use `scikit-learn==1.8.0`; install dependencies from this repo using a supported Python version.
- **Poor appearance on GitHub upload** — GitHub is a code host, not the live site. Use the `streamlit.app` link and preserve `.streamlit/config.toml` for the theme.
