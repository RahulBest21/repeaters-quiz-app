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
    # FIX 1: Return a tuple (Question String, Answer Int) to match auth.py unpacking logic
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
        # FIX 2: Set user to None (not '') so main.py correctly detects unauthenticated state
        'user': None, 
        'worksheet': None,
        'q_status': {},
        'current_q_index': 0,
        'answers_store': {}
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # FIX 3: Initialize captcha variables to prevent KeyError in auth.py on first load
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
    """Placeholder for backward compatibility."""
    pass
