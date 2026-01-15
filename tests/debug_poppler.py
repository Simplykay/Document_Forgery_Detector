import shutil
import subprocess
import os
import sys
from pdf2image import convert_from_bytes

def check_poppler():
    print(f"OS: {os.name}")
    pdftoppm = shutil.which("pdftoppm")
    pdfinfo = shutil.which("pdfinfo")
    
    print(f"pdftoppm path: {pdftoppm}")
    print(f"pdfinfo path: {pdfinfo}")
    
    if pdftoppm:
        try:
            res = subprocess.run([pdftoppm, "-h"], capture_output=True, text=True)
            print("pdftoppm -h output (first line):", res.stdout.split('\n')[0])
        except Exception as e:
            print(f"Error running pdftoppm: {e}")

    dummy_pdf = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 20 >>\nstream\nBT /F1 12 Tf ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000213 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n283\n%%EOF"
    
    print("\nAttempting convert_from_bytes...")
    try:
        poppler_path = os.path.dirname(pdftoppm) if pdftoppm else None
        print(f"Using poppler_path: {poppler_path}")
        images = convert_from_bytes(dummy_pdf, poppler_path=poppler_path)
        print(f"Success! Number of pages: {len(images)}")
    except Exception as e:
        print(f"Conversion failed: {e}")

if __name__ == "__main__":
    check_poppler()
