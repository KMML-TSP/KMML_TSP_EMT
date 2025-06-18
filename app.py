import streamlit as st
import mysql.connector as conn

# SQL - Database

# Database connection
mydb = conn.connect(host="localhost",user="root",passwd="tspemt",database="tsp_emt")
# Cursor creation
mycursor = mydb.cursor()

# User Authentication
def authenticate_user(userid):
    sql = "SELECT * FROM users WHERE user_id=%s"
    val = (userid,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True

# Login Authentication
def authenticate_login(userid, password):
    sql = "SELECT * FROM users WHERE user_id=%s AND pass=%s"
    val = (userid, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True

# Signup Authentication
def authenticate_signup(usertype, userid):
    sql = "SELECT * FROM users WHERE role=%s AND user_id=%s"
    val = (usertype, userid)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True
    
# Already Created Check
def already_created(userid):
    sql = "SELECT is_active FROM users WHERE user_id=%s"
    val = (userid,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result == (1,):
        return True


# UI Components

# Set up the page
st.set_page_config(page_title="KMML Login", page_icon="Images/KMML.png", layout="wide")

# Inject external CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "select" not in st.session_state:
    st.session_state.select = "login"

# Web Pages
class Pages:
    # Login Page
    def login(self):
        # with col1:
        #     st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Login")

            # Input fields
            userid = st.text_input("User ID", key="userid_input")
            password = st.text_input("Password", type="password", key="password_input")

            btn, alert = st.columns([3.5, 6.5])

            if btn.button("Login", key="login_button"):
                if userid and password:
                    if userid.isdigit():
                        userid = int(userid)
                        if authenticate_user(userid):
                            if authenticate_login(userid, password):
                                alert.success("Login successful!")
                            else:
                                alert.error("Incorrect Password!")
                        else:
                            alert.error("Invalid User ID!")
                    else:
                        alert.error("Invalid User ID!")
                else:
                    alert.error("Please fill the forms.")

    # Signup Page
    def signup(self):
        # with col1:
        #     st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Signup")

            # Input fields
            usertype = st.selectbox("Select your Role", ["Admin", "Manager", "Staff", "Intern"], key="usertype_input")
            userid = st.text_input("User ID", key="userid_input")

            btn, alert = st.columns([4, 6])

            # Signup button
            if btn.button("Signup", key="signup_button"):
                if usertype and userid:
                    if userid.isdigit():
                        userid = int(userid)
                        if authenticate_user(userid):
                            if not already_created(userid):
                                if authenticate_signup(usertype, userid):
                                    st.session_state.select = "create_account"
                                    st.rerun()
                                else:
                                    alert.error("Invalid User Type!")
                            else:
                                alert.error("Account already exists!")
                        else:
                            alert.error("Invalid User ID!")
                    else:
                        alert.error("Invalid User ID!")
                else:
                    alert.error("Please fill the forms.")

    # Create Account Page
    def create_account(self):
        # with col1:
            # st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Create Account")



# NavBar
blank, title, btn1, btn2 = st.columns([1, 6, 1.5, 1.5], vertical_alignment="bottom", gap="small")

# Title image (logo)
title.image("Images/KMML.png")

# Buttons
if btn1.button("Login"):
    st.session_state.select = "login"
if btn2.button("Signup"):
    st.session_state.select = "signup"

# Main content area
main_container = st.container(height=400)

pages = Pages()

# Page content
with main_container:
    col1, col2 = st.columns([5.5, 4.5], gap="medium")

    col1.image("Images/KMML_TSP.jpg")

    if st.session_state.select == "login":
        pages.login()
    elif st.session_state.select == "signup":
        pages.signup()
    elif st.session_state.select == "create_account":
        pages.create_account()
