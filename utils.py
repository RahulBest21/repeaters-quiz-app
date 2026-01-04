import hashlib
import random
import string
import pytz
from datetime import datetime
import streamlit as st

def hash_pass(p): 
    return hashlib.sha256(str(p).encode()).hexdigest()

def gen_key(): 
    return "KEY-" + ''.join(random.choices(string.digits, k=6))

def gen_captcha(): 
    a,b = random.randint(1,10), random.randint(1,10)
    return f"{a} + {b}", a+b

def get_ist(): 
    n = datetime.now(pytz.timezone('Asia/Kolkata'))
    return n.strftime("%Y-%m-%d"), n.strftime("%H:%M:%S")

def init_session_state():
    defaults = {
        'user': None, 
        'page': 'login', 
        'module': None,
        'current_q_index': 0,
        'q_status': {},
        'answers_store': {},
        'captcha_q': None,
        'captcha_a': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
            
    if st.session_state['captcha_q'] is None:
        q, a = gen_captcha()
        st.session_state.update({'captcha_q':q, 'captcha_a':a})

def reset_module_state():
    """Clears all test-specific state for a clean start"""
    keys_to_clear = ['worksheet', 'gk_q', 'gk_id', 'gk_setup', 'answers_store', 'q_status', 
                     'current_q_index', 'start_time', 'end_time', 'total_q', 'saved']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['module'] = None
    st.session_state['page'] = 'dashboard'