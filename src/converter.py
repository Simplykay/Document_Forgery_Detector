import numpy as np
import cv2
from pdf2image import convert_from_bytes
from docx import Document
import io
import os
import shutil
from PIL import Image

class DocumentProcessor:
    """Class to handle conversion of various document formats to images for analysis."""

    def _get_poppler_path(self):
        """Attempts to locate the poppler bin directory on Windows."""
        if os.name != 'nt':
            return None
            
        # 1. Check if pdftoppm is in PATH and get its directory
        pdftoppm_path = shutil.which("pdftoppm")
        if pdftoppm_path:
            return os.path.dirname(pdftoppm_path)
            
        return None

    def process_pdf(self, file_bytes):
        """
        Convert the first page of a PDF to a Numpy image array.
        
        Args:
            file_bytes (bytes): The bytes content of the PDF file.
            
        Returns:
            numpy.ndarray: The converted image in BGR format (OpenCV compatible).
        """
        try:
            # Detect poppler path on Windows
            poppler_path = self._get_poppler_path()
            
            # Convert PDF bytes to a list of PIL images
            pages = convert_from_bytes(
                file_bytes, 
                dpi=300, 
                first_page=1, 
                last_page=1,
                poppler_path=poppler_path
            )
            
            if not pages:
                raise ValueError("No pages found in PDF.")
            
            # Convert PIL image to Numpy array and then to BGR for OpenCV
            pil_image = pages[0]
            numpy_image = np.array(pil_image)
            
            # Convert RGB to BGR if it's a color image
            if len(numpy_image.shape) == 3:
                bgr_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
                return bgr_image
            
            return numpy_image

        except Exception as e:
            raise RuntimeError(f"Failed to process PDF: {str(e)}")

    def process_word(self, file_bytes):
        """
        Extract the largest embedded image from a .docx file.
        
        Args:
            file_bytes (bytes): The bytes content of the Word file.
            
        Returns:
            numpy.ndarray: The largest image found in BGR format.
        """
        try:
            doc = Document(io.BytesIO(file_bytes))
            largest_image = None
            max_size = 0
            
            # doc.inline_shapes contains embedded images
            for shape in doc.inline_shapes:
                if shape._inline.graphic.graphicData.pic is not None:
                    # Get the image bytes
                    image_part = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
                    image_blob = doc.part.related_parts[image_part].blob
                    
                    # Open with PIL to check size
                    img = Image.open(io.BytesIO(image_blob))
                    width, height = img.size
                    size = width * height
                    
                    if size > max_size:
                        max_size = size
                        # Convert to OpenCV format (BGR)
                        numpy_image = np.array(img)
                        if len(numpy_image.shape) == 3:
                            largest_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
                        else:
                            largest_image = numpy_image
            
            if largest_image is None:
                raise ValueError("No images found in Word document.")
            
            return largest_image

        except Exception as e:
            raise RuntimeError(f"Failed to process Word document: {str(e)}")
