import streamlit as st
import pandas as pd

# Set page configuration for better mobile experience
st.set_page_config(
    page_title="HSS Student Identifier",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'student_input' not in st.session_state:
    st.session_state.student_input = ''

# Function to load student numbers from Excel
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

# Load student numbers from the local Excel file
student_numbers = load_student_numbers("students.xlsx")

# Home Page: Input Student Number
def home_page():
    st.title("HSS Student Identifier")
    st.write("Enter a student number below to check if the student is enrolled.")
    
    # Input field for student number
    student_input = st.text_input("Student Number", "")
    
    # Check button
    if st.button("Check"):
        if not student_input.strip():
            st.warning("Please enter a student number.")
        else:
            # Store the input and navigate to result page
            st.session_state.student_input = student_input.strip()
            st.session_state.page = 'result'

# Result Page: Display Membership Status
def result_page():
    st.title("Check Result")
    
    student_input = st.session_state.get('student_input', '')
    
    if student_input in student_numbers:
        st.success(f"**Student number {student_input}** is **ENROLLED**.")
    else:
        st.error(f"**Student number {student_input}** is **NOT ENROLLED**.")
    
    # Back button to return to home page
    if st.button("Back"):
        st.session_state.page = 'home'

# Main App Logic
def main():
    if student_numbers is None:
        st.stop()  # Stop the app if student numbers couldn't be loaded
    
    # Navigate between pages based on session state
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'result':
        result_page()
    else:
        st.session_state.page = 'home'  # Fallback to home page

if __name__ == "__main__":
    main()
