import streamlit as st
import base64
import firebase_admin
import re
from firebase_admin import credentials
from firebase_admin import auth

# Set the page config
st.set_page_config(page_title="Diet Mate")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('diet-planning-e62ca-cee72236ac11.json')
    firebase_admin.initialize_app(cred)

# Convert image to Base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set the background image for the entire page
def set_background_image(image_path):
    base64_image = image_to_base64(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url('data:image/jpeg;base64,{base64_image}');
            background-size: 100% 100%;
            background-position: center; 
            height: 100vh;
        }}
        .main-content {{
            padding: 40px;
            border-radius: 50px;
            max-width: 100px;
            text-align: left;
            margin-left: 100; 
        }}
        h1 {{
            font-size: 40px; /* Increased font size */
            text-align: left;
        }}
        p {{
            font-size: 18px; /* Increased font size */
            font-weight: bold; 
            text-align: left;
        }}
        .stButton > button {{
            background-color: #FF9900; /* Base color */
            color: white;
            padding: 4px 8px;  /* Smaller padding */
            font-size: 8px;  /* Smaller font size */
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 5px;
            width: 30%;  /* Maintain width but you can adjust as needed */
            position: relative;
            overflow: hidden;
            z-index: 0;
            transition: background-color 0.2s, box-shadow 0.2s;
        }}
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.2), rgba(0,0,0,0));
            opacity: 0;
            transition: opacity 0.3s, transform 0.3s;
            transform: scale(0.3);
            z-index: -1;
        }}
        .stButton > button:hover {{
            background-color: #FF9900;  
            box-shadow: 0 0 20px rgba(255, 165, 0, 0.7);  
        }}
        .stButton > button:hover::before {{
            opacity: 1;
            transform: scale(1);
        }}
        </style>
        """, unsafe_allow_html=True
    )

# Sidebar styling
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"]::before {
        content: "Diet Mate 🥗"; 
        font-size: 24px; 
        font-weight: bold; 
        padding: 120px 90px 0px 30px;
        display: block;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Home page function
def home():
    # Set the background image
    set_background_image("C:/SHREYA/Infosys_internship/assets/food.jpg")
    
    # Container for content
    with st.container():
        # Centered content with padding and background
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Title and description
        st.title('Plan Well! Eat Well!😋')
        st.write('Healthy living starts with mindful eating. Our app helps you embrace a lifestyle where every meal aligns with your unique health goals, dietary preferences, and medical needs. Together, we’ll craft a diet plan that feels less like a restriction and more like an exciting path to wellness')

        # Buttons to navigate to Login and Sign-Up
        col1, col2 = st.columns(2)

        with col1:
            st.button('Login', on_click=lambda: st.session_state.update(page='Login'))
        with col2:
            st.button('Sign Up', on_click=lambda: st.session_state.update(page='SignUp'))

        st.markdown('</div>', unsafe_allow_html=True)  # Close the main content div

# Login page function
def login():
    # Set the background image
    set_background_image("C:/SHREYA/Infosys_internship/assets/login.jpg")
    
    st.title('Login')

    # Input fields for email and password
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')

    # Login button functionality
    if st.button('Login', key="login_button"):
        if email and password:
            try:
                # Authenticate the user with Firebase
                user = auth.get_user_by_email(email)
                if user:
                    # Set user session state with details
                    st.session_state.user = {
                        'uid': user.uid,
                        'email': user.email,
                        'display_name': user.display_name  # Optional if you set a display name
                    }
                    st.success('Logged in successfully!')
                    st.session_state.page = 'profile'  # Redirect to DietPlan page
                else:
                    st.error('User not found.')
            except auth.UserNotFoundError:
                st.error('User not found. Please check your email or sign up.')
        else:
            st.error('Please enter both email and password.')
    # Button to redirect to Sign Up page
    st.write("Don't have an account?")

    if st.button('Go to Sign Up'):
        st.session_state.page = 'SignUp'  # Redirect to SignUp page

# Sign Up page function
def signup():
    # Set the background image
    set_background_image("C:/SHREYA/Infosys_internship/assets/login.jpg")
    st.title('Sign Up')

    # User inputs
    email = st.text_input('Email Address')
    username = st.text_input('Enter your unique username')
    password = st.text_input('Create Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    # Password validation logic
    def validate_password(password):
        if len(password) < 6:
            return "Password must be at least 6 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return "Password must contain at least one number."
        return None  # No issues found

    # Sign Up logic
    if st.button('Create my account'):
        # Check if the passwords match
        if password != confirm_password:
            st.error('Passwords do not match. Please check and try again.')
        else:
            # Validate password
            password_error = validate_password(password)
            if password_error:
                st.error(password_error)
            else:
                try:
                    # Create user in Firebase
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.success('Account created successfully!')
                    st.write('Please login using your email and password.')
                    st.balloons()  

                except Exception as e:
                    st.error(f'Error creating account: {e}')

    # Link to login page
    st.write('Already have an account?')
    if st.button('Login here'):
        st.session_state.page = 'Login'

# Function to run the app
def app():
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    if st.session_state.page == 'Home':
        home()
    elif st.session_state.page == 'Login':
        login()
    elif st.session_state.page == 'SignUp':
        signup()

# Run the app
app()