import streamlit as st


st.title("Welcome to Corvit..")
st.text("We are learning python in HCCDA-AI")

# image = st.camera_input("Enter your feed")

st.header("This is header")
st.subheader("This is subheader")
st.text("This is text")

st.markdown("# :green[This is markdown] :sunglasses:") #h1
st.markdown("## This is markdown") #h2
st.markdown("### This is markdown") #h3
st.markdown("#### This is markdown")
st.markdown("##### This is markdown")
st.markdown("###### This is markdown")

st.success("Successfully done!")
st.info("Information Required")
st.warning("Warning! Don't do this")
st.error("This is error")

st.write(range(10))

from PIL import Image

img = Image.open("test_image.jpg")
st.image(img, width=300)

st.video("https://youtu.be/rZySQU_WzDc?si=AyHt8Ey6rcBsKhh_")

st.slider("Slide", 0, 100)
