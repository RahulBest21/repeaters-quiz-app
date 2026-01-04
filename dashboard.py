import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_data
from utils import reset_module_state

def render_dashboard():
    # Sidebar
    with st.sidebar:
        st.write(f"👤 **{st.session_state['name']}**")
        st.write(f"📱 {st.session_state['mobile']}")
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown(f"## Welcome, {st.session_state['name']}")
    
    # --- Action Buttons ---
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧮 Start Math Calculation Test", use_container_width=True): 
            reset_module_state()
            st.session_state.update({'module': 'MATH', 'page': 'quiz'})
            st.rerun()
    with c2:
        if st.button("🧠 Start GK Quiz", use_container_width=True): 
            reset_module_state()
            st.session_state.update({'module': 'GK', 'gk_setup': False, 'page': 'quiz'})
            st.rerun()
            
    st.markdown("---")
    
    # --- ANALYTICS SECTION ---
    st.subheader("📊 Performance Analytics")
    
    df_scores = get_data("Scores")
    
    if df_scores.empty or len(df_scores.columns) < 14:
        st.info("No sufficient data available for analysis yet. Take a test!")
        return

    # Filter for current user
    user_scores = df_scores[df_scores['Username'] == str(st.session_state['user'])]
    
    if user_scores.empty:
        st.info("You haven't taken any tests yet.")
        return

    # Tabs for analysis
    tab1, tab2 = st.tabs(["📈 Progress", "🏆 Rank & Percentile"])
    
    with tab1:
        # Progress Line Chart
        try:
            # Ensure Total is numeric
            user_scores['Total'] = pd.to_numeric(user_scores['Total'], errors='coerce').fillna(0)
            user_scores['Date'] = pd.to_datetime(user_scores['Date'])
            
            fig = px.line(user_scores, x='Date', y='Total', color='Quiz_ID', markers=True, 
                          title="Your Score Progression over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Key Metrics
            m1, m2, m3 = st.columns(3)
            avg_score = user_scores['Total'].mean()
            tests_taken = len(user_scores)
            best_score = user_scores['Total'].max()
            
            m1.metric("Tests Taken", tests_taken)
            m2.metric("Average Score", f"{avg_score:.2f}")
            m3.metric("Best Score", int(best_score))
        except Exception as e:
            st.error(f"Error generating progress chart: {e}")

    with tab2:
        # Percentile Calculation per Quiz Type
        latest_test = user_scores.iloc[-1]
        quiz_id = latest_test['Quiz_ID']
        
        # Get all scores for this specific quiz type
        all_quiz_scores = df_scores[df_scores['Quiz_ID'] == quiz_id].copy()
        all_quiz_scores['Total'] = pd.to_numeric(all_quiz_scores['Total'], errors='coerce').fillna(0)
        
        user_score = float(latest_test['Total'])
        topper_score = all_quiz_scores['Total'].max()
        
        # Percentile Logic: (Number of people behind you / Total people) * 100
        total_participants = len(all_quiz_scores)
        participants_below = len(all_quiz_scores[all_quiz_scores['Total'] < user_score])
        percentile = (participants_below / total_participants) * 100
        
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown(f"### Latest Test: {quiz_id}")
            st.metric("Your Score", user_score)
            st.metric("Topper Score", topper_score)
            st.metric("Percentile", f"{percentile:.1f}%")
        
        with c2:
            # Histogram
            fig2 = px.histogram(all_quiz_scores, x="Total", nbins=20, title="Score Distribution (Where do you stand?)")
            # Add vertical line for user
            fig2.add_vline(x=user_score, line_width=3, line_dash="dash", line_color="green", annotation_text="You")
            fig2.add_vline(x=topper_score, line_width=3, line_dash="dash", line_color="red", annotation_text="Topper")
            st.plotly_chart(fig2, use_container_width=True)