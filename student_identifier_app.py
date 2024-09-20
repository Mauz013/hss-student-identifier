import streamlit as st
import pandas as pd

# 1. Set page configuration first
st.set_page_config(
    page_title="HSS Student Identifier",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Function to load custom CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file `{file_name}` not found. Please ensure it exists in the repository.")

# Load custom CSS
load_css("style.css")

# 3. Function to load student numbers from Excel
@st.cache_data
def load_student_numbers(file_path):
    try:
        df = pd.read_excel(file_path)
        if 'StudentNumber' not in df.columns:
            st.error("Excel file must contain a 'StudentNumber' column.")
            return None
        # Convert to a set for faster lookup
        student_numbers = set(df['StudentNumber'].astype(str).str.strip())
        return student_numbers
    except FileNotFoundError:
        st.error(f"File `{file_path}` not found. Please ensure it exists in the repository.")
        return None
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# 4. Load student numbers from the local Excel file
student_numbers = load_student_numbers("students.xlsx")

# 5. Check if student numbers are loaded successfully
if student_numbers is None:
    st.stop()  # Stop the app if student numbers couldn't be loaded

# 6. Header
st.markdown('<div class="header">HSS Student Identifier</div>', unsafe_allow_html=True)

# 7. Form for input and submission
with st.form(key='student_form'):
    st.markdown('<div class="input-section">Enter the student number below to check enrollment status.</div>', unsafe_allow_html=True)
    
    student_input = st.text_input("", "", placeholder="Enter Student Number", key="input")
    
    submit_button = st.form_submit_button(label='Check')

# 8. Handle form submission
if submit_button:
    student_input = student_input.strip()
    if not student_input:
        st.warning("Please enter a student number.")
    else:
        if student_input in student_numbers:
            st.markdown(f'<div class="result success">✅ Student number {student_input} is <span style="color:#4CAF50;">ENROLLED</span>.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result error">❌ Student number {student_input} is <span style="color:#FF0000;">NOT ENROLLED</span>.</div>', unsafe_allow_html=True)
        
        # Option to search again
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("Search Again", key="back_button"):
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
