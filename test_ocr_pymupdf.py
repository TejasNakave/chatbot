#!/usr/bin/env python3
"""
Alternative OCR approach using PyMuPDF (fitz) for PDF to image conversion
This avoids the need for separate Poppler installation
"""

import os

# Try to install pymupdf which can handle PDF to image conversion internally
def install_pymupdf():
    """Install PyMuPDF for better PDF handling"""
    try:
        import subprocess
        import sys
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "pymupdf"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ PyMuPDF installed successfully")
            return True
        else:
            print(f"❌ Failed to install PyMuPDF: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

# Try imports
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    print("📦 Installing PyMuPDF for better PDF handling...")
    if install_pymupdf():
        try:
            import fitz
            PYMUPDF_AVAILABLE = True
        except ImportError:
            PYMUPDF_AVAILABLE = False
    else:
        PYMUPDF_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    import io
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

def extract_text_with_pymupdf_ocr(pdf_path: str, max_pages: int = 5) -> str:
    """
    Extract text from scanned PDF using PyMuPDF + OCR
    """
    if not PYMUPDF_AVAILABLE or not OCR_AVAILABLE:
        return "OCR dependencies not available"
    
    # Set up Tesseract path
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    tesseract_found = False
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            tesseract_found = True
            break
    
    if not tesseract_found:
        return "Tesseract OCR not found"
    
    try:
        print(f"🔍 Running OCR on {os.path.basename(pdf_path)} using PyMuPDF...")
        
        # Open PDF with PyMuPDF
        doc = fitz.open(pdf_path)
        extracted_text = ""
        successful_pages = 0
        
        total_pages = min(len(doc), max_pages)
        print(f"📄 Processing {total_pages} pages with OCR...")
        
        for page_num in range(total_pages):
            try:
                print(f"   🔍 Processing page {page_num + 1}/{total_pages}...")
                
                # Get page
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Run OCR
                text = pytesseract.image_to_string(img, lang='eng')
                
                if text.strip():
                    extracted_text += f"\n=== Page {page_num + 1} ===\n{text.strip()}\n"
                    successful_pages += 1
                    print(f"   ✅ Page {page_num + 1}: {len(text.strip())} characters extracted")
                else:
                    print(f"   ⚠️  Page {page_num + 1}: No text detected")
                    
            except Exception as e:
                print(f"   ❌ Page {page_num + 1}: Error - {str(e)}")
        
        doc.close()
        
        if extracted_text.strip():
            full_text = f"""OCR-Extracted Text from {os.path.basename(pdf_path)}
Source: Scanned PDF processed with PyMuPDF + Tesseract OCR
Pages processed: {successful_pages}/{total_pages}
Total pages in document: {len(fitz.open(pdf_path))}

{extracted_text}

Note: This is a sample extraction from the first {total_pages} pages. 
The document contains {len(fitz.open(pdf_path))} total pages.
For full extraction, increase max_pages parameter."""
            
            print(f"✅ OCR completed: {len(full_text)} characters from {successful_pages} pages")
            return full_text
        else:
            return f"""OCR Processing Report for {os.path.basename(pdf_path)}
Status: No readable text found in first {total_pages} pages
Possible reasons: Poor image quality, non-text content, or language not supported

This appears to be a scanned document that cannot be reliably converted to text."""
            
    except Exception as e:
        error_msg = f"OCR processing failed for {os.path.basename(pdf_path)}: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def test_ocr_on_scanned_pdf():
    """Test OCR on the problematic PDF"""
    pdf_path = "data/In Communion With Consciousness.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return
    
    print("🚀 Testing OCR on Scanned PDF")
    print("=" * 50)
    
    if PYMUPDF_AVAILABLE and OCR_AVAILABLE:
        result = extract_text_with_pymupdf_ocr(pdf_path, max_pages=3)
        
        print(f"\n📊 OCR Results:")
        print(f"Content length: {len(result)} characters")
        print(f"\nFirst 500 characters:")
        print("-" * 30)
        print(result[:500])
        print("-" * 30)
        
        if len(result) > 500:
            print(f"\n✅ OCR successful! Extracted {len(result)} characters")
            print("This PDF can now be searched and queried by your chatbot!")
        else:
            print(f"\n⚠️  Limited OCR results. This may be a complex scanned document.")
    else:
        print("❌ OCR dependencies not available")
        print("Missing:")
        if not PYMUPDF_AVAILABLE:
            print("- PyMuPDF (pip install pymupdf)")
        if not OCR_AVAILABLE:
            print("- Tesseract OCR + pytesseract")

if __name__ == "__main__":
    test_ocr_on_scanned_pdf()
