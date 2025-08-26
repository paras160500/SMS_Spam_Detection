import streamlit as st 
import pickle 
import string 
import nltk 
from nltk.stem.porter import PorterStemmer 
from nltk.corpus import stopwords
import time

# Set page config for better UI
st.set_page_config(
    page_title="🛡️ Spam Detector", 
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #667eea40; }
        to { text-shadow: 0 0 30px #764ba240; }
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-spam {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
        animation: bounceIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 20px 0;
    }
    
    .result-safe {
        background: linear-gradient(135deg, #26de81, #20bf6b);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 8px 32px rgba(38, 222, 129, 0.3);
        animation: bounceIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin: 20px 0;
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .feature-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        animation: slideIn 1s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .pulse-button {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .confidence-bar {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 10px;
        border-radius: 5px;
        animation: fillBar 1.5s ease-in-out;
        margin: 10px 0;
    }
    
    @keyframes fillBar {
        from { width: 0%; }
        to { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

# Load models
try:
    cv = pickle.load(open("vectorizor.pkl", "rb"))
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("🚨 Model files not found! Please ensure vectorizor.pkl and model.pkl are in the correct directory.")
    st.stop()

# Header with animation
st.markdown('<h1 class="main-header">🛡️ AI Spam Detective</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🔍 Advanced Message Analysis • 🤖 AI-Powered • ⚡ Real-time Detection</p>', unsafe_allow_html=True)

# Feature boxes
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>🚀 Instant</h3>
        <p>Get results in milliseconds</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🎯 Accurate</h3>
        <p>90%+ detection accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>🔒 Secure</h3>
        <p>Your data stays private</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sample messages data
spam_samples = [
    "URGENT! You have won $1000! Click here now to claim your prize: bit.ly/claim123",
    "FREE Msg: Your mobile number has been selected to receive a £350 reward! Reply YES now!",
    "WINNER!! As a valued customer you have been selected to receive a £900 prize reward! Call now!",
    "Your account has been suspended. Verify your identity immediately by clicking: www.fake-bank.com",
    "Congratulations! You've won £1,000,000 in the UK National Lottery! Claim your prize now!",
    "FLASH SALE! 90% off designer handbags! Limited time only. Shop now at www.fake-deals.com",
    "LOAN APPROVED! Get $5000 cash today with no credit check required. Apply now!",
    "FINAL NOTICE: Your lottery winnings of $50,000 are waiting. Contact us immediately!",
    "Action required: Your email will be deleted unless you confirm your password now!",
    "FREE iPhone 14! You've been selected! Click here to claim: www.freephone-offer.com"
]

normal_samples = [
    "Hey, can you pick up some milk on your way home? Thanks!",
    "Meeting moved to 3 PM tomorrow. See you in conference room B.",
    "Happy birthday! Hope you have a wonderful day.",
    "Your Amazon order has been delivered to your doorstep.",
    "Reminder: Doctor appointment at 2 PM on Friday.",
    "Thanks for dinner last night. Had a great time!",
    "The weather is great today. Perfect for a walk in the park.",
    "Can you help me with the project tomorrow? Let me know.",
    "Your flight is on time. Gate B12. Boarding starts at 5:30 PM.",
    "Movie night at my place this Saturday. Are you free?",
    "Your package will arrive between 2-4 PM today.",
    "Great presentation today! The client loved our proposal."
]

# Initialize random counters if not exists
if 'spam_counter' not in st.session_state:
    st.session_state.spam_counter = 0
if 'normal_counter' not in st.session_state:
    st.session_state.normal_counter = 0

# Sample messages for testing
st.markdown("#### 💡 Try These Sample Messages:")
sample_col1, sample_col2, sample_col3 = st.columns(3)

with sample_col1:
    if st.button("📱 Random Spam Sample", help="Click for a random spam message"):
        import random
        st.session_state.sample_text = random.choice(spam_samples)
        st.session_state.spam_counter += 1

with sample_col2:
    if st.button("✅ Random Normal Sample", help="Click for a random normal message"):
        import random
        st.session_state.sample_text = random.choice(normal_samples)
        st.session_state.normal_counter += 1

with sample_col3:
    if st.button("🔄 Clear Sample", help="Clear sample text"):
        if 'sample_text' in st.session_state:
            del st.session_state.sample_text

# Input section
st.markdown("### 📝 Enter Your Message")

# Get the current sample text or empty string
current_text = st.session_state.get('sample_text', '')

input_sms = st.text_area(
    "",
    value=current_text,
    placeholder="Type or paste your email/SMS message here...",
    height=100,
    help="Enter any text message to check if it's spam or legitimate",
    key="message_input"
)

# Show info if sample was loaded
if 'sample_text' in st.session_state and current_text:
    st.info("📝 Sample text loaded! You can edit it above or analyze it as is.")

# Your original transform function (keeping logic same)
@st.cache_data
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    ps = PorterStemmer()
    stop_word_list = stopwords.words('english')
    for i in text:
        if i.isalnum():
            if i not in stop_word_list and i not in string.punctuation: 
                i = ps.stem(i)
                y.append(i)
    return " ".join(y)

# Predict button with animation
predict_button = st.button(
    "🔍 Analyze Message", 
    help="Click to analyze the message for spam detection",
    use_container_width=True
)

if predict_button and input_sms:
    # Loading animation
    with st.spinner("🔄 Analyzing message..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        # Your original logic
        transform_message = transform_text(input_sms)
        vector = cv.transform([transform_message])
        result = model.predict(vector)[0]
        probability = model.predict_proba(vector)[0]
        
        # Clear progress bar
        progress_bar.empty()
    
    # Results with animations
    st.markdown("### 📊 Analysis Results")
    
    if result == 1:
        confidence = probability[1] * 100
        st.markdown(f"""
        <div class="result-spam">
            🚨 SPAM DETECTED! 🚨<br>
            <small>Confidence: {confidence:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.error("⚠️ This message appears to be spam. Please be cautious!")
        
        # Warning indicators
        st.markdown("#### 🚩 Spam Indicators Found:")
        spam_indicators = []
        if any(word in input_sms.lower() for word in ['free', 'win', 'winner', 'prize', 'cash']):
            spam_indicators.append("💰 Contains promotional language")
        if any(word in input_sms.upper() for word in ['URGENT', 'WINNER', 'FREE']):
            spam_indicators.append("📢 Uses attention-grabbing CAPS")
        if 'http' in input_sms.lower() or 'bit.ly' in input_sms.lower():
            spam_indicators.append("🔗 Contains suspicious links")
        if '$' in input_sms or '£' in input_sms:
            spam_indicators.append("💵 Mentions money/prizes")
            
        for indicator in spam_indicators:
            st.write(f"• {indicator}")
            
    else:
        confidence = probability[0] * 100
        st.markdown(f"""
        <div class="result-safe">
            ✅ LEGITIMATE MESSAGE ✅<br>
            <small>Confidence: {confidence:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("🛡️ This message appears to be legitimate and safe!")
    
    # Confidence visualization
    st.markdown("#### 📈 Confidence Level")
    confidence_value = max(probability[0], probability[1]) * 100
    st.progress(confidence_value / 100)
    st.write(f"Model Confidence: {confidence_value:.1f}%")
    
    # Additional insights
    with st.expander("🔬 Technical Details"):
        st.write(f"**Processed Text:** {transform_message}")
        st.write(f"**Spam Probability:** {probability[1]:.4f}")
        st.write(f"**Ham Probability:** {probability[0]:.4f}")
        st.write(f"**Vector Shape:** {vector.shape}")

elif predict_button and not input_sms:
    st.warning("⚠️ Please enter a message to analyze!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🔒 Built with Advanced ML • 🚀 Powered by Streamlit • 🛡️ Protecting Your Inbox</p>
</div>
""", unsafe_allow_html=True)