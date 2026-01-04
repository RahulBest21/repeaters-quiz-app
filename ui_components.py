import streamlit as st
import time

def _inject_css():
    """
    Injects internal CSS for styling. 
    Includes a session state check to prevent redundant re-rendering.
    """
    if "css_injected" in st.session_state:
        return
        
    st.markdown("""
    <style>
        /* --- GLOBAL THEME RESET --- */
        [data-testid="stAppViewContainer"] {
            background-color: #f8f9fa !important;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0); /* Transparent header */
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e9ecef;
        }
        
        /* Typography & Contrast Safety */
        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            color: #212529;
        }
        h1, h2, h3, h4, h5, h6, .stMarkdown, p, div, span, label {
            color: #212529 !important;
        }

        /* --- COMPONENT STYLING --- */
        
        /* 1. Modern Header Card */
        .test-header {
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border-top: 5px solid #4a90e2; /* Blue accent top */
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 10px;
        }
        .test-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #343a40 !important;
            letter-spacing: -0.5px;
        }
        
        /* Timer Group */
        .timer-group {
            display: flex;
            gap: 10px;
        }

        .timer-badge {
            background: #fff3cd;
            color: #856404 !important;
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            font-weight: 700;
            font-family: 'Roboto Mono', monospace;
            border: 1px solid #ffeeba;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }
        
        .clock-badge {
            background: #e2e3e5;
            color: #383d41 !important;
            padding: 0.4rem 1.2rem;
            border-radius: 50px;
            font-weight: 700;
            font-family: 'Roboto Mono', monospace;
            border: 1px solid #d6d8db;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }

        /* 2. Palette Container */
        .palette-container {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        .legend-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f3f5;
        }
        .legend-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }

        /* 3. Button Refinements */
        .stButton button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease-in-out;
        }
        
        /* Navigation/Grid Buttons (Secondary) */
        div[data-testid="stButton"] button[kind="secondary"] {
            background-color: #ffffff !important;
            border: 1px solid #dee2e6 !important;
            color: #495057 !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            border-color: #4a90e2 !important;
            color: #4a90e2 !important;
            background-color: #f8f9fa !important;
            transform: translateY(-1px);
        }

        /* Primary Actions (Save/Next) */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #28a745 0%, #218838 100%) !important;
            color: white !important;
            box-shadow: 0 4px 6px rgba(40, 167, 69, 0.25) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            box-shadow: 0 6px 10px rgba(40, 167, 69, 0.35) !important;
            transform: translateY(-1px);
        }

        /* 4. Input Fields */
        .stTextInput input, .stNumberInput input {
            border: 1px solid #ced4da;
            border-radius: 8px;
            padding: 0.5rem 0.75rem;
            background: white !important;
            color: #212529 !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #4a90e2;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)
    st.session_state['css_injected'] = True

def render_header(module_name):
    _inject_css() # Apply styles robustly
    start_ts = st.session_state.get('start_time', time.time())
    
    # HTML Header
    header_html = f"""
    <div class='test-header'>
        <div class='test-title'>CGL 2025 Live Mock • {module_name}</div>
        <div class='timer-group'>
            <div class='clock-badge' title='Current Time'>
                <span>🕒</span> <span id='clock_val'>--:--:--</span>
            </div>
            <div class='timer-badge' title='Time Elapsed'>
                <span>⏳</span> <span id='timer_val'>00:00</span>
            </div>
        </div>
    </div>
    """
    
    # FIX: Use .replace() for JS injection. 
    # This prevents Python f-strings from trying to parse the {{ }} in the JS code
    # and causing the "}" error to appear on screen.
    js_logic = """
    <script>
    function updateTimers() {
        // 1. Update Elapsed Timer
        var now = Math.floor(Date.now() / 1000);
        var start = START_TIMESTAMP;
        var diff = now - start;
        
        var m = Math.floor(diff / 60);
        var s = diff % 60;
        
        if(m < 10) m = '0' + m;
        if(s < 10) s = '0' + s;
        
        var timerString = m + ':' + s;
        
        // 2. Update Clock
        var date = new Date();
        var h_c = date.getHours();
        var m_c = date.getMinutes();
        var s_c = date.getSeconds();
        var ampm = h_c >= 12 ? 'PM' : 'AM';
        h_c = h_c % 12;
        h_c = h_c ? h_c : 12; // the hour '0' should be '12'
        if(m_c < 10) m_c = '0' + m_c;
        if(s_c < 10) s_c = '0' + s_c;
        
        var clockString = h_c + ':' + m_c + ':' + s_c + ' ' + ampm;

        // Apply to elements (Handle Streamlit iframe nesting)
        var timerEl = document.getElementById('timer_val');
        var clockEl = document.getElementById('clock_val');
        
        if(timerEl) {
            timerEl.innerHTML = timerString;
            clockEl.innerHTML = clockString;
        } else if (window.parent) {
            try {
                var parentTimer = window.parent.document.getElementById('timer_val');
                var parentClock = window.parent.document.getElementById('clock_val');
                if(parentTimer) parentTimer.innerHTML = timerString;
                if(parentClock) parentClock.innerHTML = clockString;
            } catch(e) {}
        }
    }
    
    // Clear any existing intervals to prevent duplicates if re-running
    if (window.myTimerInterval) clearInterval(window.myTimerInterval);
    window.myTimerInterval = setInterval(updateTimers, 1000);
    
    // Run immediately once
    updateTimers();
    </script>
    """.replace("START_TIMESTAMP", str(start_ts))

    st.markdown(header_html + js_logic, unsafe_allow_html=True)

def render_palette(total_q, current_idx):
    # Palette Container
    st.markdown("""
    <div class='palette-container'>
        <div class='legend-row'>
            <div><span class='legend-dot' style='background:#28a745;'></span>Ans</div>
            <div><span class='legend-dot' style='background:#dc3545;'></span>No</div>
            <div><span class='legend-dot' style='background:#6f42c1;'></span>Rev</div>
            <div><span class='legend-dot' style='background:#dee2e6;'></span>New</div>
        </div>
        <div style='font-size:0.9rem; font-weight:600; color:#495057; margin-bottom:10px;'>Question Grid</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom Grid logic
    cols = 4
    rows = (total_q + cols - 1) // cols
    
    for r in range(rows):
        c = st.columns(cols)
        for i in range(cols):
            q_idx = r * cols + i
            if q_idx < total_q:
                s = st.session_state['q_status'].get(q_idx, 'not_visited')
                
                # Visual Indicator logic
                if s == 'answered': emoji = "✅"
                elif s == 'not_answered': emoji = "🟥"
                elif s == 'review': emoji = "🟣"
                else: emoji = "⬜"
                
                label = f"{q_idx+1} {emoji}"
                if q_idx == current_idx: label = f"▶ {q_idx+1}"
                
                # Render Button
                if c[i].button(label, key=f"nav_{q_idx}", use_container_width=True, type="primary" if q_idx == current_idx else "secondary"):
                    st.session_state['current_q_index'] = q_idx
                    st.rerun()

def render_action_bar(current_idx, total_q, module_type):
    # Spacer
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Action Buttons Layout
    b1, b2, b3, b4 = st.columns([1, 1, 1.3, 0.7])
    
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
            # Logic to check if answered
            is_answered = False
            if module_type == 'GK':
                if st.session_state['answers_store'].get(current_idx): is_answered = True
            elif module_type == 'MATH':
                 is_answered = True # Math is always considered visited/answered if viewed due to auto-save nature of data editor
                 # Note: Ideally, you could check if the dataframe in answers_store is non-empty/modified here if required.

            st.session_state['q_status'][current_idx] = 'answered' if is_answered else 'not_answered'
            
            if current_idx < total_q - 1: st.session_state['current_q_index'] += 1
            st.rerun()
        
    with b4:
        if st.button("🗑 Clear", use_container_width=True):
            if module_type == 'GK': st.session_state['answers_store'][current_idx] = None
            st.session_state['q_status'][current_idx] = 'not_answered'
            st.rerun()
