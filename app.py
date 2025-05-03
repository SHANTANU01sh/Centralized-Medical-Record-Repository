# import streamlit as st
# from utils.auth import init_db, register_user, login_user
# from utils.file_manager import save_uploaded_file, CATEGORIES

# # Initialize DB
# init_db()

# # Initialize session state
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'username' not in st.session_state:
#     st.session_state.username = ''

# # Main login/register page
# def login_page():
#     st.title("🩺 Centralized Medical Record Repository")
#     st.subheader("Login or Register")

#     tabs = st.tabs(["🔐 Login", "📝 Register"])

#     with tabs[0]:
#         username = st.text_input("Username", key="login_user")
#         password = st.text_input("Password", type="password", key="login_pass")
#         if st.button("Login"):
#             if login_user(username, password):
#                 st.success("Login successful!")
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials.")

#     with tabs[1]:
#         new_user = st.text_input("New Username", key="reg_user")
#         new_pass = st.text_input("New Password", type="password", key="reg_pass")
#         if st.button("Register"):
#             if register_user(new_user, new_pass):
#                 st.success("Registration successful! You can now log in.")
#             else:
#                 st.error("Username already exists.")

# # Protected dashboard (shown after login)
# def dashboard():
#     st.sidebar.success(f"Logged in as: {st.session_state.username}")
#     st.sidebar.title("🧭 Navigation")
#     selection = st.sidebar.radio("Go to", ["🏠 Home", "📤 Upload Records"])

#     if selection == "🏠 Home":
#         st.title("📁 Welcome to Your Health Portal")
#         st.write("You can now upload and manage your medical records securely.")

#     elif selection == "📤 Upload Records":
#         st.title("📤 Upload Medical Records")
#         st.markdown("Upload your documents and organize them by category.")

#         category = st.selectbox("Select Category", CATEGORIES)
#         uploaded_file = st.file_uploader("Choose a medical file", type=["pdf", "png", "jpg", "jpeg", "txt"])

#         if uploaded_file is not None:
#             filepath = save_uploaded_file(st.session_state.username, category, uploaded_file)
#             st.success(f"File saved to: `{filepath}`")

#     if st.sidebar.button("Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = ''
#         st.rerun()


# # Routing
# if st.session_state.logged_in:
#     dashboard()
# else:
#     login_page()


import streamlit as st
from utils.auth import init_db, register_user, login_user
from utils.file_manager import save_uploaded_file, CATEGORIES
from utils.parser import extract_and_save_metrics, init_metrics_db
from utils.plots import fetch_metrics, plot_metric_trend

# Initialize DBs
init_db()
init_metrics_db()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''

# Main login/register page
def login_page():
    st.title("🩺 Centralized Medical Record Repository")
    st.subheader("Login or Register")

    tabs = st.tabs(["🔐 Login", "📝 Register"])

    with tabs[0]:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if login_user(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tabs[1]:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists.")

# Protected dashboard (shown after login)
def dashboard():
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.title("🧭 Navigation")
    selection = st.sidebar.radio("Go to", ["🏠 Home", "📤 Upload Records", "📊 Trends"])

    if selection == "🏠 Home":
        st.title("📁 Welcome to Your Health Portal")
        st.write("You can now upload and manage your medical records securely.")

    elif selection == "📤 Upload Records":
        st.title("📤 Upload Medical Records")
        st.markdown("Upload your documents and organize them by category.")

        category = st.selectbox("Select Category", CATEGORIES)
        uploaded_file = st.file_uploader("Choose a medical file", type=["pdf", "png", "jpg", "jpeg", "txt"])

        if uploaded_file is not None:
            filepath = save_uploaded_file(st.session_state.username, category, uploaded_file)
            st.success(f"File saved to: `{filepath}`")
            # Unified parsing for all formats
            metrics = extract_and_save_metrics(st.session_state.username, category, filepath)
            if metrics:
                st.info(f"Extracted and saved {len(metrics)} health metric(s) from this file.")
            else:
                st.info("No recognizable metrics found in this file.")

    elif selection == "📊 Trends":
        st.title("📊 Time-Series Trend Analysis")
        metric_name = st.selectbox("Select Metric", ["Hemoglobin", "Glucose", "CRP"])
        df = fetch_metrics(st.session_state.username, metric_name)
        fig = plot_metric_trend(df, metric_name)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for this metric yet.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.rerun()

# Routing
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
