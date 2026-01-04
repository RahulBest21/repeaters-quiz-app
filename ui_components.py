import streamlit as st

# Defined locally to avoid import errors or circular dependencies with utils.py
def _force_day_mode():
    st.markdown("""
        <style>
            /* 1. Global Background & Text - Force White Theme */
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

            /* 4. Headers & Markdown */
            h1, h2, h3, h4, h5, h6, p, li, span, div {
                color: #000000 !important;
            }
            
            /* 5. Metrics */
            [data-testid="stMetricValue"] {
                color: #000000 !important;
            }
            [data-testid="stMetricLabel"] {
                color: #555555 !important;
            }
            
            /* 6. Tables/Dataframes */
            div[data-testid="stDataFrame"] *, div[data-testid="stDataEditor"] * {
                color: #000000 !important;
                background-color: #ffffff !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_header(title):
    """
    Renders the consistent header for the application.
    Injects the global CSS theme to ensure Day Mode is active on every page.
    """
    _force_day_mode()  # Apply theme directly from this file
    
    st.markdown(f"""
    <div style="background-color:#ffffff; padding:10px; border-bottom: 2px solid #f0f0f0; margin-bottom: 20px;">
        <h1 style="color:#000000; margin:0; font-size: 2rem;">{title}</h1>
    </div>
    """, unsafe_allow_html=True)

def render_palette(total_q, current_idx):
    st.markdown("#### Question Palette")
    cols = st.columns(4)
    q_status = st.session_state.get('q_status', {})
    
    for i in range(total_q):
        status = q_status.get(i, 'not_visited')
        color = "#e0e0e0" # Default grey
        text_color = "black"
        
        if i == current_idx:
            color = "#007bff" # Blue for current
            text_color = "white"
        elif status == 'answered':
            color = "#28a745" # Green
            text_color = "white"
        elif status == 'not_answered':
            color = "#dc3545" # Red
            text_color = "white"
            
        if cols[i % 4].button(str(i+1), key=f"q_nav_{i}", help=f"Go to Q{i+1}"):
            st.session_state['current_q_index'] = i
            st.rerun()
            
        # Styling hack for buttons isn't perfect in Streamlit, 
        # so we rely on the state update above.
        pass

def render_action_bar(current_idx, total_q, module_name):
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        if current_idx > 0:
            if st.button("⬅️ Previous"):
                st.session_state['current_q_index'] -= 1
                st.rerun()
                
    with c3:
        if current_idx < total_q - 1:
            if st.button("Next ➡️"):
                st.session_state['current_q_index'] += 1
                st.rerun()
