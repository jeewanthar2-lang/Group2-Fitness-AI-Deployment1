"""FitnessAI Pro | Premium responsive Streamlit showcase.

Seven original pre-trained pipelines, existing held-out evaluation data,
and a clearly separated, rule-based wellness-education layer.
"""
from __future__ import annotations

import html
import io
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from fitness_app.core import (
    MODEL_INFO, MODEL_ORDER, RAW_FIELDS, load_bundle, load_model, load_split,
    winner_slug, evaluation_row, evaluation_table, infer, predict_all,
)
from fitness_app.style import GLOBAL_CSS
from fitness_app.wellness import RULE_EXPLANATION, get_wellness_suggestions

PAGES = ['home', 'final', 'comparison', 'wellness'] + MODEL_ORDER
LABELS = {
    'home': '🏠  Home dashboard',
    'final': '✨  Final AI predictor',
    'comparison': '📊  Model leaderboard',
    'wellness': '💚  Wellness studio',
    'knn': '🧭  K-Nearest Neighbors',
    'decision_tree': '🌳  Decision Tree',
    'random_forest': '🌲  Random Forest',
    'logistic_regression': '📈  Logistic Regression',
    'svm': '🎯  Support Vector Machine',
    'gradient_boosting': '⚡  Gradient Boosting',
    'naive_bayes': '🧪  Naive Bayes',
}
BRAND = {
    'knn': ('🧭', '#7054ec'),
    'decision_tree': ('🌳', '#0baa8e'),
    'random_forest': ('🌲', '#1c8bcb'),
    'logistic_regression': ('📈', '#e87951'),
    'svm': ('🎯', '#d351ab'),
    'gradient_boosting': ('⚡', '#e4a52e'),
    'naive_bayes': ('🧪', '#567ab7'),
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def markup(value: str) -> None:
    st.markdown(value, unsafe_allow_html=True)


def navigate(page: str) -> None:
    st.session_state['fitness_navigation'] = page


def page_setup(title: str = 'FitnessAI Pro | Group 02') -> None:
    st.set_page_config(page_title=title, page_icon='💜', layout='wide', initial_sidebar_state='expanded')
    markup(GLOBAL_CSS)


def banner(label: str, title: str, description: str) -> None:
    markup(f'''<div class="page-hero"><div class="eyebrow">{esc(label)}</div>
       <h1>{esc(title)}</h1><p>{esc(description)}</p></div>''')


def section(title: str, subtitle: str = '') -> None:
    markup(f'<div class="section-hd">{title}</div>' +
           (f'<div class="section-sub">{esc(subtitle)}</div>' if subtitle else ''))


def kpis(items: list[tuple[str, str, str, str]]) -> None:
    colors = ('violet','cyan','mint','amber')
    cards = ''.join(
        f'<div class="kpi {colors[i%4]}"><div class="kpi-icon">{esc(icon)}</div>'
        f'<div class="kpi-num">{esc(number)}</div><div class="kpi-label">{esc(label)}</div></div>'
        for i, (icon, number, label, _) in enumerate(items)
    )
    markup(f'<div class="kpi-grid">{cards}</div>')


def footer() -> None:
    markup('''<div class="footer">🎓 IT2011 · Group 02 · Seven supervised ML models trained on the
        1,979-record preprocessed fitness dataset. Source data was globally cleaned before
        splitting, which may introduce data leakage. Results predict an educational dataset
        label, not medical fitness or a diagnosis. Please use fictional or non-identifying
        data for demonstration.</div>''')


def sidebar() -> str:
    with st.sidebar:
        markup('''<div class="brandbox"><div class="brandicon">💜</div>
            <div><div class="brandname">FitnessAI <b>Pro</b></div>
            <div class="brandsub">GROUP 02 · ML LAB</div></div></div>''')
        st.caption('A premium seven-model AI showcase')
        if 'fitness_navigation' not in st.session_state:
            st.session_state['fitness_navigation'] = 'home'
        selected = st.radio('EXPLORE THE SITE', PAGES,
                            format_func=lambda value: LABELS[value],
                            key='fitness_navigation')
        st.divider()
        win = winner_slug()
        record = evaluation_row(win)
        markup(f'''<div class="sidebar-cap">🏆 Winner · {esc(MODEL_INFO[win]['comparison_name'])}</div>
            <p style="font-size:12px;margin:12px 0;color:#cad4e9">Mean 5-fold CV:
            <b style="color:#76f4df">{record['cv_accuracy_mean']:.2%}</b><br>
            Held-out test: <b>{record['test_accuracy']:.2%}</b></p>''')
        st.caption('Seven trained classifiers · 1,583 train / 396 test · 1,979 total')
        st.divider()
        st.caption('Educational showcase only · Not medical advice · Do not upload identifying health information.')
    return selected


def home() -> None:
    winner = winner_slug()
    score = evaluation_row(winner)
    markup(f'''<div class="hero"><div class="eyebrow">✨ Welcome to the intelligent fitness lab</div>
      <div class="hero-title">Your fitness data.<br>Seven AI perspectives.</div>
      <div class="hero-description">Explore our student-built machine learning models,
      try a Fit / Not Fit classification, compare model performance and discover
      transparent, general wellness ideas. All in one beautiful space.</div>
      <div class="hero-chips"><span class="hero-chip">🤖 7 tuned models</span>
      <span class="hero-chip">🏆 CV-selected final model</span>
      <span class="hero-chip">💚 Rule-based wellness ideas</span></div>
      <div class="hero-icon">💠</div></div>''')
    kpis([('🧠', '07', 'ML algorithms', ''),
          ('🗃️', '1,979', 'Preprocessed records', ''),
          ('📊', '1,583 / 396', 'Train / test rows', ''),
          ('🏆', f"{score['cv_accuracy_mean']:.2%}", 'Top CV accuracy', '')])
    left,right = st.columns([1,1])
    with left:
        if st.button('✨ Try the final AI predictor', type='primary', use_container_width=True,
                     key='home_final', on_click=navigate, args=('final',)):
            pass
    with right:
        if st.button('📊 Explore the model leaderboard', use_container_width=True,
                     key='home_comparison', on_click=navigate, args=('comparison',)):
            pass
    section('👥 Meet the builders', 'Seven team members. Seven different learning algorithms. One shared training and testing split.')
    for start in range(0,len(MODEL_ORDER),3):
        slugs = MODEL_ORDER[start:start+3]
        columns = st.columns(3)
        for column,slug in zip(columns,slugs):
            info = MODEL_INFO[slug]
            row = evaluation_row(slug)
            icon,color = BRAND[slug]
            with column:
                markup(f'''<div class="member-card" style="--accent:{color}">
                   <div class="member-top"><div class="member-icon">{icon}</div>
                   <span class="member-num">MODEL {MODEL_ORDER.index(slug)+1:02d}</span></div>
                   <div class="member-name">{esc(info['member'])}</div>
                   <div class="member-model">{esc(info['name'])}</div>
                   <div class="member-about">{esc(info['details'])}</div>
                   <div class="member-stats"><div><b>{row['cv_accuracy_mean']:.2%}</b><span>Cross-validation</span></div>
                   <div><b>{row['test_accuracy']:.2%}</b><span>Test accuracy</span></div></div>
                   </div>''')
                st.button('Open predictor ↗', key=f'member_go_{slug}', use_container_width=True,
                          on_click=navigate, args=(slug,))
    section('🏆 Final model spotlight', 'The winner is chosen using training cross-validation, not by choosing the highest held-out test score.')
    markup(f'''<div class="promo"><strong>✨ {esc(MODEL_INFO[winner]['name'])}</strong>
       by {esc(MODEL_INFO[winner]['member'])} leads with <b>{score['cv_accuracy_mean']:.2%}</b>
       mean five-fold training CV accuracy. Held-out test accuracy is <b>{score['test_accuracy']:.2%}</b>.
       The final prediction comes from this single selected model; the other models provide a comparison,
       not a replacement result.</div>''')
    section('💚 Wellness, without the guesswork', 'See general habit ideas based on transparent, simple rules—not hidden medical judgments.')
    markup('''<div class="promo">🌙 Sleep &nbsp;·&nbsp; 🚶 Everyday movement &nbsp;·&nbsp; 🥗 Nutrition
       &nbsp;·&nbsp; 💚 Smoking support<br><strong>Important:</strong> The suggestions are not
       model explanations, diagnostic assessments, or personalized treatment recommendations.</div>''')
    st.button('Visit the wellness studio →', key='home_wellness',
              on_click=navigate, args=('wellness',))
    footer()


def person_form(slug: str) -> None:
    """Use identical raw feature definitions and model code for every page."""
    st.markdown('#### 🧍 Enter a person’s details')
    st.caption('Demo values are pre-filled. Change them to test a prediction. Numeric values are never saved to a user profile.')
    with st.form(key=f'person_form_{slug}', border=True):
        st.markdown('**01 · Profile & physical measurements**')
        c1,c2,c3 = st.columns(3)
        with c1:
            age = st.number_input('Age (years)', min_value=1, max_value=120, value=35, step=1, key=f'age_{slug}')
            height_cm = st.number_input('Height (cm)', min_value=1.0, max_value=250.0, value=175.0, step=0.5, key=f'height_{slug}')
        with c2:
            weight_kg = st.number_input('Weight (kg)', min_value=1.0, max_value=350.0, value=72.0, step=0.5, key=f'weight_{slug}')
            heart_rate = st.number_input('Heart rate (bpm)', min_value=1.0, max_value=250.0, value=64.0, step=0.1, key=f'hr_{slug}')
        with c3:
            blood_pressure = st.number_input('Blood pressure (dataset value)', min_value=1.0, max_value=250.0, value=118.0, step=0.1, key=f'bp_{slug}', help='One numeric dataset field, NOT a full systolic/diastolic blood pressure measurement.')
            sleep_hours = st.number_input('Sleep hours', min_value=0.0, max_value=24.0, value=8.0, step=0.1, key=f'sleep_{slug}')
        st.markdown('**02 · Lifestyle & dataset indicators**')
        a,b = st.columns(2)
        with a:
            nutrition_quality = st.number_input('Nutrition quality (dataset 0–10)', min_value=0.0, max_value=10.0, value=8.0, step=0.1, key=f'nutrition_{slug}')
            smokes = st.radio('Smokes?', ['No','Yes'], horizontal=True, key=f'smokes_{slug}')
        with b:
            activity_index = st.number_input('Activity index (dataset 0–10)', min_value=0.0, max_value=10.0, value=4.2, step=0.1, key=f'activity_{slug}', help='An index score in this dataset; not minutes/hours of exercise.')
            gender = st.radio('Gender (dataset encoding)', ['Female','Male'], index=1, horizontal=True, key=f'gender_{slug}', help='The source dataset includes only Female (0) and Male (1), a limitation of the dataset.')
        submitted = st.form_submit_button('✨ Predict Fit / Not Fit', type='primary', use_container_width=True)
    if submitted:
        values = dict(age=age,height_cm=height_cm,weight_kg=weight_kg,heart_rate=heart_rate,
                      blood_pressure=blood_pressure,sleep_hours=sleep_hours,
                      nutrition_quality=nutrition_quality,activity_index=activity_index,
                      smokes=smokes,gender=gender)
        try:
            pred,warnings = infer(winner_slug() if slug=='final' else slug,pd.DataFrame([values]))
            st.session_state[f'prediction_{slug}'] = (pred,warnings,values)
        except (ValueError,FileNotFoundError) as exc:
            st.session_state.pop(f'prediction_{slug}',None)
            st.error(f'Please check the input: {exc}')


def suggestions_html(values: dict) -> None:
    tips = get_wellness_suggestions(values)
    cards = ''.join(
        f'''<div class="tip-card {esc(s.tint)}"><div class="tip-top">
        <div class="tip-icon">{s.icon}</div><div><div class="tip-title">{esc(s.title)}</div>
        <div class="tip-cat">{esc(s.category)}</div></div></div>
        <div class="tip-desc">{esc(s.description)}</div></div>'''
        for s in tips)
    markup(f'<div class="tip-grid">{cards}</div>')
    markup(f'<div class="note"><strong>How these suggestions work:</strong> {esc(RULE_EXPLANATION)}<br>'
           'They are general educational ideas, not a diagnosis, treatment or a reason for the model label.</div>')


def show_person_result(slug: str) -> None:
    saved = st.session_state.get(f'prediction_{slug}')
    if saved is None:
        markup('''<div class="promo">🪄 Ready when you are. Fill in the form and select
               <strong>Predict Fit / Not Fit</strong> to see the model’s output.</div>''')
        return
    frame,warnings,values = saved
    row = frame.iloc[0]
    fit = row['prediction']=='Fit'
    markup(f'''<div class="result {'fit' if fit else 'notfit'}">
       <div class="result-icon">{'✅' if fit else '🌱'}</div>
       <div><div class="result-class">Educational model output · class {int(row['predicted_is_fit'])}</div>
       <div class="result-title">{'FIT' if fit else 'NOT FIT'} — predicted</div>
       <div class="result-sub">This is the saved classifier’s prediction of <code>is_fit</code>,
       not a health diagnosis, a validated fitness assessment or an explanation of health status.</div></div></div>''')
    c1,c2,c3=st.columns(3)
    c1.metric('Predicted class',str(row['prediction']))
    c2.metric('Calculated BMI',f"{row['calculated_bmi']:.2f}")
    if 'model_score_fit' in frame:
        c3.metric('Model score (Fit)',f"{row['model_score_fit']:.3f}")
        st.caption('The score is a model estimate for the Fit label, **not** a calibrated medical probability or health risk.')
    elif 'decision_margin' in frame:
        c3.metric('Decision margin',f"{row['decision_margin']:+.3f}")
        st.caption('An SVM decision margin is not a probability. Positive margins favour the Fit class.')
    else:
        c3.metric('Model',MODEL_INFO[winner_slug() if slug=='final' else slug]['comparison_name'])
    for message in warnings:
        st.warning('⚠️ Outside training data — ' + message)
    section('💚 Your wellness inspiration', 'These suggestions depend on lifestyle inputs only, not on why the model predicted Fit or Not Fit.')
    suggestions_html(values)
    if slug=='final':
        section('🗳️ How did all seven models vote?', 'The final result above is from the CV-selected winner; other models are shown for comparison.')
        vote = predict_all(pd.DataFrame([values])).iloc[0]
        fit_votes = int((vote == 'Fit').sum())
        left,right=st.columns(2)
        left.metric('Models predicting Fit',f'{fit_votes} / 7')
        right.metric('Models predicting Not Fit',f'{7-fit_votes} / 7')
        view=pd.DataFrame({'Algorithm':vote.index,'Prediction':vote.values})
        view['Selected final model']=view['Algorithm'].eq(MODEL_INFO[winner_slug()]['comparison_name']).map({True:'🏆 Winner',False:'—'})
        st.dataframe(view,hide_index=True,use_container_width=True)
    markup('''<div class="note"><strong>Privacy reminder:</strong> Demo inputs live in the active
      Streamlit session only. Avoid entering identifiable personal or medical information.</div>''')


def batch_tab(slug: str) -> None:
    st.markdown('#### 📂 Predict an entire CSV')
    st.caption('Use at most 10,000 rows. Required inputs: '+', '.join(RAW_FIELDS)+'. No target column is required.')
    example=pd.DataFrame([{'age':35,'height_cm':175,'weight_kg':72,'heart_rate':64,
       'blood_pressure':118,'sleep_hours':8,'nutrition_quality':8,'activity_index':4.2,
       'smokes':'No','gender':'Male'}])
    st.download_button('⬇ Download sample CSV',data=example.to_csv(index=False).encode(),
                       file_name='fitness_sample_input.csv',mime='text/csv',key=f'sample_{slug}')
    uploaded=st.file_uploader('Select a CSV file',type=['csv'],key=f'upload_{slug}')
    if st.button('⚡ Run batch prediction',type='primary',disabled=uploaded is None,key=f'predict_batch_{slug}'):
        try:
            frame = pd.read_csv(io.BytesIO(uploaded.getvalue()))
            if len(frame)>10000:
                raise ValueError('This demo supports up to 10,000 people per upload.')
            predictions,warnings = infer(winner_slug() if slug=='final' else slug,frame)
            if slug=='final':
                all_votes = predict_all(frame)
                for col in all_votes:
                    predictions['vote_'+col.lower().replace(' ','_')] = all_votes[col].to_numpy()
            st.session_state[f'batch_{slug}'] = (predictions,warnings)
        except (ValueError,FileNotFoundError,pd.errors.ParserError,UnicodeDecodeError,KeyError) as exc:
            st.session_state.pop(f'batch_{slug}',None)
            st.error(f'Unable to process this CSV: {exc}')
    result=st.session_state.get(f'batch_{slug}')
    if result:
        df,warnings=result
        st.success(f'✅ Predictions created for {len(df):,} row(s).')
        for warning in warnings: st.warning('Outside training data — '+warning)
        st.dataframe(df.head(100),hide_index=True,use_container_width=True)
        st.download_button('⬇ Download results CSV',data=df.to_csv(index=False).encode(),
                           file_name=f'{slug}_predictions.csv',mime='text/csv',type='primary',key=f'download_{slug}')
        if len(df)>100: st.caption('Preview is limited to 100 rows; the download includes every predicted row.')
        st.caption('Uploaded CSV records are not written to disk by this application.')


def plot_layout(fig: go.Figure, height: int = 380) -> go.Figure:
    fig.update_layout(height=height,margin=dict(l=12,r=15,t=30,b=26),
        font=dict(family='DM Sans, Arial',size=12,color='#58627c'),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h',yanchor='bottom',y=1.08,x=0),
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(gridcolor='#e8ecf6',zeroline=False))
    return fig


def accuracy_chart(table: pd.DataFrame) -> None:
    names = table['model'].to_list()
    cv=(100*table['cv_accuracy_mean']).to_list()
    test=(100*table['test_accuracy']).to_list()
    fig=go.Figure()
    fig.add_trace(go.Bar(name='Training CV accuracy',x=names,y=cv,
              marker_color='#7455ed',hovertemplate='%{x}<br>CV accuracy: %{y:.2f}%<extra></extra>'))
    fig.add_trace(go.Bar(name='Held-out test accuracy',x=names,y=test,
              marker_color='#17b8c2',hovertemplate='%{x}<br>Test accuracy: %{y:.2f}%<extra></extra>'))
    fig.update_layout(barmode='group',yaxis_title='Accuracy (%)',xaxis_tickangle=-28)
    plot_layout(fig,410)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})


def confusion_chart(record: dict) -> None:
    z=[[int(record['tn']),int(record['fp'])],[int(record['fn']),int(record['tp'])]]
    fig=go.Figure(data=go.Heatmap(z=z,x=['Predicted Not Fit','Predicted Fit'],
        y=['Actual Not Fit','Actual Fit'],colorscale=[[0,'#f0efff'],[1,'#6852e8']],
        showscale=False,text=z,texttemplate='%{text}',
        textfont=dict(size=18,color='#25234d'),hovertemplate='%{x}<br>%{y}<br>Count: %{z}<extra></extra>'))
    fig.update_layout(yaxis_autorange='reversed',xaxis_side='bottom')
    plot_layout(fig,315)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})


def model_evaluation(slug: str) -> None:
    chosen=winner_slug() if slug=='final' else slug
    record=evaluation_row(chosen)
    section('📊 Model performance', 'These saved results are from the same 1,583/396 split for all seven algorithms.')
    a,b,c,d=st.columns(4)
    a.metric('5-fold CV accuracy',f"{record['cv_accuracy_mean']:.2%}")
    b.metric('Held-out accuracy',f"{record['test_accuracy']:.2%}")
    c.metric('Held-out F1',f"{record['test_f1']:.2%}")
    d.metric('Tuned variants',int(record['variants_tested']))
    e,f,g=st.columns(3)
    e.metric('Precision',f"{record['test_precision']:.2%}")
    f.metric('Recall',f"{record['test_recall']:.2%}")
    g.metric('ROC-AUC',f"{record['test_roc_auc']:.3f}")
    col1,col2=st.columns([1.15,1])
    with col1:
        st.markdown('**🧩 Confusion matrix · test set**')
        confusion_chart(record)
        st.caption('Not Fit is class 0; Fit is class 1. Values are held-out test counts.')
    with col2:
        st.markdown('**⚙️ Best tuned hyperparameters**')
        try:
            best=json.loads(str(record['best_parameters']))
            st.json(best,expanded=True)
        except json.JSONDecodeError:
            st.code(str(record['best_parameters']))
        st.caption('Parameters were chosen by training-fold cross-validation, not by the held-out test set.')
    with st.expander('See every GridSearchCV configuration and score'):
        variants=load_bundle(chosen)['tuning'].sort_values('rank').copy()
        st.dataframe(variants,hide_index=True,use_container_width=True)
        top=variants.nlargest(8,'cv_accuracy').iloc[::-1]
        fig=go.Figure(go.Bar(x=100*top['cv_accuracy'],y=top['parameters'],orientation='h',marker_color='#6e58ea',
                          hovertemplate='CV accuracy %{x:.2f}%<extra></extra>'))
        plot_layout(fig,max(300,60*len(top)))
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    st.caption(f"Training: {record['train_rows']:,} / Testing: {record['test_rows']:,} from {record['total_preprocessed_rows']:,} preprocessed records. Some preprocessing occurred globally before splitting, so leakage remains a limitation.")


def comparison() -> None:
    banner('🏁 Seven models · One evaluation standard', 'Model performance leaderboard',
           'See how every group member’s tuned classifier performs on the same training cross-validation and held-out test split.')
    table=evaluation_table()
    win=winner_slug()
    top=evaluation_row(win)
    kpis([('🏆',MODEL_INFO[win]['comparison_name'],'Top mean CV model',''),
          ('📚','5-fold','Train cross-validation',''),
          ('⚖️','396','Shared test records',''),
          ('🎯',f"{top['cv_accuracy_mean']:.2%}",'Winning CV accuracy','')])
    section('📊 Cross-validation versus test', 'Training cross-validation ranks the models; held-out test scores describe generalization and do not choose the winner.')
    accuracy_chart(table)
    section('🏅 Complete model ranking')
    show=table[['model','member','cv_accuracy_mean','cv_accuracy_std','test_accuracy',
                'test_precision','test_recall','test_f1','test_roc_auc','variants_tested']].copy()
    for key in ['cv_accuracy_mean','cv_accuracy_std','test_accuracy','test_precision','test_recall','test_f1']:
        show[key]=(show[key]*100).round(2)
    show.columns=['Model','Member','CV accuracy %','CV SD %','Test accuracy %',
                  'Precision %','Recall %','F1 %','ROC-AUC','Tuned variants']
    st.dataframe(show,hide_index=True,use_container_width=True)
    section('🎯 Precision, recall and F1')
    fig=go.Figure()
    for key,label,color in [('test_precision','Precision','#7053ee'),('test_recall','Recall','#11b8c6'),('test_f1','F1','#f49b6c')]:
        fig.add_trace(go.Bar(name=label,x=table['model'],y=100*table[key],marker_color=color))
    fig.update_layout(barmode='group',yaxis_title='Held-out score (%)',xaxis_tickangle=-28)
    plot_layout(fig,390)
    st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    markup(f'''<div class="promo"><strong>🏆 Selected: {esc(MODEL_INFO[win]['name'])}</strong>
      · {esc(MODEL_INFO[win]['member'])} · Mean 5-fold CV accuracy {top['cv_accuracy_mean']:.2%}.
      Test accuracy {top['test_accuracy']:.2%}. CV-selected means test results were not used to choose the winner.</div>''')
    markup('''<div class="note"><strong>Limitations:</strong> The 1,979-row file was
        cleaned before splitting; global missing-value imputation and outlier filtering can
        produce leakage. A single test split, dataset bias, binary gender encoding and the
        absence of clinical validation limit real-world interpretation.</div>''')
    footer()


def wellness_studio() -> None:
    banner('🌿 Wellness studio · Explainable by design','Small habits. Clear suggestions.',
           'Explore general lifestyle ideas through transparent rules—without pretending an ML classifier can diagnose fitness or explain personal health.')
    section('💚 Explore the lifestyle prompts','This optional feature is separate from all seven models. Adjust the demo inputs to see which general suggestions appear.')
    with st.form('wellness_explore'):
        c1,c2=st.columns(2)
        with c1:
            sleep=st.number_input('Sleep hours per night',min_value=0.0,max_value=24.0,value=6.5,step=0.5)
            activity=st.number_input('Activity index (dataset 0–10)',min_value=0.0,max_value=10.0,value=2.0,step=0.5)
        with c2:
            nutrition=st.number_input('Nutrition quality (dataset 0–10)',min_value=0.0,max_value=10.0,value=4.0,step=0.5)
            smoke=st.radio('Smokes?', ['No','Yes'],horizontal=True)
        submitted=st.form_submit_button('💚 Show suggestions',type='primary',use_container_width=True)
    if submitted:
        st.session_state['wellness_values']={'sleep_hours':sleep,'activity_index':activity,
                                             'nutrition_quality':nutrition,'smokes':smoke}
    if 'wellness_values' in st.session_state:
        section('✨ Lifestyle inspiration', 'Educational habits to consider—not individualized medical instructions.')
        suggestions_html(st.session_state['wellness_values'])
    else:
        markup('''<div class="promo">✨ Press <strong>Show suggestions</strong> to explore
            exactly how the separate rule-based educational cards work.</div>''')
    section('🔍 Why we keep it separate')
    markup('''<div class="promo"><strong>The models classify the dataset label.</strong>
      The wellness studio only looks at sleep hours, the dataset’s activity and nutrition
      indices, and smoking status. This is transparent example logic, and is not an explanation
      of what features caused an ML prediction or a medically validated plan.</div>''')
    footer()


def predictor(slug: str) -> None:
    final=(slug=='final')
    actual=winner_slug() if final else slug
    info=MODEL_INFO[actual]
    record=evaluation_row(actual)
    label='🏆 CV-selected final model' if final else f'👤 Member model {MODEL_ORDER.index(actual)+1:02d}'
    heading='Final AI fitness predictor' if final else info['name']
    desc=(f"{info['name']} · Built by {info['member']}. {info['details']} "
          'Predictions demonstrate the assigned dataset’s is_fit label, not a personal health diagnosis.')
    banner(label,heading,desc)
    st.caption(f"📚 Mean 5-fold CV accuracy: {record['cv_accuracy_mean']:.2%}   ·   🎯 Held-out test accuracy: {record['test_accuracy']:.2%}   ·   👥 Model owner: {info['member']}")
    tabs=st.tabs(['✨ Single prediction','📂 Batch CSV prediction','📊 Model evaluation']+
                 (['🏁 Compare all seven'] if final else []))
    with tabs[0]:
        person_form(slug)
        show_person_result(slug)
    with tabs[1]:
        batch_tab(slug)
    with tabs[2]:
        model_evaluation(slug)
    if final:
        with tabs[3]:
            st.markdown('#### 🏆 Compare the same seven algorithms')
            st.caption('The winner is determined by mean cross-validation accuracy, never test-set accuracy.')
            table=evaluation_table()
            accuracy_chart(table)
            st.dataframe(table[['model','member','cv_accuracy_mean','test_accuracy','test_f1']],
                         use_container_width=True,hide_index=True)
            st.button('Open full model leaderboard ↗',key='final_to_comp',
                      on_click=navigate,args=('comparison',))
    footer()


def render_main() -> None:
    page_setup()
    selected=sidebar()
    if selected=='home': home()
    elif selected=='final': predictor('final')
    elif selected=='comparison': comparison()
    elif selected=='wellness': wellness_studio()
    else: predictor(selected)


def render_standalone(slug: str) -> None:
    """Retained compatibility with anyone importing the original UI helper."""
    if slug not in MODEL_ORDER+['final']:
        raise ValueError(f'Unknown model: {slug}')
    page_setup('FitnessAI Pro | '+str(slug))
    with st.sidebar:
        markup('<div class="brandname">FitnessAI <b>Pro</b></div>')
        st.caption('Individual model prediction view')
    predictor(slug)
