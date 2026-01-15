import cv2
import numpy as np
import os
import sys

# Add src to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analyzer import ForgeryDetector

def create_dummy_image(path):
    # Create a 400x400 white image
    img = np.ones((400, 400, 3), dtype=np.uint8) * 255
    # Add some text to make it look like a document
    cv2.putText(img, "DUMMY DOCUMENT", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    # Save as JPEG
    cv2.imwrite(path, img)
    print(f"Created dummy image at {path}")

def test_ela():
    detector = ForgeryDetector()
    test_img_path = "test_dummy.jpg"
    
    try:
        create_dummy_image(test_img_path)
        
        print("Running ELA...")
        ela_img = detector.perform_ela(test_img_path)
        
        if ela_img is not None and ela_img.shape == (400, 400, 3):
            print("SUCCESS: ELA output generated correctly.")
            return True
        else:
            print("FAILURE: ELA output is invalid.")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    finally:
        if os.path.exists(test_img_path):
            os.remove(test_img_path)

if __name__ == "__main__":
    success = test_ela()
    sys.exit(0 if success else 1)
