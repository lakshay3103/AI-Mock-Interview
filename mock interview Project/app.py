import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import json
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION & API KEY ---
load_dotenv()

# Secure Key Handling
try:
    if "GOOGLE_API_KEY" in st.secrets:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        API_KEY = "AIzaSyD2RboTJKzy7v7u2uzSCBB-AgBqvD6O6R8"# <--- PASTE KEY HERE FOR LOCAL RUN
except:
    API_KEY = "PASTE_YOUR_API_KEY_HERE"

# Stop if key is missing
if API_KEY == "PASTE_YOUR_API_KEY_HERE":
    st.error("⚠️ STOP: You need to paste your API Key in line 18!")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- 2. UI DESIGN (DARK THEME & ALIGNMENT) ---
st.set_page_config(page_title="AI Mock Interviewer", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    /* 1. Global Background (Dark Cyberpunk) */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* 2. Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111118;
        border-right: 1px solid #333;
    }
    
    /* 3. Cards (ATS & Features) */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* 4. Score Colors */
    .score-high { color: #00ff88; font-size: 32px; font-weight: 800; }
    .score-med { color: #ffcc00; font-size: 32px; font-weight: 800; }
    .score-low { color: #ff0055; font-size: 32px; font-weight: 800; }
    
    /* 5. Chat Styling - USER (Right Aligned) */
    .chat-user {
        background-color: #2b2b40;
        padding: 15px 20px;
        border-radius: 20px 20px 0 20px;
        margin-bottom: 10px;
        border: 1px solid #444;
        max-width: 70%;
        margin-left: auto; /* <--- Pushes to Right */
        text-align: right;
    }
    
    /* 6. Chat Styling - AI (Left Aligned) */
    .chat-ai {
        background: linear-gradient(145deg, rgba(255, 0, 204, 0.1) 0%, rgba(51, 51, 153, 0.1) 100%);
        padding: 15px 20px;
        border-radius: 20px 20px 20px 0;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 0, 204, 0.2);
        max-width: 70%;
        margin-right: auto; /* <--- Keeps on Left */
    }
    
    /* 7. Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ff00cc, #333399);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(255, 0, 204, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# --- 4. SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.title("🚀 Setup")
    st.caption("Upload your resume to get started")
    
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    jd_input = st.text_area("Paste Job Description", height=200, placeholder="Paste the JD here...")
    
    if st.button("Analyze & Start Interview", use_container_width=True):
        if resume_file and jd_input:
            with st.spinner("🔍 Scanning Resume against JD..."):
                # A. Read PDF
                reader = PdfReader(resume_file)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text()
                
                # B. ATS Logic
                analysis_prompt = f"""
                Act as an ATS (Applicant Tracking System) Expert.
                Resume: {resume_text}
                JD: {jd_input}
                
                Task: Compare the Resume to the JD.
                Output JSON ONLY:
                {{
                    "match_score": (integer 0-100),
                    "missing_keywords": ["skill1", "skill2"],
                    "profile_summary": "1 sentence summary of candidate fit"
                }}
                """
                
                try:
                    response = model.generate_content(analysis_prompt)
                    clean_json = response.text.replace("```json", "").replace("```", "")
                    st.session_state.analysis = json.loads(clean_json)
                    
                    # C. Start Interview (With "Stop" Logic)
                    system_prompt = f"""
                    You are a Senior Technical Interviewer. 
                    Resume: {resume_text}
                    JD: {jd_input}
                    Analysis: {st.session_state.analysis}
                    
                    Goal: Drill the candidate on their weak areas found in the analysis.
                    
                    Rules:
                    1. Be strictly professional but encouraging. 
                    2. Start with 1 question.
                    3. Keep digging deeper if the answer is vague.
                    4. IMPORTANT: If the candidate says "I'm done", "Stop", "Feedback", or asks to end the interview, STOP asking questions. Instead, provide a structured "Final Feedback" report on their answers.
                    """
                    
                    st.session_state.chat = model.start_chat(history=[
                        {"role": "user", "parts": [system_prompt]}
                    ])
                    
                    first_msg = st.session_state.chat.send_message("Start the interview.")
                    st.session_state.messages = [{"role": "ai", "content": first_msg.text}]
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
        else:
            st.warning("⚠️ Please upload both a Resume and a Job Description!")

# --- 5. MAIN DASHBOARD ---
st.title("🤖 AI Mock Interviewer")

# A. SHOW ATS ANALYSIS (Only if scan is done)
if st.session_state.analysis:
    data = st.session_state.analysis
    score = data["match_score"]
    
    if score >= 75:
        color_class = "score-high"
        status_msg = "Great Match! Ready to Ace it."
    elif score >= 50:
        color_class = "score-med"
        status_msg = "Good Fit. Focus on missing skills."
    else:
        color_class = "score-low"
        status_msg = "Low Match. Be prepared for tough questions."
    
    with st.expander("📊 Pre-Interview Analysis (Click to Hide)", expanded=True):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 14px; color: #aaa;">ATS Match Score</div>
                <div class="{color_class}">{score}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"**📝 Profile Summary:**\n{data['profile_summary']}")
            if data["missing_keywords"]:
                st.markdown(f"**⚠️ Missing Keywords:**")
                st.error(", ".join(data["missing_keywords"]))
        with col3:
             st.info(f"💡 **Strategy:** {status_msg}")

# B. SHOW CHAT OR HERO SECTION
if not st.session_state.messages:
    # --- HERO SECTION (This replaces the empty black screen) ---
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px;">
        <h1 style="font-size: 60px; background: -webkit-linear-gradient(#eee, #999); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Ready to Ace It? 🚀
        </h1>
        <p style="font-size: 20px; color: #888; margin-bottom: 30px;">
            Don't just practice. <b>Simulate.</b><br>
            Upload your resume to generate a personalized <span style="color: #00ff88;">ATS Score</span> and start the interview.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 Gemini 2.5 Brain</h3>
            <p style="color: #aaa; font-size: 14px;">Powered by Google's latest AI for human-like conversation.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📝 ATS Scanner</h3>
            <p style="color: #aaa; font-size: 14px;">Instant match score and keyword gap analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Adaptive Drill</h3>
            <p style="color: #aaa; font-size: 14px;">Questions get harder as you get answers right.</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # --- CHAT INTERFACE ---
    for msg in st.session_state.messages:
        css_class = "chat-user" if msg["role"] == "user" else "chat-ai"
        role_label = "YOU" if msg["role"] == "user" else "INTERVIEWER"
        st.markdown(f"""
        <div class="{css_class}">
            <b style="font-size: 12px; color: #888;">{role_label}</b><br>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)

    if user_input := st.chat_input("Type your answer here..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. AI Response
        if st.session_state.chat:
            with st.spinner("Interviewer is thinking..."):
                response = st.session_state.chat.send_message(user_input)
                st.session_state.messages.append({"role": "ai", "content": response.text})
                st.rerun()