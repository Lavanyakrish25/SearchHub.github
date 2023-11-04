import streamlit as st

def app():
    st.title('Welcome to SearchHub')
    
    # Introduction and description of your website
    st.write('Welcome to this  website. This is the home page where you can get the Basic information and working of SEARCHHUB.')
    
    # Links to other pages
    st.subheader('Explore Our Website:')
    st.write('**Step 1**: Go to Account page and SignUp or Login.' )
    st.write('**Step 2**: Once you have logged-in,go to "QUERY PDF" page ,upload the PDF file which you want to query.')
    st.write('**Step 3**: Finally go to About page to know about ME. ')
    # You can customize the design and content further to match your website's branding.
    st.subheader('Main Features:')
    st.write('1. **Account Page**: Sign in or sign up to access personalized features.')
    st.write('2. **Query Page**: Upload PDF files for AI-based processing and ask questions.')
    st.write('3. **About Page**: Now about Me.')

    st.subheader('Important Note:')
    st.write("If you need any personalized assistant or any  AI related service, I'M here to help and work with you.")
    
    # Add your contact information here
    st.write("Contact details in about page")