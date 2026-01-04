import streamlit as st
from datetime import datetime
import pytz

def get_ist():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

def reset_module_state():
    keys_to_reset = ['worksheet', 'start_time', 'end_time', 'q_status', 'total_q', 'current_q_index', 'answers_store', 'saved']
    for k in keys_to_reset:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state['current_q_index'] = 0
    st.session_state['answers_store'] = {}

def init_session_state():
    """Initialize session state variables if they don't exist."""
    defaults = {
        'page': 'login',
        'authenticated': False,
        'name': '',
        'mobile': '',
        'user': '',
        'worksheet': None,
        'q_status': {},
        'current_q_index': 0,
        'answers_store': {}
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# --- GLOBAL THEME FIX ---
def inject_custom_css():
    st.markdown("""
        <style>
            /* 1. Global Background & Text */
            .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            
            /* 2. Sidebar */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
                border-right: 1px solid #e0e0e0;
            }
            [data-testid="stSidebar"] * {
                color: #000000 !important;
            }

            /* 3. Inputs (Text, Number, Date) */
            input, textarea, select, .stTextInput > div > div > input, .stNumberInput > div > div > input {
                color: #000000 !important;
                background-color: #ffffff !important;
                border: 1px solid #cccccc !important;
            }
            /* Input Labels */
            label, .stTextInput label, .stNumberInput label {
                color: #222222 !important;
                font-weight: 600 !important;
            }

            /* 4. DataFrames & Tables */
            div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
                background-color: #ffffff !important;
                border: 1px solid #e0e0e0;
            }
            div[data-testid="stDataFrame"] *, div[data-testid="stDataEditor"] * {
                color: #000000 !important;
                background-color: #ffffff !important;
            }

            /* 5. Headers & Markdown */
            h1, h2, h3, h4, h5, h6, p, li, span {
                color: #000000 !important;
            }
            
            /* 6. Metrics */
            [data-testid="stMetricValue"] {
                color: #000000 !important;
            }
            [data-testid="stMetricLabel"] {
                color: #555555 !important;
            }

            /* 7. Buttons */
            button[kind="primary"] {
                background-color: #ff4b4b !important;
                color: white !important;
                border: none;
            }
            button[kind="secondary"] {
                background-color: white !important;
                color: #000000 !important;
                border: 1px solid #cccccc !important;
            }
            
            /* 8. Solution Box for Quiz */
            .solution-box {
                background-color: #f8f9fa;
                color: #000000 !important;
                border-left: 5px solid #007bff;
                padding: 10px;
                margin-bottom: 8px;
                border-radius: 4px;
                font-family: monospace;
            }
            .solution-header {
                font-weight: bold;
                color: #0056b3 !important;
            }
        </style>
    """, unsafe_allow_html=True)
