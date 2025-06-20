# Libraries Used:

# 1. For App Creation
import streamlit as st
import mysql.connector as conn
# 2. For Emailing Users
import smtplib
from email.message import EmailMessage
import random



# SQL - Database:

# 1. Database connection
mydb = conn.connect(host="localhost",user="root",passwd="tspemt",database="tsp_emt")
# 2. Cursor creation
mycursor = mydb.cursor()
    
# 3. Email Authentication
def authenticate_mail(email):
    sql = "SELECT id FROM users WHERE email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True

# 4. Login Authentication
def authenticate_login(email, password):
    sql = "SELECT id FROM users WHERE email=%s AND pass=%s"
    val = (email, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return True
    
# 5. Already Created Check
def already_created(email):
    sql = "SELECT is_active FROM users WHERE email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result == (1,):
        return True
    
# 6. User Account Creation
def create_user(password, email):
    sql = "UPDATE users SET pass=%s, is_active=%s WHERE email=%s"
    val = (password, 1, email)
    mycursor.execute(sql, val)
    mydb.commit()
    return True

# 7. User Role Identification
def identify_role(email):
    sql = "SELECT role FROM users WHERE email=%s"
    val = (email,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return result[0]
    


# Send Email:
def send_password_email(usermail, password):
    # Company Mail Credentials
    EMAIL_ADDRESS = "kmmltspemt@gmail.com"
    EMAIL_PASSWORD = "tspemt@123"

    # Mail content
    msg = EmailMessage()
    msg['Subject'] = "KMML Account Signup - Verification Password"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = usermail
    msg.set_content(f"Your signup verification password is: {password}\n\nKMML EMT Team")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False



# UI Components:

# 1. Set up the page
st.set_page_config(page_title="KMML Login", page_icon="images/KMML.png", layout="wide")

# 2. Inject external CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Initialize session state
if "select" not in st.session_state:
    st.session_state.select = "login"

# 4. Web Pages
class Pages:
    # 4.1 Login Page
    def login(self):
        # Header
        st.header("Login")

        # Input fields
        usermail = st.text_input("User Email", key="usermail_input").strip()
        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login", key="login_button"):
            if usermail and password:
                if authenticate_mail(usermail):
                    if authenticate_login(usermail, password):
                        st.success("Login successful!")

                        # Next Page Navigation
                        user_role = identify_role(usermail)
                        st.session_state["email"] = usermail
                        st.switch_page(user_role)
                    else:
                        st.error("Incorrect Password!")
                else:
                    st.error("Invalid email address!")
            else:
                st.error("Please fill in all the fields.")


    # 4.2 Signup Page
    def signup(self):
        # Header
        st.header("Signup")

        # Input fields
        usermail = st.text_input("User Email", key="usermail_input").strip()
        password = st.text_input("Password", type="password", key="password_input")

        btn1, btn2 = st.columns([5,4], gap="small")
        
        # Get Password
        if btn1.button("Get Password", key="get_password_button"):
            if usermail:
                if authenticate_mail(usermail):
                    if already_created(usermail):
                        # Generate 6-digit numeric password
                        mailed_password = str(random.randint(100000, 999999))
                        st.session_state["mailed_password"] = mailed_password

                        # Send email to usermail
                        if send_password_email(usermail, st.session_state["mailed_password"]):
                            st.success("Password has been sent to your email.")
                        else:
                            st.error("Failed to send email. Try again.")
                    else:
                        st.error("This account is already created!")
                else:
                    st.error("Email is not in the company list!")
            else:
                st.error("Please enter your email!")

        # Signup
        if btn2.button("Signup", key="signup_button"):
            if usermail and password:
                if authenticate_mail(usermail):
                    if already_created(usermail):
                        if password == st.session_state["mailed_password"]:
                            if create_user(password, usermail):
                                st.success("Signup successful!")

                                # Next Page Navigation
                                user_role = identify_role(usermail)
                                st.write(user_role)
                                st.session_state["email"] = usermail
                                # st.switch_page(f"pages/{user_role}.py")
                                # st.switch_page(f"pages/admin.py")
                                # st.switch_page("Admin")
                                st.switch_page(user_role)
                            else:
                                st.error("Failed to create account!")
                        else:
                            st.error("Incorrect Verification Password!")
                    else:
                        st.error("This account is already created!")
                else:
                    st.error("Email is not in the company list!")
            else:
                st.error("Please fill in all the fields.")



# 5. NavBar
blank, title, btn1, btn2 = st.columns([1, 6, 1.5, 1.5], vertical_alignment="bottom", gap="small")

# 5.1 Title image (logo)
title.image("images/KMML.png")

# 5.2 Buttons
if btn1.button("Login"):
    st.session_state.select = "login"
if btn2.button("Signup"):
    st.session_state.select = "signup"

# 6. Main content area
main_container = st.container()

# 7. Object to switch pages
pages = Pages()

# 8. Page content
with main_container:
    col1, col2 = st.columns([5.5, 4.5], gap="medium")

    col1.image("images/KMML_TSP.jpg")

    with col2:
        if st.session_state.select == "login":
            pages.login()
        elif st.session_state.select == "signup":
            pages.signup()