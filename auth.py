import streamlit as st
from utils import hash_pass, gen_key, gen_captcha
from database import get_data, save_to_sheet, update_password

def render_auth(logo_html):
    # BRANDING: Added "Dashboard & Login by RahulBest"
    st.markdown(f"""
    <div style='text-align:center; padding:30px; background:white; border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.08); width:60%; margin:auto;'>
        {logo_html}
        <h1 style='color:#333; margin-bottom: 5px;'>The Repeaters Official</h1>
        <p style='color:#666; font-size: 14px; font-weight: 500; margin-top: 0;'>✨ Dashboard & Login Interface by <b>RahulBest</b></p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["🔐 Login", "📝 Register", "🆘 Reset"])
    
    with t1:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            c1, c2 = st.columns([1,2])
            with c1: st.info(f"{st.session_state['captcha_q']} = ?")
            with c2: ans = st.number_input("Ans", step=1, label_visibility="collapsed")
            
            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if ans != st.session_state['captcha_a']: 
                    st.error("Wrong Captcha")
                    q,a=gen_captcha() 
                    st.session_state.update({'captcha_q':q, 'captcha_a':a})
                    st.rerun()
                
                df = get_data("Users")
                if not df.empty:
                    df['Username'] = df['Username'].astype(str)
                    rec = df[df['Username'] == str(u)]
                    if not rec.empty and str(rec.iloc[0]['Password']) == hash_pass(p):
                        st.session_state.update({'user': u, 'name': rec.iloc[0]['Name'], 'mobile': str(rec.iloc[0]['Mobile']), 'page': 'dashboard'})
                        st.rerun()
                    else: st.error("Invalid Username or Password")
                elif u == "admin" and p == "admin": 
                    st.session_state.update({'user': "admin", 'name': "Administrator", 'mobile': "0000000000", 'page': 'dashboard'})
                    st.rerun()
                else: st.error("Database connection failed")

    with t2:
        with st.form("reg"):
            nu = st.text_input("Username")
            np_ = st.text_input("Password", type="password")
            nn = st.text_input("Name")
            nm = st.text_input("Mobile")
            if st.form_submit_button("Register", use_container_width=True):
                df = get_data("Users")
                if not df.empty and str(nu) in df['Username'].astype(str).values: 
                    st.error("Username Taken")
                else:
                    k = gen_key()
                    if save_to_sheet("Users", [nu, hash_pass(np_), nn, nm, k]): 
                        st.success(f"Registration Successful! Recovery Key: {k}")
                        st.info("Please save this key for password recovery.")
                    else: st.error("Registration Error")

    with t3:
        with st.form("reset"):
            fu, fk, fnp = st.text_input("User"), st.text_input("Key"), st.text_input("New Pass", type="password")
            if st.form_submit_button("Reset", use_container_width=True):
                df = get_data("Users")
                if not df.empty:
                    match = df[(df['Username'].astype(str)==fu) & (df['RecoveryKey']==fk)]
                    if not match.empty and update_password(fu, hash_pass(fnp)): 
                        st.success("Password Updated")
                    else: st.error("Invalid Credentials")
                else: st.error("DB Error")
