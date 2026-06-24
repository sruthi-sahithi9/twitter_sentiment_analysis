import streamlit as st
import pickle
import re

# Set page config
st.set_page_config(page_title="Twitter Sentiment Demo", layout="centered", page_icon="🐦")

# Injecting Custom CSS
st.markdown("""
<style>
    /* Premium aesthetics for Streamlit */
    
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0d0e15 0%, #1a1c29 100%);
        color: #ffffff;
        font-family: 'Inter', 'Roboto', sans-serif;
    }
    
    /* Title styling */
    h1 {
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #3498db, #9b59b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px !important;
        padding-bottom: 10px;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #a0a5b5;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* Glassmorphism container for text area */
    div[data-baseweb="textarea"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    div[data-baseweb="textarea"]:focus-within {
        border: 1px solid rgba(52, 152, 219, 0.5) !important;
        box-shadow: 0 0 20px rgba(52, 152, 219, 0.15);
    }
    div[data-baseweb="textarea"] textarea {
        color: #ffffff !important;
    }
    
    /* Button styling */
    div.stButton > button {
        background: linear-gradient(90deg, #3498db 0%, #9b59b6 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1.1rem;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        display: block;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(52, 152, 219, 0.5);
        color: white;
    }
    
    /* Result card */
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

# Application UI
st.markdown("<h1>Twitter Sentiment Live Demo</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze the emotional tone of any tweet instantly.</div>", unsafe_allow_html=True)

# Load Models
@st.cache_resource
def load_models():
    try:
        model = pickle.load(open("svm_model.pkl", "rb"))
        vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
        return model, vectorizer
    except FileNotFoundError:
        st.error("Model files not found. Please train the model first.")
        return None, None

model, vectorizer = load_models()

def clean_tweet_fn(tweet_text):
    # Remove user tags
    tweet_text = re.sub(r"@[\\w]*", "", tweet_text)
    # Remove special characters
    tweet_text = re.sub(r"[^a-zA-Z#]", " ", tweet_text)
    # Remove short words
    cleaned = " ".join([w for w in str(tweet_text).split() if len(w) > 3])
    return cleaned

tweet = st.text_area("Enter your tweet below:", height=150, placeholder="What's happening?")

if st.button("Analyze Sentiment"):
    if tweet.strip() == "":
        st.warning("Please enter a tweet to analyze.")
    elif model is not None and vectorizer is not None:
        with st.spinner("Analyzing..."):
            cleaned = clean_tweet_fn(tweet)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            
            if prediction == 0:
                html_str = """
                <div class="result-card result-positive">
                    <div class="result-icon">✨</div>
                    <div class="result-title" style="color: #2ecc71;">Normal Tweet</div>
                    <div style="color: #a0a5b5;">This tweet appears to be normal / non-toxic.</div>
                </div>
                """
            else:
                html_str = """
                <div class="result-card result-negative">
                    <div class="result-icon">⚠️</div>
                    <div class="result-title" style="color: #e74c3c;">Toxic / Negative Tweet</div>
                    <div style="color: #a0a5b5;">This tweet contains toxic, racist, or sexist language.</div>
                </div>
                """
            st.markdown(html_str, unsafe_allow_html=True)
