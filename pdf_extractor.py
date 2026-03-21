"""
PDF Text Extraction Utility
Handles both digital and scanned PDFs
"""

import io
from typing import Optional

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text_from_pdf(uploaded_file) -> Optional[str]:
    """
    Extract text from uploaded PDF
    Tries digital extraction first, falls back to OCR if needed
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        Extracted text or None
    """
    try:
        # Reset file pointer
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()
        
        # Try digital extraction first
        text = extract_digital_pdf(pdf_bytes)
        
        if text and len(text.strip()) > 50:
            return text
        
        # If digital extraction fails or returns little text, try OCR
        if OCR_AVAILABLE:
            text = extract_scanned_pdf(pdf_bytes)
            return text
        else:
            return text if text else "Could not extract text. OCR not available."
    
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"


def extract_digital_pdf(pdf_bytes: bytes) -> str:
    """Extract text from digital PDF using PyPDF2"""
    if not PYPDF2_AVAILABLE:
        return ""
    
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    except Exception as e:
        return ""


def extract_scanned_pdf(pdf_bytes: bytes) -> str:
    """Extract text from scanned PDF using OCR"""
    if not OCR_AVAILABLE:
        return "OCR not available. Please install pytesseract and Pillow."
    
    try:
        # This is a simplified version
        # In production, use pdf2image to convert pages to images
        # then run OCR on each image
        return "OCR extraction not fully implemented. Please use digital PDF or paste text manually."
    
    except Exception as e:
        return f"OCR error: {str(e)}"


def check_dependencies():
    """Check which PDF processing libraries are available"""
    deps = {
        'pypdf2': PYPDF2_AVAILABLE,
        'ocr': OCR_AVAILABLE
    }
    return deps
