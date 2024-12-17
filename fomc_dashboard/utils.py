import streamlit as st
import base64


def set_background(image_path):
    """
    Set a background image for the Streamlit app.

    Args:
        image_path (str): Absolute path to the local image file.
    """
    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Inject CSS into the Streamlit app
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
