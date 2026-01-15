import streamlit as st
import cv2
import numpy as np
import os
import sys
from PIL import Image

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import ForgeryDetector

# Page configuration
st.set_page_config(page_title="Document Forgery Detector", layout="wide")

# Initialize Forgery Detector
detector = ForgeryDetector()

st.title("🛡️ Document Forgery Detector")
st.markdown("""
Extract digital fingerprints and compression artifacts to detect forgeries.
This tool uses **Error Level Analysis (ELA)** and **Metadata Inspection**.
""")

# File Uploader
uploaded_file = st.file_uploader("Upload a document image (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file temporarily to a path
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        # Load Original Image for Display
        original_image = Image.open(temp_path)
        
        # UI Layout: Two columns for comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(original_image, use_container_width=True)

        with col2:
            st.subheader("ELA Analysis")
            # Perform ELA
            ela_result = detector.perform_ela(temp_path)
            # Convert BGR (OpenCV) to RGB (Streamlit/PIL)
            ela_rgb = cv2.cvtColor(ela_result, cv2.COLOR_BGR2RGB)
            st.image(ela_rgb, use_container_width=True)
            st.caption("Bright areas indicate potential compression inconsistencies (forgeries).")

        # Metadata Section
        st.divider()
        st.subheader("📄 Metadata Forensic Report")
        
        metadata = detector.extract_metadata(temp_path)
        
        if metadata:
            # Check for red flags (Photoshop, GIMP, etc.)
            software = str(metadata.get('Software', '') or metadata.get('Software (Info)', '')).lower()
            red_flags = ["photoshop", "gimp", "adobe", "pixelmator"]
            
            found_red_flags = [flag for flag in red_flags if flag in software]
            
            if found_red_flags:
                st.error(f"⚠️ **RED FLAG**: Editing software detected in metadata: `{software}`")
                st.warning("The document has likely been processed by professional editing tools.")
            else:
                st.success("No obvious editing software markers found in standard EXIF tags.")

            # Display metadata table
            st.json(metadata)
        else:
            st.info("No EXIF metadata found in the image.")

    except Exception as e:
        st.error(f"Error during analysis: {e}")
    
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
else:
    st.info("Please upload an image to begin analysis.")
