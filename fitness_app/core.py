"""Inference and evaluation for the bundled seven pretrained fitness models.

Trained using the 1,979-row cleaned fitness dataset; split: 1,583/396.
Models are loaded only from this repository's trusted bundled files.
Predictions are educational dataset labels, not medical assessments.
"""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import numpy as np
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
MODEL_DIR = ROOT / 'models'

TARGET='is_fit'
NUMERIC=['age','height_cm','weight_kg','heart_rate','blood_pressure','sleep_hours','nutrition_quality','activity_index','bmi']
BINARY=['smokes','gender_M']
FEATURES=NUMERIC+BINARY
RAW_FIELDS=['age','height_cm','weight_kg','heart_rate','blood_pressure','sleep_hours','nutrition_quality','activity_index','smokes','gender']
MODEL_INFO={
 'knn':{'name':'K-Nearest Neighbors (KNN)','comparison_name':'KNN','member':'SM S Weerasinghe','details':'Distance-based classifier; neighbors, distance and weights are tuned.'},
 'decision_tree':{'name':'Decision Tree','comparison_name':'Decision Tree','member':'WMHS Wijethunga','details':'Interpretable tree rules; split criterion, tree depth and minimum leaf size are tuned.'},
 'logistic_regression':{'name':'Logistic Regression','comparison_name':'Logistic Regression','member':'WMDS Weesinghe','details':'Linear binary classifier; regularization and class weights are tuned.'},
 'random_forest':{'name':'Random Forest','comparison_name':'Random Forest','member':'RMJN Rathnayaka','details':'Ensemble of bagged trees; number of trees and tree complexity are tuned.'},
 'svm':{'name':'Support Vector Machine (SVM)','comparison_name':'SVM','member':'HCJ Gunathunga','details':'Maximum-margin classifier; kernel, C and gamma are tuned.'},
 'gradient_boosting':{'name':'Gradient Boosting','comparison_name':'Gradient Boosting','member':'HAP Priyadarshani','details':'Sequential ensemble; learning rate, trees and depth are tuned.'},
 'naive_bayes':{'name':'Gaussian Naive Bayes','comparison_name':'Naive Bayes','member':'SKTB Senarathna','details':'Probability-based model; variance smoothing is tuned.'},
}
MODEL_ORDER=['knn','decision_tree','random_forest','logistic_regression','svm','gradient_boosting','naive_bayes']
SEED=42
CV_FOLDS=5

def load_split():
    """Load evaluation data, exactly as used in the training project."""
    train = pd.read_csv(DATA / 'splits' / 'fitness_train.csv')
    test = pd.read_csv(DATA / 'splits' / 'fitness_test.csv')
    for frame in (train, test):
        missing = set(FEATURES + [TARGET]) - set(frame.columns)
        if missing:
            raise ValueError(f'Split data is missing: {sorted(missing)}')
    return train[FEATURES], test[FEATURES], train[TARGET].astype(int), test[TARGET].astype(int)

@lru_cache(maxsize=8)
def load_bundle(slug):
    if slug not in MODEL_INFO: raise ValueError(f'Unknown model {slug}')
    file=MODEL_DIR/f'{slug}.joblib'
    if not file.exists(): raise FileNotFoundError(f'Missing {file.name}; deploy the complete models/ directory.')
    bundle=joblib.load(file)
    if not isinstance(bundle,dict) or not {'pipeline','summary','tuning'}<=set(bundle):
        raise ValueError(f'Model file has an invalid format: {file.name}')
    return bundle

def load_model(slug):
    return load_bundle(slug)['pipeline']

def evaluation_table():
    return pd.DataFrame([{**load_bundle(slug)['summary'], 'member': MODEL_INFO[slug]['member']} for slug in MODEL_ORDER]).sort_values(['cv_accuracy_mean','cv_f1_mean','model'],ascending=[False,False,True]).reset_index(drop=True)

def winner_slug():
    """Select only by training-fold CV accuracy, never by held-out test results."""
    return str(evaluation_table().iloc[0]['slug'])

def evaluation_row(slug):
    return load_bundle(slug)['summary']

def _parse_binary(value,field):
    if pd.isna(value): raise ValueError(f'Missing {field}')
    key=str(value).strip().lower()
    choices=({'0':0,'1':1,'no':0,'yes':1,'false':0,'true':1,'n':0,'y':1}
             if field=='smokes' else {'0':0,'1':1,'f':0,'m':1,'female':0,'male':1})
    if key not in choices: raise ValueError(f'Invalid {field}: {value!r}')
    return choices[key]

def prepare_features(raw):
    if raw.empty: raise ValueError('Provide at least one person.')
    missing=[col for col in RAW_FIELDS if col not in raw.columns and not (col=='gender' and 'gender_M' in raw.columns)]
    if missing: raise ValueError('Missing columns: '+', '.join(missing))
    result=pd.DataFrame(index=raw.index); notices=[]
    X_train,_,_,_=load_split()
    for field in NUMERIC:
        if field=='bmi':continue
        try: vals=pd.to_numeric(raw[field],errors='raise').astype(float)
        except (TypeError,ValueError) as exc: raise ValueError(f'{field} must be numeric.') from exc
        if not np.isfinite(vals.to_numpy(dtype=float)).all(): raise ValueError(f'{field} includes missing/non-finite values.')
        result[field]=vals
        bounds=X_train[field].agg(['min','max'])
        if ((vals<float(bounds['min'])) | (vals>float(bounds['max']))).any():
            notices.append(f'{field} outside training range [{bounds["min"]:g}, {bounds["max"]:g}].')
    if (result['height_cm']<=0).any() or (result['weight_kg']<=0).any(): raise ValueError('Height and weight must be positive.')
    result['bmi']=result['weight_kg']/((result['height_cm']/100)**2)
    result['smokes']=raw['smokes'].map(lambda x:_parse_binary(x,'smokes')).astype(int)
    key='gender' if 'gender' in raw.columns else 'gender_M'
    result['gender_M']=raw[key].map(lambda x:_parse_binary(x,'gender')).astype(int)
    return result[FEATURES],notices

def infer(slug,input_data):
    x,notices=prepare_features(input_data)
    model=load_model(slug)
    pred=np.asarray(model.predict(x),dtype=int)
    out=input_data.copy();out['calculated_bmi']=x['bmi'].round(2).to_numpy()
    out['predicted_is_fit']=pred
    out['prediction']=np.where(pred==1,'Fit','Not Fit')
    if hasattr(model,'predict_proba'):
        out['model_score_fit']=model.predict_proba(x)[:,list(model.classes_).index(1)].round(4)
    elif hasattr(model,'decision_function'):
        out['decision_margin']=np.asarray(model.decision_function(x)).round(4)
    return out,notices

def predict_all(input_data):
    x,_=prepare_features(input_data)
    return pd.DataFrame({MODEL_INFO[slug]['comparison_name']:np.where(load_model(slug).predict(x)==1,'Fit','Not Fit')
                         for slug in MODEL_ORDER},index=input_data.index)
