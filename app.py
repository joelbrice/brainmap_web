import streamlit as st
import requests
import time
from PIL import Image
import numpy as np





# Page configuration MUST BE FIRST
st.set_page_config(
    page_title="Brainmap",
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

# Function to load custom CSS for theme switching
# Function to load custom CSS for theme switching
def load_custom_css(theme="light"):
    if theme == "light":
        css = """
        <style>
            /* Light Theme Styles */
            body {
                background-color: #F8F9FA; /* light background */
                color: #000; /* dark text color */
            }
            .sidebar .sidebar-content {
                background-color: #FFFFFF; /* white background for sidebar */
                color: #000; /* dark text in sidebar */
            }
            .sidebar .sidebar-header {
                background-color: #F8F9FA; /* light background for sidebar header */
            }
            .css-1v3fvcr {
                background-color: #F8F9FA !important; /* background color fix for Streamlit widgets */
            }
            .custom-title {
                font-size: 50px;
                font-weight: bold;
                color: #4CAF50; /* Green title */
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
            .stButton>button {
                background-color: #4CAF50; /* Green button color */
                color: white;
                border-radius: 5px;
                border-color: transprent;
            }
            .stButton>button:hover {
                background-color: #45A049; /* Darker green on hover */
                border: none;
            }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    elif theme == "dark":
        css = """
        <style>
            /* Dark Theme Styles */
            body {
                background-color: #2E2E2E; /* dark background */
                color: #FFFFFF; /* white text color */
            }
            .stAppViewContainer{
                background-color: #2E2E2E; /* dark background */
                color: #FFFFFF !important; /* white text color */
            }
             .stSidebar  {
                background-color: #1E1E1E; /* dark background for sidebar */
                color: #FFFFFF; /* white text in sidebar */
            }

            .stRadio {
                background-color: #1E1E1E !important;
                color: #FFFFFF !important;
            }
            .custom-title {
                font-size: 50px;
                font-weight: bold;
                color: #FF9800; /* Orange title for dark theme */
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
            .stButton>button {
                background-color: #FF9800; /* Orange button color */
                color: white;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #FB8C00; /* Darker orange on hover */
            }
        </style>
        """
        # Inject the custom CSS styles into the app
        st.markdown(css, unsafe_allow_html=True)



st.title("Advanced MRI Analysis for Tumor Detection")
logo = Image.open("static/images/brainmap_logo.png")

# Provide a detailed description

# Set the title of the application

# Provide a detailed description with enhanced styling
st.markdown("""
### Welcome to **BrainMap**!

**BrainMap** is a cutting-edge platform leveraging artificial intelligence to revolutionize brain tumor detection and classification. Our state-of-the-art deep learning algorithms analyze MRI scans with precision, providing rapid and accurate assessments to support medical professionals in their diagnostic process.

#### How It Works:
- **Upload an MRI Image**: Simply upload your MRI image using the interface.
- **Get Instant Predictions**: Our advanced system will swiftly process the image and deliver a comprehensive analysis indicating the presence or absence of tumors.

#### Why Choose BrainMap?
- **Reliable**: Combining the power of machine learning with medical expertise.
- **Efficient**: Non-invasive tool for early tumor detection.
- **Improving Outcomes**: Potentially enhances patient outcomes through timely intervention.

Thank you for choosing BrainMap as your trusted partner in medical imaging analysis!
""")



# Sidebar for settings and branding
st.sidebar.image(logo, width=150)
st.sidebar.header(":brain: BrainMap Navigation")
st.sidebar.write(":bust_in_silhouette: **About Us**")
st.sidebar.write(":mag: **Upload MRI Image**")
st.sidebar.write(":bar_chart: **Results**")
st.sidebar.markdown("---")
st.sidebar.write(":page_facing_up: Visit our [documentation](https://joelbrice.github.io/brainmap.github.io/).")

st.sidebar.title("Settings")
# Add a sidebar theme selector
theme = st.sidebar.radio("Choose a Theme:", ["Light", "Dark"])
# Apply the selected theme's CSS
load_custom_css(theme.lower())


'''
## Upload MRI Image
'''

# URL of the API
url = 'https://brainmapv1-390823521738.europe-west3.run.app/predict'  # Update this to the correct URL of your FastAPI server
# Placeholder for the image
image_placeholder = st.empty()

SHOW_THANK_YOU = False

# Upload_file:
uploaded_file = st.file_uploader("Choose an MRI image...", type=["tif", "tiff", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, width=300, caption="Uploaded image")
    if st.button('Predict'):
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
# Function to load custom CSS
