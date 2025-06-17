import streamlit as st

# Set up the page
st.set_page_config(page_title="KMML Login", layout="wide")

# Inject external CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "select" not in st.session_state:
    st.session_state.select = "login"

# Web Pages
class Pages:
    def login(self, col1, col2):
        with col1:
            st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Login")

            # Input fields
            username = st.text_input("User Name", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")

            btn, alert = st.columns([3.5, 6.5])

            msg_placeholder = alert.empty()

            if btn.button("Login", key="login_button"):
                if username and password:
                    msg_placeholder.success("Login successful!")
                else:
                    msg_placeholder.error("Please fill the forms.")
            else:
                # Always keep some space reserved for the alert
                msg_placeholder.markdown("<div class='alert-space'></div>", unsafe_allow_html=True)


    def signup(self, col1, col2):
        with col1:
            st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Signup")

            # Input fields
            usertype = st.selectbox("Select your Role", ["Admin", "Manager", "Staff", "Intern"], key="usertype_input")
            username = st.text_input("User Name", key="signup_username_input")

            btn, alert = st.columns([4.5, 5.5])

            # Signup button
            if btn.button("Signup", key="signup_button"):
                if usertype and username:
                    alert.success("Signup successful!")
                else:
                    alert.error("Please fill the forms.")

# NavBar
blank, title, btn1, btn2 = st.columns([1, 6, 1.5, 1.5], vertical_alignment="bottom", gap="small")

# Title image (logo)
title.image("Images/KMML.png", use_container_width=True)

# Buttons
if btn1.button("Login"):
    st.session_state.select = "login"
if btn2.button("Signup"):
    st.session_state.select = "signup"

# Main content area
main_container = st.container(height=400)

# Page content
with main_container:
    col1, col2 = st.columns([5.5, 4.5], gap="medium")
    pages = Pages()

    if st.session_state.select == "login":
        pages.login(col1, col2)
    elif st.session_state.select == "signup":
        pages.signup(col1, col2)
