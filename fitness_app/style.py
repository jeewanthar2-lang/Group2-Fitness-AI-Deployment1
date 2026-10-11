
"""Visual styling for the seven-model Streamlit fitness showcase."""

GLOBAL_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

:root { --ink:#17233f; --muted:#697991; --purple:#6e4ef6; --cyan:#05aec7; --mint:#13aa8e; --line:#e6e9f5; }

html,body,[class*="css"] {font-family:'DM Sans',sans-serif;}

h1,h2,h3,h4{font-family:'Plus Jakarta Sans','DM Sans',sans-serif!important;letter-spacing:-.035em!important;color:var(--ink)}

[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 85% 5%, #edebff 0%,transparent 23%),radial-gradient(circle at 10% 35%,#e9f9fb 0%,transparent 26%),#f7f9fe;color:var(--ink)}

[data-testid="stHeader"]{background:transparent}

.main .block-container{max-width:1330px;padding-top:1.7rem;padding-bottom:4rem}

section[data-testid="stSidebar"]{background:linear-gradient(170deg,#171932 0%,#231f47 55%,#162a43 100%);border-right:1px solid #2f3565}

section[data-testid="stSidebar"] *{color:#ecedff}

section[data-testid="stSidebar"] .stRadio label[data-testid="stWidgetLabel"] p{color:#aab6d5!important}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label{background:#ffffff0b;padding:.59rem .75rem;border:1px solid transparent;border-radius:12px;transition:all .15s}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover{background:#ffffff16;border-color:#ffffff18}

section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked){background:linear-gradient(100deg,#7561f9bb,#268ad966);border-color:#9e98ff99}

section[data-testid="stSidebar"] hr{border-color:#ffffff20}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#dbe3fa}

.stButton>button[kind="primary"], .stFormSubmitButton>button[kind="primary"],.stDownloadButton>button[kind="primary"]{background:linear-gradient(105deg,#6852f3,#a351e4);border:none;color:white!important;border-radius:12px;font-weight:750;min-height:2.85rem;box-shadow:0 6px 22px #6c4af62b;transition:transform .18s ease,box-shadow .18s ease}

.stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{transform:translateY(-2px);box-shadow:0 9px 25px #6c4af648}

/* FIX: Bright white prediction button text */
[data-testid="stFormSubmitButton"] button,
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(105deg, #6852F3, #A351E4) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* FIX: Force inner button labels to be white */
[data-testid="stFormSubmitButton"] button *,
.stFormSubmitButton > button[kind="primary"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
}

/* FIX: Visible button text on hover */
[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(105deg, #5C42E7, #923DD5) !important;
    color: #FFFFFF !important;
}

.stButton>button[kind="secondary"]{background:white;border:1px solid #dedff1;border-radius:11px;color:#48446c;transition:all .18s}

.stButton>button[kind="secondary"]:hover{border-color:#7968f5;color:#6d50f6;background:#f5f2ff}

[data-testid="stMetric"]{background:#fff;border:1px solid #e9ebf5;border-radius:18px;padding:1rem 1.2rem;box-shadow:0 7px 30px #202d5909}

[data-testid="stMetric"] label{color:#63718d!important;font-weight:650}

[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#282b4a;font-weight:800}

[data-testid="stForm"]{background:white;border:1px solid #e9e8f5;border-radius:20px;padding:1.3rem;box-shadow:0 12px 35px #19204a0a}

[data-testid="stTabs"] button{font-weight:700;color:#57647b}

[data-testid="stTabs"] button[aria-selected="true"]{color:#664bf5}

[data-testid="stTabs"] [data-baseweb="tab-highlight"]{background:#7659f5}

[data-testid="stDataFrame"]{border:1px solid #e6eaf5;border-radius:13px;overflow:hidden}

[data-testid="stFileUploader"]{background:#fff;border-radius:14px;padding:10px;border:1px solid #ebedf7}

input,textarea {border-radius:10px!important}

[data-testid="stAlert"]{border-radius:13px}

/* Pure HTML sections */

.brandbox{display:flex;align-items:center;gap:11px;margin:6px 0 21px}

.brandicon{width:46px;height:46px;border-radius:15px;background:linear-gradient(135deg,#7370fa,#31b7dc);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px #706cf566;font-size:23px}

.brandname{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.18rem;font-weight:800;letter-spacing:-.04em;color:#fff}

.brandname b{color:#74e8ee}.brandsub{font-size:10px;letter-spacing:2px;color:#b1b5d8;margin-top:3px;font-weight:700}

.sidebar-cap{display:inline-flex;padding:8px 11px;border-radius:10px;background:#4b47826b;border:1px solid #ffffff19;color:#cfeaff;font-size:12px;font-weight:700}

.hero{position:relative;isolation:isolate;overflow:hidden;border-radius:26px;padding:42px 44px;background:linear-gradient(116deg,#232359 0%,#3c35a7 50%,#6c45b7 100%);box-shadow:0 18px 38px #252d6d24;color:white!important}

.hero:before{content:"";position:absolute;z-index:-1;right:-80px;top:-125px;width:450px;height:450px;background:radial-gradient(circle,#79ebf94b,transparent 65%);border-radius:100%}

.hero:after{content:"";position:absolute;z-index:-1;right:8%;bottom:-190px;width:330px;height:330px;background:radial-gradient(circle,#f082fb6c,transparent 65%);border-radius:100%}

.eyebrow{color:#9bebf4;font-size:12px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:13px}

.hero-title{font:800 clamp(29px,4vw,48px)/1.12 'Plus Jakarta Sans',sans-serif;letter-spacing:-.055em;color:#fff;margin:0 0 12px}

.hero-description{font-size:15px;line-height:1.85;max-width:660px;color:#dbe4ff;margin-bottom:24px}

.hero-chips{display:flex;flex-wrap:wrap;gap:9px}.hero-chip{padding:8px 12px;font-size:12px;font-weight:750;border-radius:99px;background:#ffffff20;border:1px solid #ffffff25;color:white}

.hero-icon{font-size:72px;position:absolute;right:8%;top:27%;filter:drop-shadow(0px 12px 15px #060d4488);transform:rotate(-15deg);opacity:.75}

.section-hd{display:flex;align-items:center;gap:10px;margin:30px 0 10px;font:800 23px 'Plus Jakarta Sans',sans-serif;color:#202a4d;letter-spacing:-.04em}

.section-sub{font-size:14px;line-height:1.7;color:#70819a;margin:0 0 18px}

.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:15px;margin:22px 0}

.kpi{background:white;border-radius:18px;border:1px solid #e7eaf5;padding:20px;box-shadow:0 8px 28px #1f255d08}

.kpi-icon{font-size:22px;margin-bottom:8px}.kpi-num{font:800 26px 'Plus Jakarta Sans',sans-serif;color:#27294e}.kpi-label{font-size:12px;font-weight:700;color:#708098;margin-top:6px}

.kpi.violet{border-top:4px solid #7454ed}.kpi.cyan{border-top:4px solid #24c2d4}.kpi.mint{border-top:4px solid #21c4a0}.kpi.amber{border-top:4px solid #fcab66}

.member-card{background:white;min-height:200px;border:1px solid #e8ebf4;border-radius:18px;padding:19px 19px 9px;margin-top:10px;box-shadow:0 10px 28px #26377109;position:relative;overflow:hidden}

.member-card:before{content:"";position:absolute;left:0;top:0;width:5px;height:100%;background:var(--accent,#6d54ec)}

.member-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}

.member-icon{background:color-mix(in srgb,var(--accent,#7357e8) 11%,white);width:43px;height:43px;border-radius:13px;display:grid;place-items:center;font-size:21px}

.member-num{background:#f3f4fa;color:#697891;padding:6px 10px;border-radius:99px;font-weight:800;font-size:11px}

.member-name{font-weight:800;color:#202647;font-size:15px;margin-bottom:4px}

.member-model{font-weight:700;color:var(--accent,#6957e8);font-size:12px;margin-bottom:7px}

.member-about{font-size:12px;color:#79859c;line-height:1.55;min-height:42px}

.member-stats{display:flex;gap:18px;border-top:1px solid #eef0f7;padding-top:10px;margin-top:14px}

.member-stats b{font-size:15px;color:#23264a}.member-stats span{display:block;font-size:10px;color:#9aa4b6;margin-top:3px}

.promo{background:linear-gradient(120deg,#edfffc,#edf2ff);border:1px solid #e1eaf5;padding:18px 22px;border-radius:18px;color:#44516f;font-size:14px;line-height:1.75}

.promo strong{color:#35316a}

.page-hero{background:linear-gradient(110deg,#26265b,#5344b4);color:white!important;border-radius:22px;padding:30px 32px;margin-bottom:18px;position:relative;overflow:hidden}

.page-hero:after{content:"";background:radial-gradient(circle,#b98afb80,transparent 70%);width:260px;height:260px;position:absolute;right:-38px;top:-90px}

.page-hero h1,.page-hero h2{position:relative;color:#fff!important;font:800 clamp(23px,3vw,33px) 'Plus Jakarta Sans',sans-serif;letter-spacing:-.045em;margin:2px 0 10px}

.page-hero p{position:relative;color:#e1e5ff;margin:0;max-width:760px;line-height:1.8;font-size:13px}

.page-hero .eyebrow{position:relative}

.result{border-radius:21px;padding:26px 28px;margin:18px 0 12px;display:flex;align-items:center;gap:25px;border:1px solid #d3eadd}

.result.fit{background:linear-gradient(112deg,#e9fff5,#eefdfb);border-color:#b9edd5}

.result.notfit{background:linear-gradient(112deg,#fff3e7,#fff9ef);border-color:#fbd9ba}

.result-icon{display:grid;place-items:center;min-width:62px;height:62px;border-radius:19px;background:white;font-size:35px}

.result-title{font:800 27px 'Plus Jakarta Sans',sans-serif;color:#115f50;margin:0 0 6px}.notfit .result-title{color:#ae5b29}

.result-sub{font-size:12px;line-height:1.8;color:#5d6b80}.result-class{font-size:10px;font-weight:850;letter-spacing:1.6px;color:#58717d;text-transform:uppercase;margin-bottom:7px}

.tip-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;margin:18px 0}

.tip-card{background:white;border:1px solid #e9ecf6;border-radius:17px;padding:19px 19px 17px;box-shadow:0 7px 23px #15265f08}

.tip-top{display:flex;align-items:center;gap:10px;margin-bottom:9px}.tip-icon{width:43px;height:43px;border-radius:12px;background:#f4efff;display:grid;place-items:center;font-size:22px}.tip-card.cyan .tip-icon{background:#e2f8fc}.tip-card.amber .tip-icon{background:#fff5e6}.tip-card.mint .tip-icon{background:#e4fbf2}

.tip-title{font-weight:800;color:#30314d;font-size:14px;line-height:1.4}

.tip-cat{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#8a90a6;font-weight:800;margin-top:3px}

.tip-desc{font-size:12px;line-height:1.75;color:#6f7c92}

.note{background:#fff;border-left:4px solid #9d8bec;border-radius:12px;padding:14px 17px;color:#66758b;font-size:12px;line-height:1.75;margin:12px 0 17px}

.note strong{color:#4937ae}

.footer{margin-top:33px;padding:22px 0;border-top:1px solid #dfe5f2;font-size:12px;line-height:1.7;color:#7f8aa1}

@media(max-width:950px){.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.hero-icon{display:none}.hero{padding:32px 28px}}

@media(max-width:650px){.main .block-container{padding-left:1rem;padding-right:1rem}.kpi-grid,.tip-grid{grid-template-columns:1fr}.hero{padding:28px 21px;border-radius:19px}.hero-title{font-size:29px}.page-hero{padding:24px 21px}.result{padding:18px;gap:12px}.result-icon{min-width:48px;height:48px;font-size:24px}.result-title{font-size:20px}.kpi{padding:15px}}

@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important}}

</style>
"""
