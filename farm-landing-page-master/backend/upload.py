import streamlit as st
import cv2
import numpy as np
from PIL import Image

def analyze_mango_ripeness(image):
    image_np = np.array(image)

    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    lower_fully_ripe = np.array([0, 100, 100])
    upper_fully_ripe = np.array([30, 255, 255])

    lower_partially_ripe = np.array([31, 100, 100])
    upper_partially_ripe = np.array([60, 255, 255])

    lower_unripe = np.array([61, 100, 100])
    upper_unripe = np.array([90, 255, 255])

    mask_fully_ripe = cv2.inRange(image_bgr, lower_fully_ripe, upper_fully_ripe)
    mask_partially_ripe = cv2.inRange(image_bgr, lower_partially_ripe, upper_partially_ripe)
    mask_unripe = cv2.inRange(image_bgr, lower_unripe, upper_unripe)

    fully_ripe_pixel_count = cv2.countNonZero(mask_fully_ripe)
    partially_ripe_pixel_count = cv2.countNonZero(mask_partially_ripe)
    unripe_pixel_count = cv2.countNonZero(mask_unripe)

    total_pixels = image_bgr.shape[0] * image_bgr.shape[1]
    fully_ripe_percentage = (fully_ripe_pixel_count / total_pixels) * 100
    partially_ripe_percentage = (partially_ripe_pixel_count / total_pixels) * 100
    unripe_percentage = (unripe_pixel_count / total_pixels) * 100

    ripeness = "Unknown"
    max_percentage = max(fully_ripe_percentage, partially_ripe_percentage, unripe_percentage)

    if fully_ripe_percentage == max_percentage:
        ripeness = "Fully Ripe"
    elif partially_ripe_percentage == max_percentage:
        ripeness = "Partially Ripe"
    elif unripe_percentage == max_percentage:
        ripeness = "Unripe"

    st.image(image, caption="Original Image", use_column_width=True)
    st.header("Ripeness Categories:")
    st.write("Fully Ripe: %.2f%%" % fully_ripe_percentage)
    st.write("Partially Ripe: %.2f%%" % partially_ripe_percentage)
    st.write("Unripe: %.2f%%" % unripe_percentage)
    st.write("Dominant Ripeness Category:", ripeness)

st.title("Mango Ripeness Analysis")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    analyze_mango_ripeness(image)


# streamlit run upload.py --server.enableXsrfProtection=false

# index.html
# gunicorn --bind 
# pm2 
# streamlit run upload.py

