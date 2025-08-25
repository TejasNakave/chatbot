#!/usr/bin/env python3
"""
OCR-Enhanced PDF Loader
Adds OCR capability to extract text from scanned PDFs using Tesseract
"""

import os
import PyPDF2
from PIL import Image
import io
try:
    import pytesseract
    import pdf2image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def install_ocr_dependencies():
    """Instructions for installing OCR dependencies"""
    print("📦 To enable OCR for scanned PDFs, install these dependencies:")
    print()
    print("1. Install Python packages:")
    print("   pip install pytesseract pillow pdf2image")
    print()
    print("2. Install Tesseract OCR:")
    print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Or use: winget install UB-Mannheim.TesseractOCR")
    print()
    print("3. Install Poppler (for pdf2image):")
    print("   Windows: Download from https://blog.alivate.com.au/poppler-windows/")
    print("   Or use conda: conda install -c conda-forge poppler")
    print()

def extract_text_with_ocr(pdf_path, max_pages=5):
    """
    Extract text from scanned PDF using OCR
    Args:
        pdf_path: Path to the PDF file
        max_pages: Maximum pages to process (OCR is slow)
    """
    if not OCR_AVAILABLE:
        print("❌ OCR dependencies not installed")
        install_ocr_dependencies()
        return ""
    
    try:
        print(f"🔍 Running OCR on {os.path.basename(pdf_path)}...")
        print(f"⚠️  Processing first {max_pages} pages only (OCR is slow)")
        
        # Convert PDF pages to images
        pages = pdf2image.convert_from_path(pdf_path, first_page=1, last_page=max_pages)
        
        extracted_text = ""
        for i, page in enumerate(pages, 1):
            print(f"   Processing page {i}/{len(pages)}...")
            
            # Use OCR to extract text
            text = pytesseract.image_to_string(page)
            
            if text.strip():
                extracted_text += f"\n--- Page {i} ---\n{text}\n"
                print(f"   ✅ Page {i}: {len(text)} characters extracted")
            else:
                print(f"   ⚠️  Page {i}: No text found")
        
        if extracted_text:
            # Add metadata
            full_text = f"""OCR-Extracted Content from {os.path.basename(pdf_path)}
(First {max_pages} pages only - scanned PDF)

{extracted_text}

Note: This content was extracted using OCR from a scanned PDF. 
Text accuracy may vary. For complete content, consider using the full OCR processing."""
            
            print(f"✅ OCR completed: {len(full_text)} characters extracted")
            return full_text
        else:
            return f"OCR processed {max_pages} pages from {os.path.basename(pdf_path)} but no readable text was found."
            
    except Exception as e:
        print(f"❌ OCR failed: {str(e)}")
        return f"OCR processing failed for {os.path.basename(pdf_path)}: {str(e)}"

def enhanced_load_pdf(file_path):
    """
    Enhanced PDF loader that tries regular extraction first, then OCR
    """
    print(f"📄 Loading PDF: {os.path.basename(file_path)}")
    
    # Try regular text extraction first
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text.strip():
                    text += page_text + "\n"
            
            if text.strip():
                print(f"✅ Regular extraction successful: {len(text)} characters")
                return text
            else:
                print("⚠️  No text found with regular extraction, trying OCR...")
                return extract_text_with_ocr(file_path, max_pages=3)  # Process first 3 pages
                
    except Exception as e:
        print(f"❌ PDF processing failed: {str(e)}")
        return f"Failed to process PDF {os.path.basename(file_path)}: {str(e)}"

if __name__ == "__main__":
    # Test with your problematic PDF
    pdf_path = "data/In Communion With Consciousness.pdf"
    
    if OCR_AVAILABLE:
        print("✅ OCR dependencies available")
        result = enhanced_load_pdf(pdf_path)
        print(f"\nResult preview:\n{result[:500]}...")
    else:
        print("❌ OCR dependencies not available")
        install_ocr_dependencies()
