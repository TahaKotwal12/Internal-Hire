import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration at the very beginning
st.set_page_config(page_title="Internal Hire", layout="wide", page_icon="./resources/favicon.ico")


# Load environment variables (if needed)
from dotenv import load_dotenv
load_dotenv()


# Add logo above the navigation menu
st.sidebar.image("./resources/logo.png", use_column_width=True)
st.logo("./resources/logo.png")


# Create a navigation menu with different Python files as options
selected = option_menu(
        menu_title=None,  # required
        options=["Dashboard", "Upload Resume", "Search Expertise"],  # options for the menu
        icons=["house", "upload", "search"],  # icons for the menu items
        default_index=0,  # default selected option,
        orientation="horizontal", 
)

# Logic to display the selected page
if selected == "Dashboard":
    exec(open("views/dashboard.py").read())  # Open and run the Dashboard page
elif selected == "Upload Resume":
    exec(open("views/upload_resume.py").read())  # Open and run the Upload Resume page
elif selected == "Search Expertise":
    exec(open("views/search_expertise.py").read())  # Open and run the Search Expertise page

# Footer text
st.sidebar.markdown(
    "<p style='text-align: center;'>Made for HR</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<p style='text-align: center;'>© 2024 Internal Hire</p>",
    unsafe_allow_html=True
)





