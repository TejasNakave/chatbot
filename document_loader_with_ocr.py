#!/usr/bin/env python3
"""
Enhanced Document Loader with OCR Support
Extracts text from both regular PDFs and scanned images using OCR
"""

import os
import glob
from typing import List, Dict
import PyPDF2
from docx import Document

# OCR imports (with fallback if not available)
try:
    import pytesseract
    import pdf2image
    from PIL import Image
    OCR_AVAILABLE = True
    print("✅ OCR capabilities available")
except ImportError as e:
    OCR_AVAILABLE = False
    print(f"⚠️  OCR not available: {e}")

def detect_tesseract_path():
    """Auto-detect Tesseract installation path on Windows"""
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
        "tesseract"  # If in PATH
    ]
    
    for path in possible_paths:
        if path == "tesseract" or os.path.exists(path):
            try:
                if path != "tesseract":
                    pytesseract.pytesseract.tesseract_cmd = path
                # Test if it works
                pytesseract.get_tesseract_version()
                print(f"✅ Tesseract found at: {path}")
                return True
            except:
                continue
    
    print("❌ Tesseract not found. Please install it:")
    print("   Download: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Or run: winget install UB-Mannheim.TesseractOCR")
    return False

def extract_text_with_ocr(pdf_path: str, max_pages: int = 10) -> str:
    """
    Extract text from scanned PDF using OCR
    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum pages to process (OCR is slow)
    Returns:
        Extracted text string
    """
    if not OCR_AVAILABLE:
        return f"OCR not available for {os.path.basename(pdf_path)}. Install: pip install pytesseract pillow pdf2image"
    
    if not detect_tesseract_path():
        return f"Tesseract OCR not installed for {os.path.basename(pdf_path)}"
    
    try:
        print(f"🔍 Running OCR on {os.path.basename(pdf_path)}...")
        print(f"📄 Processing first {max_pages} pages (OCR is resource-intensive)")
        
        # Convert PDF pages to images
        try:
            pages = pdf2image.convert_from_path(
                pdf_path, 
                first_page=1, 
                last_page=max_pages,
                dpi=200,  # Good balance of quality vs speed
                fmt='jpeg'
            )
        except Exception as e:
            return f"Failed to convert PDF to images: {str(e)}\nMay need to install Poppler: https://blog.alivate.com.au/poppler-windows/"
        
        extracted_text = ""
        successful_pages = 0
        
        for i, page in enumerate(pages, 1):
            try:
                print(f"   🔍 OCR processing page {i}/{len(pages)}...")
                
                # Use OCR to extract text
                text = pytesseract.image_to_string(page, lang='eng')
                
                if text.strip():
                    extracted_text += f"\n=== Page {i} ===\n{text.strip()}\n"
                    successful_pages += 1
                    print(f"   ✅ Page {i}: {len(text.strip())} characters extracted")
                else:
                    print(f"   ⚠️  Page {i}: No text detected")
                    
            except Exception as e:
                print(f"   ❌ Page {i}: OCR failed - {str(e)}")
        
        if extracted_text.strip():
            # Add metadata
            full_text = f"""OCR-Extracted Text from {os.path.basename(pdf_path)}
Source: Scanned PDF processed with OCR
Pages processed: {successful_pages}/{len(pages)}
Extraction date: {os.path.getctime(pdf_path)}

{extracted_text}

Note: This content was extracted using OCR. Text accuracy may vary depending on image quality."""
            
            print(f"✅ OCR completed: {len(full_text)} characters from {successful_pages} pages")
            return full_text
        else:
            return f"""OCR Processing Report for {os.path.basename(pdf_path)}
Status: No readable text found
Pages processed: {len(pages)}
Possible reasons: Poor image quality, non-text content, unsupported language

This document appears to contain images or text that cannot be reliably extracted."""
            
    except Exception as e:
        error_msg = f"OCR processing failed for {os.path.basename(pdf_path)}: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def load_pdf_with_ocr_fallback(file_path: str) -> str:
    """
    Enhanced PDF loader that tries regular extraction first, then OCR
    """
    file_name = os.path.basename(file_path)
    print(f"📄 Loading PDF: {file_name}")
    
    # Try regular text extraction first
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"   📊 PDF has {len(pdf_reader.pages)} pages")
            
            # Check first few pages for text
            pages_with_text = 0
            for i, page in enumerate(pdf_reader.pages[:5]):  # Check first 5 pages
                page_text = page.extract_text()
                if page_text.strip():
                    text += page_text + "\n"
                    pages_with_text += 1
            
            # If we found text in regular extraction, continue with all pages
            if pages_with_text > 0:
                print(f"   ✅ Text-based PDF detected, extracting all pages...")
                for page in pdf_reader.pages[5:]:  # Process remaining pages
                    text += page.extract_text() + "\n"
                
                print(f"   ✅ Regular extraction: {len(text)} characters from {len(pdf_reader.pages)} pages")
                return text
            else:
                print(f"   ⚠️  No extractable text found, trying OCR...")
                return extract_text_with_ocr(file_path, max_pages=5)  # Process first 5 pages with OCR
                
    except Exception as e:
        print(f"   ❌ PDF processing failed: {str(e)}")
        return f"Failed to process PDF {file_name}: {str(e)}"

def load_documents_from_folder_with_ocr(folder_path: str = "data/") -> List[Dict[str, str]]:
    """
    Enhanced document loader with OCR support for scanned PDFs
    """
    documents = []
    
    if not os.path.exists(folder_path):
        print(f"Warning: Folder '{folder_path}' does not exist.")
        return documents
    
    print(f"📂 Loading documents from: {os.path.abspath(folder_path)}")
    if OCR_AVAILABLE:
        print("🔍 OCR support enabled for scanned PDFs")
    else:
        print("⚠️  OCR not available - scanned PDFs will have limited content")
    
    # Get all supported file types
    file_patterns = [
        os.path.join(folder_path, "*.pdf"),
        os.path.join(folder_path, "*.docx"), 
        os.path.join(folder_path, "*.txt")
    ]
    
    all_files = []
    for pattern in file_patterns:
        files = glob.glob(pattern)
        all_files.extend(files)
    
    print(f"📋 Found {len(all_files)} files: {[os.path.basename(f) for f in all_files]}")
    
    for file_path in all_files:
        try:
            content = ""
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower()
            
            print(f"\n🔄 Processing: {file_name}")
            
            if file_ext == ".pdf":
                content = load_pdf_with_ocr_fallback(file_path)
            elif file_ext == ".docx":
                content = load_docx(file_path)
            elif file_ext == ".txt":
                content = load_txt(file_path)
            
            if content.strip():
                documents.append({
                    "file_name": file_name,
                    "file_path": file_path,
                    "content": content,
                    "file_type": file_ext
                })
                print(f"✅ Successfully loaded: {file_name} ({len(content):,} characters)")
            else:
                # Still add with placeholder
                documents.append({
                    "file_name": file_name,
                    "file_path": file_path,
                    "content": f"Document could not be processed: {file_name}",
                    "file_type": file_ext
                })
                print(f"⚠️  Added with placeholder: {file_name}")
                
        except Exception as e:
            print(f"❌ Error loading {file_path}: {str(e)}")
            # Add error document
            documents.append({
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                "content": f"Error loading {os.path.basename(file_path)}: {str(e)}",
                "file_type": os.path.splitext(file_path)[1].lower()
            })
    
    print(f"\n📊 Loading complete: {len(documents)} documents processed")
    return documents

def load_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def load_txt(file_path: str) -> str:
    """Load text from TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error reading TXT: {str(e)}")

if __name__ == "__main__":
    # Test the enhanced loader
    print("🚀 Testing Enhanced Document Loader with OCR")
    print("=" * 60)
    
    docs = load_documents_from_folder_with_ocr()
    
    print(f"\n📋 Summary:")
    for doc in docs:
        print(f"📄 {doc['file_name']}: {len(doc['content']):,} characters")
        if "OCR-Extracted" in doc['content']:
            print(f"   🔍 Processed with OCR")
        elif "scanned images" in doc['content']:
            print(f"   ⚠️  Scanned PDF - needs OCR setup")
        else:
            print(f"   ✅ Regular text extraction")
