import streamlit as st
import tempfile, os
from styles import apply_styles
from engine import process_video_ai, generate_natural_audio

st.set_page_config(page_title="AuraSync", layout="wide")
apply_styles()

st.title("AuraSync")

# --- 1. SETUP SECTION (This is the only manual card) ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: mode = st.radio("Mode", ["Visually Impaired", "Hearing Impaired"])
with c2: depth = st.select_slider("Depth", ["Instant", "Low", "Medium", "High"], "Low")
with c3: video_file = st.file_uploader("Video", type=['mp4'])

if video_file and st.button("🚀 Analyze"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.getvalue())
        path = tmp.name
    with st.spinner("Analyzing..."):
        res, thoughts = process_video_ai(path, mode, depth)
        st.session_state.res = res
        st.session_state.thoughts = thoughts
        st.session_state.active_mode = mode
        if mode == "Visually Impaired":
            st.session_state.audio = generate_natural_audio(res)
    os.remove(path)
st.markdown("</div>", unsafe_allow_html=True)

# --- 2. THE RESULTS AREA (Scorched Earth Edition) ---
if "res" in st.session_state and st.session_state.res:
    col_left, col_right = st.columns([1, 1])

    if st.session_state.active_mode == "Visually Impaired":
        with col_left:
            # We use native border=True to replace the card class
            with st.container(border=True):
                st.subheader("🔊 Audio Description")
                st.audio(st.session_state.audio)
                st.video(video_file)
        with col_right:
            if st.session_state.thoughts and len(st.session_state.thoughts) > 50:
                with st.container(border=True):
                    st.subheader("🧠 AI Thinking Trace")
                    st.info(st.session_state.thoughts)

    else:  # HEARING IMPAIRED
        with col_left:
            with st.container(border=True):
                st.subheader("📽️ Video")
                st.video(video_file)
            if st.session_state.thoughts and len(st.session_state.thoughts) > 50:
                with st.container(border=True):
                    st.subheader("🧠 AI Thinking Trace")
                    st.info(st.session_state.thoughts)
        with col_right:
            with st.container(border=True):
                st.subheader("📝 Dynamic Script")
                st.write(st.session_state.res)

st.markdown("<div class='footer'>Powered by Gemini 3 Flash • AuraSync • 2026</div>", unsafe_allow_html=True)