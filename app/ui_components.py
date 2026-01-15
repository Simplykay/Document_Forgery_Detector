import streamlit as st

def render_neon_scanner():
    """
    Renders a neon green scanning animation that can be overlaid on images.
    """
    st.markdown(
        """
        <style>
        @keyframes scan {
            0% { top: 0%; }
            50% { top: 100%; }
            100% { top: 0%; }
        }

        .scanner-container {
            position: relative;
            overflow: hidden;
            width: 100%;
        }

        .scanner-bar {
            position: absolute;
            height: 4px;
            width: 100%;
            background-color: #39ff14;
            box-shadow: 0px 0px 15px 5px #39ff14;
            z-index: 10;
            animation: scan 3s linear infinite;
            pointer-events: none;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

def inject_scanner_bar():
    """
    Injects the actual div for the scanner bar.
    This should be called within the container where the image is rendered.
    """
    st.markdown('<div class="scanner-bar"></div>', unsafe_allow_html=True)
