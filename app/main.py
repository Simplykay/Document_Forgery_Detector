import streamlit as st
import cv2
import numpy as np
import os
import sys
import time
import io
from PIL import Image

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import ForgeryDetector
from src.converter import DocumentProcessor
from src.metadata import scan_metadata
from app.ui_components import render_neon_scanner, inject_scanner_bar

# Page configuration
st.set_page_config(page_title="Document Forgery Detector Pro", layout="wide")

# Initialize Logic Classes
detector = ForgeryDetector()
processor = DocumentProcessor()

# Inject CSS for Neon Scanner
render_neon_scanner()

st.title("🛡️ Document Forgery Detector Pro")
st.markdown("""
Extract digital fingerprints, compression artifacts, and hidden metadata to detect forgeries.
Supports **Images (JPG/PNG)**, **PDFs**, and **Word (DOCX)** documents.
""")

# File Uploader
uploaded_file = st.file_uploader("Upload a file for forensic analysis", type=["jpg", "jpeg", "png", "pdf", "docx"])

if uploaded_file is not None:
    # 1. Setup UI Placeholders
    scanner_placeholder = st.empty()
    result_placeholder = st.empty()
    
    # Show the Neon Scanner animation
    with scanner_placeholder.container():
        st.info("🔍 Initiating Deep Forensic Scan...")
        inject_scanner_bar()
        # Preview of what's being scanned (if it's an image)
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="Scanning original image...", use_container_width=True)
        else:
            st.warning(f"Extracting forensic data from {uploaded_file.name}...")

    # 2. Background Processing
    try:
        # We'll store everything in a dict to display later
        report = {
            "red_flags": [],
            "ela_image": None,
            "original_image": None,
            "metadata": {}
        }

        # Step A: Metadata Scanning (Deep scan for PDF/Docx)
        # Convert UploadedFile to BytesIO for scanning
        file_bytes = uploaded_file.getvalue()
        file_io = io.BytesIO(file_bytes)
        
        # Get Red Flags from metadata
        report["red_flags"] = scan_metadata(file_io)

        # Step B: Document Processing / Image Extraction
        if uploaded_file.name.endswith('.pdf'):
            bgr_image = processor.process_pdf(file_bytes)
        elif uploaded_file.name.endswith('.docx'):
            bgr_image = processor.process_word(file_bytes)
        else:
            # It's an image
            nparr = np.frombuffer(file_bytes, np.uint8)
            bgr_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        report["original_image"] = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        # Step C: ELA Analysis
        # We need a temp file for ELA because the current class expects a path
        temp_path = f"temp_analysis_{uploaded_file.name}"
        if uploaded_file.name.endswith(('.pdf', '.docx')):
            temp_path += ".jpg" # Ensure it's a jpg for ELA
        
        cv2.imwrite(temp_path, bgr_image)
        
        try:
            ela_result = detector.perform_ela(temp_path)
            report["ela_image"] = cv2.cvtColor(ela_result, cv2.COLOR_BGR2RGB)
            
            # Extract image-specific EXIF metadata if it's an image
            if not uploaded_file.name.endswith(('.pdf', '.docx')):
                img_metadata = detector.extract_metadata(temp_path)
                # Check for image software flags
                software = str(img_metadata.get('Software', '')).lower()
                if any(tool in software for tool in ["photoshop", "gimp", "adobe"]):
                    report["red_flags"].append(f"Image EXIF: Editing software detected: {software}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        # 3. Simulated "Processing" Delay (As requested 3-5s)
        time.sleep(3.5)

        # 4. Clear Scanner and Display Results
        scanner_placeholder.empty()

        with result_placeholder.container():
            st.header("🏁 Forensic Analysis Report")
            
            # Layout: Comparison
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original / Extracted Image")
                st.image(report["original_image"], use_container_width=True)
            with col2:
                st.subheader("ELA (Error Level Analysis)")
                st.image(report["ela_image"], use_container_width=True)
                st.caption("Bright/White clusters often indicate localized editing (forgery).")

            # Red Flags Section
            st.divider()
            if report["red_flags"]:
                st.error("🚨 **RED FLAGS DETECTED**")
                for flag in report["red_flags"]:
                    st.markdown(f"- {flag}")
            else:
                st.success("✅ No significant forgery markers detected in metadata or ELA baseline.")

    except Exception as e:
        scanner_placeholder.empty()
        st.error(f"❌ Analysis Failed: {str(e)}")

else:
    st.info("Please upload a document or image to begin forensic analysis.")
