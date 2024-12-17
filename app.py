import streamlit as st
import requests
import time
from PIL import Image
import numpy as np
# Page configuration MUST BE FIRST
st.set_page_config(
    page_title="BrainMap Web",
    page_icon=":brain:",
    layout="wide",
    initial_sidebar_state="expanded",
)
# # Load custom CSS for styling
st.markdown('''
<style>
.big-font {
    font-size:20px !important;
}
.custom-title {
    font-size: 50px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}
.custom-footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    color: gray;
    font-size: 12px;
}
</style>
''', unsafe_allow_html=True)
# st.markdown('''
# <style>
# .big-font {
#     font-size:20px !important;
# }
# </style>
# ''', unsafe_allow_html=True)
'''
# Brainmap, a tumor detection and classification platform!
'''
st.markdown('<p class="big-font">Welcome to Brainmap! A platform for tumor detection. Upload an MRI image and get a prediction on whether it indicates the presence of tumor or not.</p>', unsafe_allow_html=True)
# Load and display the logo
logo = Image.open("static/images/brainmap_logo.png")
# Main header
st.image(logo, width=200)
st.markdown('<div class="custom-title">BrainMap MRI Analysis</div>', unsafe_allow_html=True)
st.write("Welcome to BrainMap! Upload an MRI image and get a prediction on whether it indicates the presence of a tumor or not.")
# Sidebar for settings and branding
st.sidebar.image(logo, width=150)
st.sidebar.title("Settings")
theme = st.sidebar.radio("Choose a Theme:", ["Light", "Dark", "Custom"])
st.sidebar.write("Visit our [documentation](https://brainmap-docs.com).")

'''
## Upload MRI Image
'''
# URL of the API
url = 'https://brainmapv1-390823521738.europe-west3.run.app/predict'  # Update this to the correct URL of your FastAPI server
# Placeholder for the image
image_placeholder = st.empty()

SHOW_THANK_YOU = " "

# Upload_file:
uploaded_file = st.file_uploader("Choose an MRI image...", type=["tif", "tiff", "png", "jpg", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, width=300, caption="Uploaded image")
    if st.button('Get Prediction and the Probability of having a tumor'):
        # Loading bar starts here
        with st.spinner('Processing the image...'):
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
        # Proceed with the image processing and prediction
        img = uploaded_file.getvalue()
        files = {"file": ("image.jpeg", img, "image/jpeg")}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            result = response.json()
            if "Prediction" in result and 'Probability' in result:
                prediction = result["Prediction"]
                probability = result["Probability"]
                if prediction is not None:
                    if prediction == 'notumor':
                        st.markdown(f"<h2 style='color:green;'>No tumor detected</h2>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h2 style='color:red;'>Tumor detected: {prediction}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color:black;'>Probability: {probability * 100:.2f}%</h3>", unsafe_allow_html=True)
                     # Set the flag to show "Thank you" message
                    SHOW_THANK_YOU = True
                else:
                    st.error("Error: Prediction value is None.")
            else:
                st.error("Error: 'Prediction' key not found in API response.")
        else:
            st.error(f"Error in API request. Status code: {response.status_code}")
# Conditional "Thank you" message
if SHOW_THANK_YOU:
    st.markdown('<p class="big-font">Thank you for using BrainMap!</p>', unsafe_allow_html=True)

def load_custom_css():
    css = """
        <style>
        /* Add a background color */
        body {
            background-color: #F5F7FA;
        }
        /* Style the header text */
        .main-title {
            font-size: 50px;
            font-weight: bold;
            color: #4CAF50; /* Green */
            text-align: center;
            margin-bottom: 20px;
        }
        /* Footer style */
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            color: gray;
            font-size: 12px;
        }
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)
# Apply the custom CSS
load_custom_css()
# Footer
st.markdown('<div class="custom-footer">© 2024 BrainMap Inc. All rights reserved.</div>', unsafe_allow_html=True)
