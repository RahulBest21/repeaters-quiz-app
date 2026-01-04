import streamlit as st
import pandas as pd
import numpy as np
import time
from utils import save_to_sheet, get_ist, reset_module_state
from database import get_data
# CHANGED: Removed 'modules.' prefix
from ui_components import render_header, render_palette, render_action_bar

def init_math_worksheet():
    if st.session_state.get('worksheet') is not None: return

    def rnd(l,h,c): return np.random.choice(np.arange(l,h), size=c, replace=False)
    rows_a, cols_a = rnd(21,99,5), rnd(10,99,5)
    
    ws = {
        'headers': {'r': rows_a, 'c': cols_a},
        'questions': [
            {'id': 0, 'type': 'df', 'title': 'Table Practice (16-19)', 'data': pd.DataFrame(None, index=rnd(11,99,3), columns=[16,17,18,19]), 'key': 'prac'},
            {'id': 1, 'type': 'df', 'title': 'Hard Grid Multiplication', 'data': pd.DataFrame(None, index=rnd(11,99,3), columns=rnd(11,99,3)), 'key': 'mgrid'},
            {'id': 2, 'type': 'df', 'title': 'Division Practice', 'data': pd.DataFrame(None, index=rnd(50,99,3), columns=rnd(10,49,3)), 'key': 'div'},
            {'id': 3, 'type': 'df', 'title': 'Successive Percentage', 'data': pd.DataFrame(np.random.randint(1,51,(6,3)), columns=['First','Second','Third'], index=range(1,7)), 'key': 'succ'},
            {'id': 4, 'type': 'df', 'title': 'Addition Speed', 'data': pd.DataFrame(None, index=[str(x) for x in rows_a]+["Total"], columns=[str(x) for x in cols_a]+["Total"]), 'key': 'add'},
            {'id': 5, 'type': 'df', 'title': 'Subtraction Speed', 'data': pd.DataFrame(None, index=rnd(100,999,5), columns=rnd(100,500,5)), 'key': 'sub'}
        ]
    }
    if 'Increment % (Value)' not in ws['questions'][3]['data'].columns:
         ws['questions'][3]['data']['Increment % (Value)'] = None
         ws['questions'][3]['data']['Decrement % (Value)'] = None
    
    st.session_state['worksheet'] = ws
    st.session_state['total_q'] = 6
    st.session_state['start_time'] = time.time()
    st.session_state['q_status'] = {i: 'not_visited' for i in range(6)}

def grade_math(user_df, op, label, h=None):
    score, total = 0, 0
    solutions_text = []
    
    if user_df is None: return 0, 0, []

    for r in user_df.index:
        for c in user_df.columns:
            if op=='succ' and 'crement' not in c: continue
            total += 1
            correct = 0
            try:
                if op in ['mult','df'] and label=='Table Practice (16-19)': correct = float(r)*float(c)
                elif label=='Hard Grid Multiplication': correct = float(r)*float(c)
                elif label=='Division Practice': correct = round(float(r)/float(c), 2)
                elif label=='Subtraction Speed': correct = abs(float(r)-float(c))
                elif label=='Addition Speed':
                    ri, ci = list(user_df.index).index(r), list(user_df.columns).index(c); rv, cv = h['r'], h['c']
                    if r!='Total' and c!='Total': correct = rv[ri]+cv[ci]
                    elif r=='Total' and c=='Total': correct = sum([x+y for x in rv for y in cv])
                    elif r=='Total': correct = sum([x+cv[ci] for x in rv])
                    else: correct = sum([rv[ri]+y for y in cv])
                elif label=='Successive Percentage':
                    p = [float(user_df.loc[r, k]) for k in ['First','Second','Third']]
                    is_inc = 'Incr' in c; factor = 1
                    for x in p: factor *= (1 + x/100) if is_inc else (1 - x/100)
                    correct = round(100*factor, 2)
                
                val = str(user_df.loc[r,c]).strip()
                if val and val != "None" and val != "nan" and abs(float(val) - correct) < 0.1: 
                    score += 1
                else: 
                    solutions_text.append(f"<b>{label} [{r}, {c}]</b>: You: {val} | Ans: {correct}")
            except: pass
    return score, total, solutions_text

def render_math_quiz():
    init_math_worksheet()
    
    main_col, right_col = st.columns([0.75, 0.25], gap="medium")
    
    with right_col:
        render_palette(st.session_state['total_q'], st.session_state['current_q_index'])
        st.markdown("---")
        if st.button("🔥 SUBMIT TEST", type="primary", use_container_width=True):
            st.session_state['end_time'] = time.time()
            st.session_state['page'] = 'scorecard'
            st.rerun()

    with main_col:
        render_header("MATH")
        # BRANDING: RahulBest
        st.markdown("<h3 style='text-align: left; color: #444; border-left: 4px solid #f0ad4e; padding-left: 10px; margin-bottom: 20px;'>Maths by RahulBest</h3>", unsafe_allow_html=True)
        
        current_idx = st.session_state['current_q_index']
        render_action_bar(current_idx, st.session_state['total_q'], "MATH")
        
        if st.session_state['q_status'].get(current_idx) == 'not_visited':
            st.session_state['q_status'][current_idx] = 'not_answered'

        st.subheader(f"Question No. {current_idx + 1}")
        
        q_obj = st.session_state['worksheet']['questions'][current_idx]
        st.info(f"Topic: {q_obj['title']}")
        
        d_key = f"data_{current_idx}"
        if d_key not in st.session_state['answers_store']: 
            st.session_state['answers_store'][d_key] = q_obj['data']
        
        col_cfg = {c: st.column_config.NumberColumn(required=False) for c in q_obj['data'].columns}
        if q_obj['key'] == 'succ': 
            col_cfg = {
                "First": st.column_config.NumberColumn(disabled=True), 
                "Second": st.column_config.NumberColumn(disabled=True), 
                "Third": st.column_config.NumberColumn(disabled=True), 
                "Increment % (Value)": st.column_config.NumberColumn(required=False), 
                "Decrement % (Value)": st.column_config.NumberColumn(required=False)
            }
        
        edited = st.data_editor(st.session_state['answers_store'][d_key], key=f"editor_{current_idx}", use_container_width=True, column_config=col_cfg, height=400)
        st.session_state['answers_store'][d_key] = edited

def render_math_scorecard():
    st.balloons()
    
    # BRANDING: Nitin Sharma
    st.markdown("""
        <div style='text-align:center; margin-bottom: 20px;'>
            <h1 style='color:#333;'>Scorecard by Nitin Sharma</h1>
            <p style='color:#666;'>Detailed Math Analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    ws = st.session_state['worksheet']
    duration = round(st.session_state['end_time'] - st.session_state['start_time'], 2)
    
    s_total, t_total = 0, 0
    all_sols = []
    
    for i, q in enumerate(ws['questions']):
        df_res = st.session_state['answers_store'].get(f"data_{i}", q['data'])
        op_code = 'div' if 'Division' in q['title'] else 'succ' if 'Percentage' in q['title'] else 'add' if 'Addition' in q['title'] else 'sub' if 'Subtraction' in q['title'] else 'mult'
        s, t, sol = grade_math(df_res, op_code, q['title'], ws['headers'])
        s_total+=s; t_total+=t; all_sols.extend(sol)

    c1, c2 = st.columns(2)
    with c1: st.metric("Total Score", f"{s_total}/{t_total}")
    with c2: st.metric("Time Taken", f"{duration} sec")
    
    st.subheader("Detailed Solutions")
    if not all_sols: st.success("🎉 Perfect Score!")
    for l in all_sols: st.markdown(f"<div class='solution-box'>{l}</div>", unsafe_allow_html=True)
    
    if 'saved' not in st.session_state:
        ist_date, ist_time = get_ist()
        save_to_sheet("Scores", [ist_date, ist_time, st.session_state['name'], st.session_state['mobile'], "-", "-", "-", "-", "-", "-", s_total, duration, st.session_state['user'], "Calculation"])
        st.session_state['saved'] = True
    
    if st.button("Back to Dashboard"):
        reset_module_state()
        st.rerun()
