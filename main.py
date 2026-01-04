import streamlit as st
from styles import load_css
from utils import init_session_state
from modules.auth import render_auth
from modules.dashboard import render_dashboard
from modules.quiz_math import render_math_quiz, render_math_scorecard
from modules.quiz_gk import render_gk_quiz, render_gk_scorecard

# 1. Config
st.set_page_config(page_title="The Repeaters Official", page_icon="🔐", layout="wide")

# 2. Init State & CSS
init_session_state()
logo_html = load_css()

# 3. Routing Logic
if st.session_state['user'] is None:
    render_auth(logo_html)

else:
    # Authenticated Pages
    page = st.session_state['page']
    
    if page == 'dashboard':
        render_dashboard()
        
    elif page == 'quiz':
        if st.session_state['module'] == 'MATH':
            render_math_quiz()
        elif st.session_state['module'] == 'GK':
            render_gk_quiz()
            
    elif page == 'scorecard':
        if st.session_state['module'] == 'MATH':
            render_math_scorecard()
        elif st.session_state['module'] == 'GK':
            render_gk_scorecard()