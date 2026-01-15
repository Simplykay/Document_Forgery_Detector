from pypdf import PdfReader
from docx import Document
import io
from datetime import datetime

def scan_metadata(file_object):
    """
    Scans PDF or Word file metadata for suspicious keywords and temporal anomalies.
    
    Args:
        file_object (BytesIO): The file-like object to scan.
        
    Returns:
        list: A list of 'Red Flags' found in the metadata.
    """
    red_flags = []
    suspicious_keywords = ['photoshop', 'gimp', 'i love pdf', 'modified']
    
    # Reset file pointer
    file_object.seek(0)
    file_bytes = file_object.read()
    file_object.seek(0)
    
    # Helper to check keywords
    def check_keywords(text, source):
        if not text:
            return
        text_lower = str(text).lower()
        for kw in suspicious_keywords:
            if kw in text_lower:
                red_flags.append(f"Suspicious keyword '{kw}' found in {source}: '{text}'")

    try:
        # Check if it's a PDF (starts with %PDF)
        if file_bytes.startswith(b'%PDF'):
            reader = PdfReader(file_object)
            meta = reader.metadata
            
            if meta:
                # Common PDF metadata tags
                tags_to_check = [('/Producer', 'Producer'), ('/Creator', 'Creator'), ('/Author', 'Author'), ('/Software', 'Software')]
                for tag, label in tags_to_check:
                    if tag in meta:
                        check_keywords(meta[tag], label)
                
                # Date anomaly check for PDF
                # PDF dates are often in format D:YYYYMMDDHHmmSSOHH'mm'
                creation_date = meta.get('/CreationDate')
                mod_date = meta.get('/ModDate')
                
                # Basic check for existence and common modifications
                if creation_date and mod_date:
                    # Very basic check: if they differ and mod is present, it's been edited
                    if creation_date != mod_date:
                        red_flags.append(f"Modification detected: Creation and Modification dates differ.")
        
        # Check if it's a DOCX (ZIP format starts with PK)
        elif file_bytes.startswith(b'PK'):
            doc = Document(file_object)
            props = doc.core_properties
            
            # Check core properties
            check_keywords(props.author, "Author")
            check_keywords(props.last_modified_by, "Last Modified By")
            
            # Temporal anomalies
            if props.created and props.modified:
                if props.created > props.modified:
                    red_flags.append(f"Temporal Anomaly: Creation date ({props.created}) is after Modification date ({props.modified}).")
                elif props.created != props.modified:
                    # In many forgery cases, any modification is a red flag if it's supposed to be an original scan
                    pass 

    except Exception as e:
        red_flags.append(f"Error scanning metadata: {str(e)}")
        
    return list(set(red_flags)) # Return unique flags
