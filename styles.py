import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Import a clean, modern font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

        /* Global Background and Text */
        html, body, [class*="css"] { 
            font-family: 'Outfit', sans-serif; 
            background-color: #0F0F1A; 
            color: #E0E0FF; 
        }

        /* The Main Header Gradient */
        h1 {
            background: -webkit-linear-gradient(#FF4DAD, #FF8552);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        /* Cards */
        .card { 
            background: #161625; 
            padding: 24px; 
            border-radius: 18px; 
            border: 1px solid #2A2A40; 
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: transform 0.2s ease-in-out;
        }

        /* Input Field Styling */
        .stTextArea textarea {
            background-color: #1A1A2E !important;
            color: #00FFCC !important;
            border: 1px solid #303050 !important;
            border-radius: 12px !important;
            font-family: 'Courier New', Courier, monospace;
        }

        /* The 'Cool' Button */
        .stButton>button { 
            background: linear-gradient(90deg, #FF4DAD 0%, #FF8552 100%); 
            color: white; 
            border: none; 
            border-radius: 12px; 
            height: 3.5em; 
            font-weight: 600; 
            width: 100%;
            transition: 0.3s; 
            box-shadow: 0 4px 15px rgba(255, 77, 173, 0.3);
        }
        .stButton>button:hover { 
            transform: scale(1.02); 
            box-shadow: 0 6px 20px rgba(255, 77, 173, 0.5); 
        }

        /* AI Thinking Trace Box Style */
        .stInfo {
            background-color: #1A1A2E !important;
            border-left: 5px solid #FF4DAD !important;
            color: #E0E0FF !important;
        }

        /* Footer Alignment */
        .footer { 
            text-align: center; 
            font-size: 0.85em; 
            color: #606080; 
            margin-top: 60px;
            padding-bottom: 20px;
            letter-spacing: 1px;
        }

        /* Slider Color Fix */
        .stSlider [data-baseweb="slider"] {
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)