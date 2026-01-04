import streamlit as st
import time

def _inject_css():
    """
    Injects internal CSS for styling and fixes the white screen/contrast issues
    by strictly enforcing text colors and backgrounds.
    """
    st.markdown("""
    <style>
        /* --- GLOBAL THEME RESET (Fixes White Screen/Contrast) --- */
        .stApp {
            background-color: #f8f9fa !important; /* Light grey background */
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Force text color to black/dark grey */
        h1, h2, h3, h4, h5, h6, p, li, span, div, label, .stMarkdown {
            color: #212529 !important;
        }
        
        /* --- CUSTOM COMPONENT STYLING --- */
        
        /* 1. Header Card */
        .test-header {
            background-color: #ffffff;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-bottom: 3px solid #4a90e2; /* Accent border */
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .test-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #2c3e50 !important;
        }
        .timer-box {
            background-color: #fff3cd;
            color: #856404 !important;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            border: 1px solid #ffeeba;
            font-family: monospace;
            font-size: 1.2rem;
        }

        /* 2. Palette / Sidebar Area */
        .legend-box {
            width: 12px;
            height: 12px;
            border-radius: 2px;
            border: 1px solid #ccc;
            margin-right: 4px;
        }
        
        /* 3. Action Bar (Bottom) */
        .action-bar {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            margin-top: 20px;
            border-top: 1px solid #eee;
        }

        /* 4. Streamlit Button Enhancements */
        .stButton button {
            border-radius: 6px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        /* Primary Button (Save & Next) */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #28a745 !important;
            border-color: #28a745 !important;
            color: white !important;
            box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #218838 !important;
        }
        /* Secondary Buttons */
        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: #ffffff !important;
            border: 1px solid #ced4da !important;
            color: #495057 !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            border-color: #4a90e2 !important;
            color: #4a90e2 !important;
            background-color: #f8f9fa !important;
        }
        
        /* 5. Inputs & Dataframes */
        .stTextInput input, .stNumberInput input {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ced4da !important;
            border-radius: 5px;
        }
        div[data-testid="stDataFrame"] {
            border: 1px solid #eee;
            border-radius: 5px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(module_name):
    _inject_css() # Apply styles immediately
    start_ts = st.session_state.get('start_time', time.time())
    st.markdown(f"""
    <div class='test-header'>
        <div class='test-title'>CGL 2025 T-2 Live Mock - {module_name}</div>
        <div class='timer-box'>⏳ <span id='timer_val'>00:00</span></div>
    </div>
    <script>
    try {{
        setInterval(function(){{
            var e = Math.floor((Date.now()/1000)-{start_ts});
            var m = Math.floor(e/60); var s = e%60;
            if(s<10) s='0'+s;
            if(m<10) m='0'+m;
            // Try standard access
            var el = document.getElementById('timer_val');
            // Try parent access (Streamlit specific)
            if(!el && window.parent) {{
                el = window.parent.document.getElementById('timer_val');
            }}
            if(el) el.innerHTML = m+':'+s;
        }}, 1000);
    }} catch(e) {{ console.log("Timer error:", e); }}
    </script>
    """, unsafe_allow_html=True)

def render_palette(total_q, current_idx):
    st.markdown("#### Section Analysis")
    st.markdown("""
    <div style='margin-bottom:15px; background: white; padding: 10px; border-radius: 8px; border: 1px solid #eee;'>
        <div style='display:flex; justify-content:space-between; font-size: 0.85em; color: #555;'>
            <div><span class='legend-box' style='background:#5cb85c; display:inline-block;'></span> Ans</div>
            <div><span class='legend-box' style='background:#d9534f; display:inline-block;'></span> No</div>
            <div><span class='legend-box' style='background:#5bc0de; display:inline-block;'></span> Rev</div>
            <div><span class='legend-box' style='background:#eee; display:inline-block;'></span> New</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Grid CSS for buttons
    cols = 4
    rows = (total_q + cols - 1) // cols
    
    for r in range(rows):
        c = st.columns(cols)
        for i in range(cols):
            q_idx = r * cols + i
            if q_idx < total_q:
                s = st.session_state['q_status'].get(q_idx, 'not_visited')
                
                # Determine visual label and help text
                if s == 'answered': emoji = "✅"
                elif s == 'not_answered': emoji = "🟥"
                elif s == 'review': emoji = "🟣"
                else: emoji = "⬜"
                
                label = f"{q_idx+1} {emoji}"
                if q_idx == current_idx: label = f"▶ {q_idx+1}"
                
                # Use secondary style for all, let emoji do the talking, highlight current
                if c[i].button(label, key=f"nav_{q_idx}", use_container_width=True, type="primary" if q_idx == current_idx else "secondary"):
                    st.session_state['current_q_index'] = q_idx
                    st.rerun()

def render_action_bar(current_idx, total_q, module_type):
    # Container for action bar
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    b1, b2, b3, b4 = st.columns([1, 1, 1.2, 0.8])
    
    with b1:
        if st.button("⬅ Previous", use_container_width=True):
            if current_idx > 0: 
                st.session_state['current_q_index'] -= 1
                st.rerun()
            
    with b2:
        if st.button("🟣 Review", use_container_width=True, help="Mark for Review"):
            st.session_state['q_status'][current_idx] = 'review'
            if current_idx < total_q - 1: st.session_state['current_q_index'] += 1
            st.rerun()
        
    with b3:
        if st.button("✅ Save & Next", type="primary", use_container_width=True):
            # Check if actually answered
            is_answered = False
            if module_type == 'GK':
                if st.session_state['answers_store'].get(current_idx): is_answered = True
            elif module_type == 'MATH':
                 is_answered = True

            st.session_state['q_status'][current_idx] = 'answered' if is_answered else 'not_answered'
            
            if current_idx < total_q - 1: st.session_state['current_q_index'] += 1
            st.rerun()
        
    with b4:
        if st.button("🗑 Clear", use_container_width=True):
            if module_type == 'GK': st.session_state['answers_store'][current_idx] = None
            st.session_state['q_status'][current_idx] = 'not_answered'
            st.rerun()
