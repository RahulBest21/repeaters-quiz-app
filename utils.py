import streamlit as st
from datetime import datetime
import pytz
import hashlib
import random
import string

# --- CORE UTILITIES ---

def get_ist():
    """Returns current date and time in IST."""
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

def reset_module_state():
    """Resets the state for quizzes/worksheets."""
    keys_to_reset = ['worksheet', 'start_time', 'end_time', 'q_status', 'total_q', 'current_q_index', 'answers_store', 'saved']
    for k in keys_to_reset:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state['current_q_index'] = 0
    st.session_state['answers_store'] = {}

def gen_captcha():
    """Generates a simple math captcha (Question, Answer)."""
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    return f"{a} + {b}", a + b

def init_session_state():
    """Initialize base session state variables if they don't exist."""
    defaults = {
        'page': 'login',
        'authenticated': False,
        'name': '',
        'mobile': '',
        'user': None, 
        'worksheet': None,
        'q_status': {},
        'current_q_index': 0,
        'answers_store': {}
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    if 'captcha_q' not in st.session_state:
        q, a = gen_captcha()
        st.session_state['captcha_q'] = q
        st.session_state['captcha_a'] = a

def hash_pass(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(str(password).encode()).hexdigest()

def gen_key():
    """Generates a random session key."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def inject_custom_css():
    """Injects professional CSS for a clean, light-themed UI."""
    st.markdown("""
        <style>
        /* Force Light Theme Background & Text */
        [data-testid="stAppViewContainer"] {
            background-color: #f8f9fa;
        }
        [data-testid="stHeader"] {
            background-color: #f8f9fa;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e9ecef;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6, .stMarkdown, p, label {
            color: #212529 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1 {
            color: #1a1a1a !important;
            font-weight: 700;
        }
        
        /* Buttons - Professional Blue */
        .stButton > button {
            background-color: #0d6efd;
            color: white !important;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: background-color 0.2s;
        }
        .stButton > button:hover {
            background-color: #0b5ed7;
            border-color: #0a58ca;
        }
        .stButton > button:focus {
            box-shadow: 0 0 0 0.25rem rgba(49, 132, 253, 0.5);
            color: white !important;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #212529;
            border: 1px solid #ced4da;
            border-radius: 4px;
        }
        
        /* Dataframes / Tables */
        [data-testid="stDataFrame"] {
            border: 1px solid #dee2e6;
            border-radius: 4px;
            background-color: white;
        }
        
        /* Success/Info Messages */
        .stAlert {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
        }
        </style>
    """, unsafe_allow_html=True)
