import streamlit as st
import base64
import os

def load_css():
    # Logo handling
    logo_file = "logo.png"
    logo_html = ""
    if os.path.exists(logo_file):
        with open(logo_file, 'rb') as f: bin_str = base64.b64encode(f.read()).decode()
        logo_html = f"<img src='data:image/png;base64,{bin_str}' class='logo-img'>"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        /* FORCE DAY MODE / LIGHT THEME */
        :root {{
            --primary-color: #ff4b4b;
            --background-color: #ffffff;
            --secondary-background-color: #f0f2f6;
            --text-color: #31333F;
            --font: "Inter", sans-serif;
        }}
        
        /* Force main app background to white */
        .stApp {{
            background-color: #ffffff !important;
            color: #31333F !important;
        }}
        
        /* Sidebar background */
        section[data-testid="stSidebar"] {{
            background-color: #f8f9fa !important;
            border-right: 1px solid #ddd;
        }}
        
        /* Text color overrides to ensure readability */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: #31333F !important;
        }}
        
        /* Input fields background */
        input, textarea, select {{
            background-color: #ffffff !important;
            color: #31333F !important;
            border: 1px solid #ddd !important;
        }}
        
        /* Table text color */
        th, td {{
            color: #31333F !important;
        }}

        /* HIDE DEFAULT STREAMLIT ELEMENTS */
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stApp {{ margin-top: -50px; }}

        /* LOGO STYLING */
        .logo-img {{ height: 80px; width: auto; margin-bottom: 10px; }}

        /* TCS iON HEADER STYLE */
        .test-header {{
            background: white !important;
            padding: 10px 20px;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 999;
        }}
        .test-title {{ font-size: 18px; font-weight: 700; color: #333 !important; }}
        .timer-box {{ font-size: 20px; font-weight: 700; color: #d9534f !important; background: #fdf2f2 !important; padding: 5px 15px; border-radius: 5px; border: 1px solid #f8d7da; }}

        /* QUESTION PALETTE */
        .palette-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            padding: 10px;
            background: #fdfdfd !important;
            border: 1px solid #ddd;
            height: 400px;
            overflow-y: auto;
        }}
        
        /* STATUS COLORS (TCS Standard) */
        .status-answered {{ background-color: #5cb85c !important; color: white !important; border-color: #4cae4c !important; }}
        .status-not_answered {{ background-color: #d9534f !important; color: white !important; border-color: #d43f3a !important; }}
        .status-review {{ background-color: #5bc0de !important; color: white !important; border-color: #46b8da !important; }}
        .status-not_visited {{ background-color: #fff !important; color: #333 !important; }}
        .status-current {{ border: 2px solid #f0ad4e !important; box-shadow: 0 0 5px #f0ad4e; }}

        .legend-box {{ width: 20px; height: 20px; margin-right: 8px; border-radius: 3px; border: 1px solid #ccc; }}

        /* ACTION BAR */
        .action-bar {{
            background: #f8f9fa !important;
            padding: 10px;
            border-top: 1px solid #ddd;
            border-bottom: 1px solid #ddd;
            margin-bottom: 15px;
        }}
        div.stButton > button {{ width: 100%; border-radius: 4px; font-weight: 600; }}
        
        /* ANALYTICS CARDS */
        .metric-card {{
            background: white !important;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .solution-box {{
            background: white !important;
            border-left: 5px solid #ef4444;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            color: #333 !important;
        }}
        
        /* Tab Text Color Force */
        button[data-baseweb="tab"] {{
            color: #31333F !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return logo_html
