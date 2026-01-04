import streamlit as st
import time
import pandas as pd
import plotly.express as px # Added for leaderboard
from database import get_data, save_to_sheet
from utils import get_ist, reset_module_state
from ui_components import render_header, render_palette, render_action_bar

def setup_gk():
    with st.sidebar:
        st.button("Back", on_click=reset_module_state)
    
    st.subheader("Select Quiz Parameters")
    df = get_data("GK_Questions")
    
    if not df.empty:
        sub = st.selectbox("Subject", df['Subject'].unique())
        chap = st.selectbox("Chapter", df[df['Subject']==sub]['Chapter'].unique())
        quiz = st.selectbox("Quiz", df[(df['Subject']==sub) & (df['Chapter']==chap)]['Quiz_Name'].unique())
        
        if st.button("Start Test", type="primary"):
            q_data = df[(df['Subject']==sub) & (df['Chapter']==chap) & (df['Quiz_Name']==quiz)].to_dict('records')
            st.session_state['gk_q'] = q_data
            st.session_state['gk_id'] = f"{sub} | {chap} | {quiz}"
            st.session_state['start_time'] = time.time()
            st.session_state['total_q'] = len(q_data)
            st.session_state['q_status'] = {i: 'not_visited' for i in range(len(q_data))}
            st.session_state['gk_setup'] = True
            st.rerun()
    else: 
        st.warning("No Data Available")
        if st.button("Back"): reset_module_state(); st.rerun()

def render_gk_quiz():
    if not st.session_state.get('gk_setup', False):
        setup_gk()
        return

    main_col, right_col = st.columns([0.75, 0.25], gap="medium")
    
    with right_col:
        render_palette(st.session_state['total_q'], st.session_state['current_q_index'])
        st.markdown("---")
        if st.button("🔥 SUBMIT TEST", type="primary", use_container_width=True):
            st.session_state['end_time'] = time.time()
            st.session_state['page'] = 'scorecard'
            st.rerun()
            
    with main_col:
        # This function injects the JS Timer you referenced
        render_header("GK")
        
        # BRANDING: Anil Yadav
        st.markdown("""
        <div style='background-color: #f9f9f9; padding: 10px; border-radius: 5px; border-left: 4px solid #5cb85c; margin-bottom: 20px;'>
            <small style='color: #666; font-style: italic; font-weight: 600;'>
            Questions framed and solutions by anil yadav
            </small>
        </div>
        """, unsafe_allow_html=True)

        current_idx = st.session_state['current_q_index']
        render_action_bar(current_idx, st.session_state['total_q'], "GK")
        
        if st.session_state['q_status'].get(current_idx) == 'not_visited':
            st.session_state['q_status'][current_idx] = 'not_answered'

        st.subheader(f"Question No. {current_idx + 1}")
        
        q_data = st.session_state['gk_q'][current_idx]
        st.write(f"**{q_data['Question']}**")
        
        opts = [str(q_data[o]) for o in ['OptionA','OptionB','OptionC','OptionD']]
        existing = st.session_state['answers_store'].get(current_idx)
        
        sel = st.radio("Select Option:", opts, index=opts.index(existing) if existing in opts else None, key=f"radio_{current_idx}")
        
        if sel: 
            st.session_state['answers_store'][current_idx] = sel

def render_gk_scorecard():
    st.balloons()
    
    st.markdown("""
        <div style='text-align:center; margin-bottom: 20px;'>
            <h1 style='color:#333;'>Scorecard by Nitin Sharma</h1>
            <p style='color:#666;'>General Knowledge Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # FIX: Safe duration calculation to prevent KeyError
    # This ensures it doesn't crash if 'end_time' or 'start_time' are missing
    end_t = st.session_state.get('end_time', time.time())
    start_t = st.session_state.get('start_time', end_t)
    duration = round(end_t - start_t, 2)
    
    score = 0
    # FIX: Safety check for gk_q existence
    if 'gk_q' not in st.session_state:
        st.error("No quiz data found.")
        if st.button("Back to Dashboard"):
            reset_module_state()
            st.session_state['page'] = 'dashboard'
            st.rerun()
        return

    total = len(st.session_state['gk_q'])
    sols = []
    
    for i, q in enumerate(st.session_state['gk_q']):
        u_ans = st.session_state['answers_store'].get(i)
        c_ans = str(q['Answer'])
        if str(u_ans) == c_ans: score += 1
        else: sols.append(f"**Q{i+1}: {q['Question']}**<br>You: {u_ans if u_ans else 'Skipped'} | Correct: {c_ans}<br><i>{q.get('Solution','')}</i>")
    
    # Save first
    if 'saved' not in st.session_state:
        ist_date, ist_time = get_ist()
        save_to_sheet("Scores", [ist_date, ist_time, st.session_state['name'], st.session_state['mobile'], "-", "GK", "-", "-", "-", "-", score, duration, st.session_state['user'], st.session_state['gk_id']])
        st.session_state['saved'] = True

    c1, c2 = st.columns(2)
    with c1: st.metric("Score", f"{score}/{total}")
    with c2: st.metric("Time", f"{duration}s")
    
    st.markdown("---")
    
    # --- TABS: Solutions & Leaderboard ---
    t1, t2 = st.tabs(["💡 Detailed Solutions", "🏆 Leaderboard & Analysis"])
    
    with t1:
        if not sols: st.success("🎉 Perfect Score!")
        for s in sols: st.markdown(f"<div class='solution-box'>{s}</div>", unsafe_allow_html=True)
    
    with t2:
        # Fetch fresh data to show live leaderboard
        df_scores = get_data("Scores")
        if not df_scores.empty and len(df_scores.columns) >= 14:
            # Filter for current GK Topic (Quiz ID)
            current_quiz_id = st.session_state['gk_id']
            # Using 'Topic' column (13th index usually, but matched by name in dashboard fix)
            # Assuming 'Topic' exists as per dashboard fix
            if 'Topic' in df_scores.columns:
                 quiz_scores = df_scores[df_scores['Topic'] == current_quiz_id].copy()
            else:
                 # Fallback if column naming varies
                 quiz_scores = df_scores[df_scores['Quiz_ID'] == current_quiz_id].copy() if 'Quiz_ID' in df_scores.columns else df_scores
                 
            quiz_scores['Total'] = pd.to_numeric(quiz_scores['Total'], errors='coerce').fillna(0)
            
            # 1. Percentile Logic
            user_score = score
            topper_score = quiz_scores['Total'].max()
            total_participants = len(quiz_scores)
            
            if total_participants > 0:
                participants_below = len(quiz_scores[quiz_scores['Total'] < user_score])
                percentile = (participants_below / total_participants) * 100
            else:
                percentile = 100.0
                
            c_a, c_b = st.columns(2)
            with c_a:
                st.metric("Your Percentile", f"{percentile:.1f}%")
                st.metric("Topper Score", int(topper_score) if not pd.isna(topper_score) else 0)
            
            with c_b:
                # 2. Comparison Graph
                fig = px.histogram(quiz_scores, x="Total", nbins=15, title="Score Distribution", color_discrete_sequence=['#5bc0de'])
                fig.add_vline(x=user_score, line_width=3, line_dash="dash", line_color="green", annotation_text="You")
                fig.add_vline(x=topper_score, line_width=3, line_dash="dash", line_color="red", annotation_text="Topper")
                st.plotly_chart(fig, use_container_width=True)
                
            # 3. Leaderboard Table
            st.subheader("Top Performers")
            leaderboard = quiz_scores[['Name', 'Total', 'Duration']].sort_values(by='Total', ascending=False).head(10).reset_index(drop=True)
            st.dataframe(leaderboard, use_container_width=True)
        else:
            st.info("Leaderboard data updating...")

    st.markdown("---")
    if st.button("Back to Dashboard"):
        reset_module_state()
        st.session_state['page'] = 'dashboard'
        st.rerun()
