# Document Forgery Detector 🛡️

A digital forensics tool designed to identify potential forgeries in documents (JPG/PNG) using Error Level Analysis (ELA) and Metadata Inspection.

## Features

- **Error Level Analysis (ELA)**: Detects compression artifacts and inconsistencies by resaving images at 90% quality and highlighting the differences.
- **Metadata Inspection**: Automatically extracts EXIF data to check for editing software markers (Photoshop, GIMP, Adobe, etc.).
- **Streamlit Dashboard**: A user-friendly web interface for uploading images and viewing forensic reports side-by-side.

## Project Structure

```text
├── app/
│   └── main.py          # Streamlit UI
├── src/
│   └── analyzer.py     # Core detection logic
├── tests/
│   └── test_ela.py     # Verification script
├── requirements.txt    # Project dependencies
└── setup_env.sh        # Environment setup script
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Simplykay/Document_Forgery_Detector.git
   cd Document_Forgery_Detector
   ```

2. **Setup virtual environment**:
   ```bash
   # On Windows (Git Bash) or Linux
   ./setup_env.sh
   ```
   *Alternatively, create a venv manually and install requirements:*
   ```bash
   python -m venv venv
   source venv/Scripts/activate # Windows
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app/main.py
```

Upload a document image to start the analysis!

## Verification

You can verify the core logic by running the test script:
```bash
python tests/test_ela.py
```

## Technologies Used

- **Python**
- **Streamlit** (UI)
- **OpenCV** (Image processing & ELA)
- **Pillow** (Metadata extraction)
- **NumPy**
- **Scikit-image**
