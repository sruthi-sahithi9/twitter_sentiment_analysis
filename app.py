import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Set page config
st.set_page_config(page_title="Twitter Sentiment Demo", layout="centered", page_icon="🛍️")

# Injecting Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0d0e15 0%, #1a1c29 100%);
        color: #ffffff;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px !important;
        padding-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #a0a5b5;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 300;
    }
    div[data-baseweb="textarea"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    div[data-baseweb="textarea"]:focus-within {
        border: 1px solid rgba(0, 198, 255, 0.5) !important;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.15);
    }
    div[data-baseweb="textarea"] textarea {
        color: #ffffff !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1.1rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 198, 255, 0.5);
        color: white;
    }
    .result-card {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        animation: fadeIn 0.5s ease;
        margin-top: 30px;
    }
    .result-positive {
        background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(39, 174, 96, 0.2) 100%);
        border: 1px solid rgba(46, 204, 113, 0.3);
    }
    .result-negative {
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.1) 0%, rgba(192, 57, 43, 0.2) 100%);
        border: 1px solid rgba(231, 76, 60, 0.3);
    }
    .result-neutral {
        background: linear-gradient(135deg, rgba(241, 196, 15, 0.1) 0%, rgba(243, 156, 18, 0.2) 100%);
        border: 1px solid rgba(241, 196, 15, 0.3);
    }
    .result-icon {
        font-size: 4rem;
        margin-bottom: 10px;
    }
    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>Product Sentiment Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze customer feedback (Positive / Negative / Neutral).</div>", unsafe_allow_html=True)

analyzer = SentimentIntensityAnalyzer()

tweet = st.text_area("Enter customer review/tweet below:", height=150, placeholder="e.g., I absolutely love this product! It's amazing.")

if st.button("Analyze Sentiment"):
    if tweet.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            scores = analyzer.polarity_scores(tweet)
            compound_score = scores['compound']
            
            if compound_score >= 0.05:
                html_str = f"""
                <div class="result-card result-positive">
                    <div class="result-icon">😍</div>
                    <div class="result-title" style="color: #2ecc71;">Positive Feedback</div>
                    <div style="color: #a0a5b5;">This customer is happy! (Score: {compound_score:.2f})</div>
                </div>
                """
            elif compound_score <= -0.05:
                html_str = f"""
                <div class="result-card result-negative">
                    <div class="result-icon">😡</div>
                    <div class="result-title" style="color: #e74c3c;">Negative Feedback</div>
                    <div style="color: #a0a5b5;">This customer is unhappy. (Score: {compound_score:.2f})</div>
                </div>
                """
            else:
                html_str = f"""
                <div class="result-card result-neutral">
                    <div class="result-icon">😐</div>
                    <div class="result-title" style="color: #f1c40f;">Neutral Feedback</div>
                    <div style="color: #a0a5b5;">This customer is feeling neutral. (Score: {compound_score:.2f})</div>
                </div>
                """
            st.markdown(html_str, unsafe_allow_html=True)
