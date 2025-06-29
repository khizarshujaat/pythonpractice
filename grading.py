import streamlit as st

st.title("Corvit Grading System...")

marks = st.number_input("Enter Obtain marks:", min_value=1)
total = st.number_input("Enter total marks:", min_value=1)

p = round(marks / total * 100, 2)

r = st.button("Calculate result")

if r:
    st.subheader(f'Your Percentage :blue[{p} %]')

    if p >= 80:
        st.success('Excellent')
    elif p >= 60 and p < 80:
        st.info('Pass')
    else:
        st.error('Fail')