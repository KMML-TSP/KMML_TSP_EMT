import streamlit as st

# Set up the page
st.set_page_config(page_title="KMML Login", layout="wide")

# Inject external CSS
with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Web Pages
class Pages:
    def login(self):
        with col1:
            st.image("Images/KMML_TSP.jpg")

        with col2:
            # Header
            st.header("Login")

            # Input fields
            username = st.text_input("User Name", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")

            btn, alert = st.columns([1.1,3])

            # Login button
            if btn.button("Login", key="login_button"):
                if username and password:
                    alert.success("Login successful!")
                else:
                    alert.error("Please fill the forms.")

# Title
st.title("KMML TSP EMT")

# Define the main container for the page content
main_container = st.container(height=400)

select_pages = Pages()

# Main content
with main_container:
    col1, blank, col2 = st.columns([5, 0.1, 4])

    select_pages.login()

    

