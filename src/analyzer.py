import cv2
import numpy as np
import os
from PIL import Image
from PIL.ExifTags import TAGS

class ForgeryDetector:
    """Class to detect digital forgeries in documents."""

    def perform_ela(self, image_path, quality=90):
        """
        Perform Error Level Analysis (ELA) on an image.
        
        Args:
            image_path (str): Path to the input image.
            quality (int): JPEG quality level for resaving (default 90).
            
        Returns:
            numpy.ndarray: The ELA processed image with enhanced brightness.
        """
        # Load the original image
        original = cv2.imread(image_path)
        if original is None:
            raise ValueError(f"Could not read image at {image_path}")

        temp_filename = "temp_resaved.jpg"
        
        try:
            # Resave the image at the specified quality
            cv2.imwrite(temp_filename, original, [cv2.IMWRITE_JPEG_QUALITY, quality])
            
            # Load the resaved image
            resaved = cv2.imread(temp_filename)
            
            # Compute the absolute difference between the original and resaved image
            # ELA highlights areas where the local compression level differs
            ela_image = cv2.absdiff(original, resaved)
            
            # Enhance brightness so it's visible to the human eye
            # We use a multiplier (alpha) to boost the low-intensity differences
            # A common factor for ELA visibility is around 15-30
            ela_image = cv2.convertScaleAbs(ela_image, alpha=20, beta=0)
            
            return ela_image
            
        finally:
            # Ensure the temporary file is cleaned up
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def extract_metadata(self, image_path):
        """
        Extract EXIF metadata from an image and look for editing software markers.
        
        Args:
            image_path (str): Path to the input image.
            
        Returns:
            dict: Dictionary of relevant EXIF tags and their values.
        """
        metadata = {}
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # Specifically look for 'Software' or 'ModifyDate'
                    if tag in ['Software', 'DateTime', 'DateTimeDigitized', 'DateTimeOriginal']:
                        metadata[tag] = value
            
            # Additional check for image info (some software markers might be here)
            if 'software' in img.info:
                metadata['Software (Info)'] = img.info['software']
                
        except Exception as e:
            metadata['Error'] = f"Failed to extract metadata: {str(e)}"
            
        return metadata

if __name__ == "__main__":
    # Simple test stub
    print("ForgeryDetector class defined.")
