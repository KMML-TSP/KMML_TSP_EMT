# Libraries Used: 

# 1. For App Creation
import streamlit as st
import mysql.connector as conn



# Check if user is authenticated
if "email" not in st.session_state:
    st.warning("You must be logged in to access this page.")
    st.stop()



# SQL - Database:

# 1. Database connection
mydb = conn.connect(host="localhost",user="root",passwd="tspemt",database="tsp_emt")
# 2. Cursor creation
mycursor = mydb.cursor(buffered=True)

# 3. User Details
mycursor.execute(f"SELECT * FROM users WHERE email = '{st.session_state['email']}'")
user_info = mycursor.fetchone()
# [0]=id, [1]=full_name, [2]=role, [3]=user_id, [4]=email, [5]=pass, [6]=created_at, [7]=is_active



# UI Components:

# 1. Set up the page
st.set_page_config(page_title="KMML Admin", page_icon="./images/KMML.png", layout="wide")

# 2. Inject external CSS
with open("./css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Initialize session state
if "select" not in st.session_state:
    st.session_state.select = "home"

# 4. Web Pages
class Pages:
    def home(self):
        st.title("Welcome to your Dashboard")
        st.write(f"Logged in as: {user_info[1]}")

    def profile(self):
        pass

# 5. NavBar
blank, title, btn1, btn2 = st.columns([1, 6, 1.5, 1.5], vertical_alignment="bottom", gap="small")

# 5.1 Title image (logo)
title.image("./images/KMML.png")

# 5.2 Buttons
if btn1.button("Home"):
    st.session_state.select = "home"
if btn2.button("Profile"):
    st.session_state.select = "profile"

# 6. Main content area
main_container = st.container()

# 7. Object to switch pages
pages = Pages()

# 8. Page content
with main_container:
    if st.session_state.select == "home":
        pages.home()
    elif st.session_state.select == "profile":
        pages.profile()