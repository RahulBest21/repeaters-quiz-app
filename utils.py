import streamlit as st
from utils import inject_custom_css

def render_header(title):
    """
    Renders the consistent header for the application.
    Injects the global CSS theme to ensure Day Mode is active on every page.
    """
    inject_custom_css()  # <--- FIX: Applies theme to every page using this header
    
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
        # This is a visual indicator using markdown if buttons fail to style
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
