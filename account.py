import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import google.auth
from google.oauth2 import id_token
from google.auth.transport import requests
file_path= "chathubconnect-b2484-0de26f648cfd.json"
# Initialize the Firebase Admin SDK
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)

def app():
    st.title('Welcome to :violet[SearchHub] :sunglasses')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    email = password = None  # Initialize email and password

    def f():
        nonlocal email, password
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    if choice == 'Sign up':
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        username = st.text_input("Enter your unique username")

        if st.button('Create my account'):
            user = auth.create_user(email=email, password=password, uid=username)
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()
    
    else:
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        login_button = st.button('Login', on_click=f)

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

    def ap():
        st.write('Query')

if __name__ == '__main__':
    app()
