import streamlit as st
import time

def render_header(module_name):
    start_ts = st.session_state.get('start_time', time.time())
    st.markdown(f"""
    <div class='test-header'>
        <div class='test-title'>CGL 2025 T-2 Live Mock - {module_name}</div>
        <div class='timer-box'>⏳ <span id='timer_val'>00:00</span></div>
    </div>
    <script>
    setInterval(function(){{
        var e = Math.floor((Date.now()/1000)-{start_ts});
        var m = Math.floor(e/60); var s = e%60;
        if(s<10) s='0'+s;
        if(m<10) m='0'+m;
        var el = window.parent.document.getElementById('timer_val');
        if(el) el.innerHTML = m+':'+s;
    }}, 1000);
    </script>
    """, unsafe_allow_html=True)

def render_palette(total_q, current_idx):
    st.markdown("**Section Analysis**")
    st.markdown("""<div style='margin-bottom:10px; font-size: 0.8em;'>
        <span class='legend-box' style='background:#5cb85c; display:inline-block;'></span> Answered
        <span class='legend-box' style='background:#d9534f; display:inline-block;'></span> Not Ans
        <span class='legend-box' style='background:#fff; display:inline-block;'></span> Unvisited
        <span class='legend-box' style='background:#5bc0de; display:inline-block;'></span> Review
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    
    # Custom Grid CSS for buttons
    cols = 4
    rows = (total_q + cols - 1) // cols
    
    for r in range(rows):
        c = st.columns(cols)
        for i in range(cols):
            q_idx = r * cols + i
            if q_idx < total_q:
                s = st.session_state['q_status'].get(q_idx, 'not_visited')
                
                # Determine visual label
                if s == 'answered': emoji = "✅"
                elif s == 'not_answered': emoji = "🟥"
                elif s == 'review': emoji = "🟣"
                else: emoji = "⬜"
                
                label = f"{q_idx+1} {emoji}"
                if q_idx == current_idx: label = f"▶ {q_idx+1}"
                
                if c[i].button(label, key=f"nav_{q_idx}", use_container_width=True):
                    st.session_state['current_q_index'] = q_idx
                    st.rerun()

def render_action_bar(current_idx, total_q, module_type):
    st.markdown("<div class='action-bar'>", unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    
    if b1.button("⬅ Previous"):
        if current_idx > 0: 
            st.session_state['current_q_index'] -= 1
            st.rerun()
            
    if b2.button("Mark Review"):
        st.session_state['q_status'][current_idx] = 'review'
        if current_idx < total_q - 1: st.session_state['current_q_index'] += 1
        st.rerun()
        
    if b3.button("Save & Next", type="primary"):
        # Check if actually answered
        is_answered = False
        if module_type == 'GK':
            if st.session_state['answers_store'].get(current_idx): is_answered = True
        elif module_type == 'MATH':
             # Math is considered answered if viewed/edited (simplification for DataFrame editing)
             # Ideally check if DF is empty, but for speed we assume 'Saved' means committed
             is_answered = True

        st.session_state['q_status'][current_idx] = 'answered' if is_answered else 'not_answered'
        
        if current_idx < total_q - 1: st.session_state['current_q_index'] += 1
        st.rerun()
        
    if b4.button("Clear"):
        if module_type == 'GK': st.session_state['answers_store'][current_idx] = None
        st.session_state['q_status'][current_idx] = 'not_answered'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
