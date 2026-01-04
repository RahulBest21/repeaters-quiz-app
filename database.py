import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_client():
    try:
        if "gcp_service_account" not in st.secrets: return None
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(st.secrets["gcp_service_account"]), scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

def get_data(worksheet_name):
    client = get_client()
    if client:
        try: 
            if worksheet_name == "Scores":
                raw_data = client.open("Repeaters_Database").worksheet(worksheet_name).get_all_values()
                if len(raw_data) > 1: return pd.DataFrame(raw_data[1:], columns=raw_data[0])
                return pd.DataFrame()
            else:
                return pd.DataFrame(client.open("Repeaters_Database").worksheet(worksheet_name).get_all_records())
        except: pass
    
    # Fallback for GK Questions if DB fails or is empty for testing
    if worksheet_name == "GK_Questions":
        return pd.DataFrame([
            {"Subject":"History","Chapter":"Ch-1 Ancient India","Quiz_Name":"Buddhism","Question":"Where did Gautama Buddha attain enlightenment?","OptionA":"Lumbini","OptionB":"Bodh Gaya","OptionC":"Sarnath","OptionD":"Kushinagar","Answer":"Bodh Gaya","Solution":"Bodh Gaya (Bihar)."},
            {"Subject":"History","Chapter":"Ch-1 Ancient India","Quiz_Name":"Mauryan Empire","Question":"Who fought the Kalinga War?","OptionA":"Chandragupta","OptionB":"Bindusara","OptionC":"Ashoka","OptionD":"Kanishka","Answer":"Ashoka","Solution":"Ashoka in 261 BC."},
            {"Subject":"Science","Chapter":"Ch-1 Biology","Quiz_Name":"Human Body","Question":"Largest bone in human body?","OptionA":"Tibia","OptionB":"Humerus","OptionC":"Femur","OptionD":"Fibula","Answer":"Femur","Solution":"Femur (thigh bone)."}
        ])
    return pd.DataFrame()

def save_to_sheet(worksheet_name, row_data):
    client = get_client()
    if not client: return False
    try: client.open("Repeaters_Database").worksheet(worksheet_name).append_row(row_data, value_input_option='USER_ENTERED'); return True
    except: return False

def update_password(username, new_pass):
    client = get_client()
    if not client: return False
    try:
        sheet = client.open("Repeaters_Database").worksheet("Users")
        cell = sheet.find(username)
        sheet.update_cell(cell.row, 2, new_pass)
        return True
    except: return False