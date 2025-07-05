import streamlit as st

# Custom CSS for each button
st.markdown("""
<style>
    /* Blue button */
    .st-key-blue button {
        background-color: #4285F4;
        color: white;
        border: none;
    }
    .st-key-blue button:hover {
        background-color: #3367D6;
    }

    /* Red button */
    .st-key-red button {
        background-color: #EA4335;
        color: white;
        border: none;
    }
    .st-key-red button:hover {
        background-color: #D33426;
    }

    /* Green button */
    .st-key-green button {
        background-color: #34A853;
        color: white;
        border: none;
    }
    .st-key-green button:hover {
        background-color: #2D9248;
    }

    /* Yellow button */
    .st-key-yellow button {
        background-color: #FBBC05;
        color: black;
        border: none;
    }
    .st-key-yellow button:hover {
        background-color: #E9AB04;
    }
</style>
""", unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('Blue Button', key='blue'):
        st.write("Blue button clicked!")

with col2:
    if st.button('Red Button', key='red'):
        st.write("Red button clicked!")

with col3:
    if st.button('Green Button', key='green'):
        st.write("Green button clicked!")

with col4:
    if st.button('Yellow Button', key='yellow'):
        st.write("Yellow button clicked!")