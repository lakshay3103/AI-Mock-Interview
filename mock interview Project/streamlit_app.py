import streamlit as st
from typing import Optional
import time

# Page configuration
st.set_page_config(
    page_title="AI Mock Interviewer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto"
)

# Vibrant, modern CSS with collapsible sidebar support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Vibrant color palette */
    :root {
        --bg-dark: #0a0a0f;
        --bg-card: #12121a;
        --bg-elevated: #1a1a25;
        --bg-input: #1e1e2a;
        --text-primary: #ffffff;
        --text-secondary: #a0a0b0;
        --text-muted: #6b6b7b;
        --accent-pink: #ff3d8a;
        --accent-blue: #3d7dff;
        --accent-cyan: #00d4ff;
        --accent-purple: #a855f7;
        --gradient-main: linear-gradient(135deg, #ff3d8a 0%, #a855f7 50%, #3d7dff 100%);
        --gradient-button: linear-gradient(135deg, #ff3d8a 0%, #ff6b6b 100%);
        --gradient-card: linear-gradient(145deg, #1a1a25 0%, #12121a 100%);
        --border-subtle: rgba(255, 255, 255, 0.08);
        --border-accent: rgba(255, 61, 138, 0.3);
        --glow-pink: 0 0 30px rgba(255, 61, 138, 0.3);
        --glow-blue: 0 0 30px rgba(61, 125, 255, 0.3);
    }
    
    /* Base app styling */
    .stApp {
        background: var(--bg-dark);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp > header {
        background: transparent !important;
    }
    
    /* Sidebar - Collapsible & Mobile Optimized */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #12121a 100%);
        border-right: 1px solid var(--border-subtle);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: -21rem;
    }
    
    /* Collapse button styling */
    button[kind="header"] {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
    }
    
    /* Headers with gradient */
    h1 {
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }
    
    /* Main hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 1rem;
        position: relative;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255, 61, 138, 0.15) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    
    .hero-title {
        font-size: clamp(2rem, 5vw, 3.5rem) !important;
        font-weight: 800 !important;
        background: var(--gradient-main);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 1rem;
        margin-bottom: 0;
        position: relative;
        z-index: 1;
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(26, 26, 37, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: var(--border-accent);
        box-shadow: var(--glow-pink);
    }
    
    /* Sidebar sections */
    .sidebar-card {
        background: var(--gradient-card);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .sidebar-card:hover {
        border-color: rgba(255, 61, 138, 0.2);
    }
    
    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text-primary);
    }
    
    .sidebar-icon {
        width: 32px;
        height: 32px;
        background: var(--gradient-button);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--bg-input);
        border: 2px dashed rgba(255, 61, 138, 0.3);
        border-radius: 12px;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-pink);
        background: rgba(255, 61, 138, 0.05);
    }
    
    [data-testid="stFileUploader"] label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: var(--text-muted) !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
    
    /* Text area */
    .stTextArea textarea {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
        resize: none;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--accent-pink) !important;
        box-shadow: 0 0 0 3px rgba(255, 61, 138, 0.1) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Primary button - Vibrant gradient */
    .stButton > button {
        background: var(--gradient-button) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(255, 61, 138, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 30px rgba(255, 61, 138, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) scale(0.98) !important;
    }
    
    /* Chat container */
    .chat-wrapper {
        background: rgba(18, 18, 26, 0.5);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-subtle);
        border-radius: 24px;
        padding: 1.5rem;
        min-height: 350px;
        max-height: 450px;
        overflow-y: auto;
    }
    
    /* Message bubbles */
    .msg-row {
        display: flex;
        gap: 0.875rem;
        margin-bottom: 1.25rem;
        animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .msg-avatar {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    
    .avatar-ai {
        background: var(--gradient-main);
    }
    
    .avatar-user {
        background: linear-gradient(135deg, #3d7dff 0%, #00d4ff 100%);
    }
    
    .msg-bubble {
        flex: 1;
        padding: 1rem 1.25rem;
        border-radius: 16px;
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.65;
    }
    
    .bubble-ai {
        background: linear-gradient(145deg, rgba(255, 61, 138, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
        border: 1px solid rgba(255, 61, 138, 0.15);
        border-left: 3px solid var(--accent-pink);
    }
    
    .bubble-user {
        background: var(--bg-elevated);
        border: 1px solid var(--border-subtle);
    }
    
    /* Chat input */
    .stChatInput {
        position: relative;
    }
    
    .stChatInput > div {
        background: var(--bg-input) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 16px !important;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: var(--accent-pink) !important;
        box-shadow: 0 0 0 3px rgba(255, 61, 138, 0.1) !important;
    }
    
    .stChatInput input {
        color: var(--text-primary) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stChatInput button {
        background: var(--gradient-button) !important;
        border-radius: 10px !important;
    }
    
    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 2.5rem 1.5rem;
        position: relative;
    }
    
    .welcome-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .welcome-emoji {
        font-size: 3.5rem;
        margin-bottom: 1.25rem;
        position: relative;
        z-index: 1;
    }
    
    .welcome-heading {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    
    .welcome-text {
        color: var(--text-secondary);
        font-size: 1rem;
        max-width: 450px;
        margin: 0 auto 2rem;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        max-width: 600px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    .feature-card {
        background: rgba(26, 26, 37, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: left;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(255, 61, 138, 0.2);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        color: var(--text-muted);
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* Status badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-active {
        background: rgba(255, 61, 138, 0.15);
        color: var(--accent-pink);
        border: 1px solid rgba(255, 61, 138, 0.3);
    }
    
    .badge-waiting {
        background: rgba(61, 125, 255, 0.15);
        color: var(--accent-blue);
        border: 1px solid rgba(61, 125, 255, 0.3);
    }
    
    /* Tips box */
    .tip-card {
        background: linear-gradient(145deg, rgba(0, 212, 255, 0.08) 0%, rgba(61, 125, 255, 0.05) 100%);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    
    .tip-card p {
        color: var(--accent-cyan);
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Success/Error overrides */
    .stSuccess {
        background: rgba(16, 185, 129, 0.12) !important;
        border: 1px solid rgba(16, 185, 129, 0.25) !important;
        border-radius: 12px !important;
        color: #10b981 !important;
    }
    
    .stError {
        background: rgba(255, 61, 138, 0.12) !important;
        border: 1px solid rgba(255, 61, 138, 0.25) !important;
        border-radius: 12px !important;
        color: var(--accent-pink) !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid var(--border-subtle);
        margin: 1.25rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-elevated);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 61, 138, 0.3);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] > div:first-child {
            padding: 1rem 0.75rem;
        }
        
        .hero-section {
            padding: 1.5rem 0.75rem;
        }
        
        .chat-wrapper {
            padding: 1rem;
            border-radius: 16px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .glass-card {
            padding: 1rem;
            border-radius: 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'resume_uploaded' not in st.session_state:
    st.session_state.resume_uploaded = False

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.25rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.08);">
        <div class="sidebar-icon">
            <span style="filter: grayscale(100%) brightness(2);">&#128193;</span>
        </div>
        <div>
            <h3 style="margin: 0; font-size: 1rem; color: #fff; font-weight: 700;">Your Documents</h3>
            <p style="margin: 0; font-size: 0.8rem; color: #6b6b7b;">Upload to begin</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Resume Upload
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-title">
            <span style="font-size: 1.1rem;">&#128196;</span>
            <span>Resume (PDF)</span>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=['pdf'],
        help="Max 200MB",
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file:
        st.session_state.resume_uploaded = True
        st.success(f"Uploaded: {uploaded_file.name}")
    
    # Job Description
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-title">
            <span style="font-size: 1.1rem;">&#128221;</span>
            <span>Job Description</span>
        </div>
    """, unsafe_allow_html=True)
    
    job_description = st.text_area(
        "Paste JD here",
        height=180,
        placeholder="Paste the job description to personalize your interview...",
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Start Button
    st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
    start_button = st.button("Start Interview", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if start_button:
        if uploaded_file and job_description:
            st.session_state.interview_started = True
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Hello! I'm your AI interviewer today. I've reviewed your resume and the job description. Let's start with an icebreaker: **Tell me about yourself and what excites you about this opportunity?**"
            })
            st.rerun()
        else:
            st.error("Upload resume and paste job description first.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Tip
    st.markdown("""
    <div class="tip-card">
        <p><strong>Pro tip:</strong> Practice speaking your answers aloud before typing for realistic interview prep.</p>
    </div>
    """, unsafe_allow_html=True)

# Main Area
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">AI Mock Interviewer</h1>
    <p class="hero-subtitle">powered by Gemini 2.5 Flash</p>
</div>
""", unsafe_allow_html=True)

# Chat or Welcome
if st.session_state.interview_started and st.session_state.messages:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"""
            <div class="msg-row">
                <div class="msg-avatar avatar-ai">&#129302;</div>
                <div class="msg-bubble bubble-ai">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row">
                <div class="msg-avatar avatar-user">&#128100;</div>
                <div class="msg-bubble bubble-user">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your answer...")
    
    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Simulated AI responses (replace with Gemini API)
        ai_responses = [
            "Great response! Your background sounds impressive. Next question: **What's your greatest professional achievement and why does it matter to you?**",
            "I appreciate that insight! Let's dive deeper: **Describe a challenging project you led. What obstacles did you face and how did you overcome them?**",
            "Excellent problem-solving skills! Now: **How do you stay current with industry trends and continue developing your skills?**",
            "That shows great initiative! Here's a behavioral question: **Tell me about a time you disagreed with a colleague. How did you handle it?**",
            "Wonderful! Final question: **Where do you see your career in 5 years, and how does this role align with that vision?**"
        ]
        
        response_index = min(len([m for m in st.session_state.messages if m["role"] == "user"]) - 1, len(ai_responses) - 1)
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_responses[response_index]
        })
        
        st.rerun()

else:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-emoji">&#127919;</div>
        <h2 class="welcome-heading">Ready to nail your interview?</h2>
        <p class="welcome-text">
            Upload your resume and paste the job description in the sidebar to start a personalized AI-powered mock interview.
        </p>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">&#10024;</div>
                <div class="feature-title">Tailored Questions</div>
                <div class="feature-desc">AI analyzes your resume for relevant questions</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128172;</div>
                <div class="feature-title">Real-time Feedback</div>
                <div class="feature-desc">Get instant insights on your responses</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#128170;</div>
                <div class="feature-title">Build Confidence</div>
                <div class="feature-desc">Practice makes perfect interviews</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">&#127942;</div>
                <div class="feature-title">Behavioral Prep</div>
                <div class="feature-desc">Master common interview scenarios</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Status Footer
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.interview_started:
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem;">
            <span class="badge badge-active">&#9679; Interview Active</span>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.resume_uploaded:
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem;">
            <span class="badge badge-waiting">&#9679; Add Job Description</span>
        </div>
        """, unsafe_allow_html=True)
