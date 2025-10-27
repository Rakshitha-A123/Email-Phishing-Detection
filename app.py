import streamlit as st
from datetime import datetime
import json
from users import UserManager
from database import EmailHistory
from detector import PhishingDetector

# Initialize components
user_manager = UserManager()
email_history = EmailHistory()
detector = PhishingDetector()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    st.title("📧 Phishing Email Detector - Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if user_manager.verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Register")
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Register"):
            if not new_username or not new_password:
                st.error("Please fill in all fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            elif user_manager.add_user(new_username, new_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

def analyze_and_store_email(email_input, username):
    try:
        # Analyze email
        result = detector.analyze_email(email_input)
        
        # Store in history
        success = email_history.add_entry(
            user_id=username,
            email_content=email_input,
            prediction=result['is_phishing'],
            confidence=result['risk_score'] / 100,
            features=json.dumps(result['reasons']),
            risk_score=result['risk_score']
        )
        
        if not success:
            st.warning("Note: Failed to save to history")
        
        return result
        
    except Exception as e:
        print(f"Error in analyze_and_store_email: {str(e)}")
        st.error(f"An error occurred while analyzing: {str(e)}")
        return None

def main_app():
    # Add logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    st.sidebar.write(f"Welcome, {st.session_state.username}!")
    
    # Main tabs
    tab1, tab2 = st.tabs(["Email Analysis", "History"])
    
    with tab1:
        st.title("📧 Phishing Email Detector")
        st.write("Paste the email content below to check if it's phishing or legitimate:")
        
        email_input = st.text_area("Email Content", height=200)
        
        if st.button("Check Email"):
            if not email_input.strip():
                st.warning("⚠️ Please enter some email content to check.")
                return
            
            try:
                with st.spinner("Analyzing email..."):
                    # Analyze and store results
                    result = analyze_and_store_email(email_input, st.session_state.username)
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if result['is_phishing']:
                            st.error("🚨 PHISHING DETECTED")
                        else:
                            st.success("✅ LIKELY LEGITIMATE")
                        
                        st.metric("Risk Score", f"{result['risk_score']}%")
                    
                    with col2:
                        st.info("### Detected Issues")
                        if result['reasons']:
                            for reason in result['reasons']:
                                st.write(reason)
                        else:
                            st.write("No suspicious elements detected.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with tab2:
        st.title("📊 Testing History")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("View your previous email analysis results:")
        with col2:
            if st.button("Clear History"):
                email_history.clear_user_history(st.session_state.username)
                st.success("History cleared!")
                st.rerun()
        
        history = email_history.get_user_history(st.session_state.username)
        if not history:
            st.info("No history found. Start analyzing emails to build your history!")
        else:
            for entry in history:
                with st.expander(f"Email tested on {datetime.fromisoformat(entry[4]).strftime('%Y-%m-%d %H:%M:%S')}"):
                    st.write("**Email Content:**")
                    st.text(entry[1][:200] + "..." if len(entry[1]) > 200 else entry[1])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        result_text = "🚨 Phishing" if entry[2] == 1 else "✅ Legitimate"
                        st.write(f"**Result:** {result_text}")
                    with col2:
                        st.write(f"**Risk Score:** {entry[3]:.1%}")
                    
                    if entry[5]:
                        st.write("**Detected Issues:**")
                        for feature in json.loads(entry[5]):
                            st.write(f"- {feature}")

def main():
    st.set_page_config(
        page_title="Phishing Email Detector",
        page_icon="📧",
        layout="wide"
    )
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()