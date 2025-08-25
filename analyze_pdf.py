#!/usr/bin/env python3
"""
Advanced PDF Analysis Tool
Analyzes PDF structure to understand why text extraction fails
"""

import PyPDF2
import os

def analyze_pdf_structure(file_path):
    """Analyze PDF structure in detail"""
    print(f"🔍 Analyzing PDF: {os.path.basename(file_path)}")
    print("=" * 60)
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Basic info
            print(f"📄 Basic Information:")
            print(f"   Pages: {len(pdf_reader.pages)}")
            print(f"   Encrypted: {pdf_reader.is_encrypted}")
            print(f"   File size: {os.path.getsize(file_path):,} bytes")
            
            # Metadata
            if pdf_reader.metadata:
                print(f"\n📋 Metadata:")
                for key, value in pdf_reader.metadata.items():
                    print(f"   {key}: {value}")
            
            # Analyze first few pages in detail
            print(f"\n🔍 Page Analysis (first 5 pages):")
            for i in range(min(5, len(pdf_reader.pages))):
                page = pdf_reader.pages[i]
                text = page.extract_text()
                
                # Check for images/objects
                page_dict = page.get('/Resources')
                has_xobject = False
                has_font = False
                
                if page_dict and '/XObject' in page_dict:
                    has_xobject = True
                if page_dict and '/Font' in page_dict:
                    has_font = True
                
                print(f"   Page {i+1}:")
                print(f"     Text length: {len(text)}")
                print(f"     Has XObjects (images): {has_xobject}")
                print(f"     Has Fonts: {has_font}")
                if text.strip():
                    print(f"     Sample text: {repr(text[:50])}")
                else:
                    print(f"     Sample text: [NO TEXT FOUND]")
            
            # Overall analysis
            total_text_chars = 0
            pages_with_text = 0
            pages_with_images = 0
            
            print(f"\n📊 Full Document Analysis:")
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                total_text_chars += len(text)
                if text.strip():
                    pages_with_text += 1
                
                page_dict = page.get('/Resources')
                if page_dict and '/XObject' in page_dict:
                    pages_with_images += 1
                
                # Show progress for large PDFs
                if (i + 1) % 50 == 0:
                    print(f"     Processed {i+1}/{len(pdf_reader.pages)} pages...")
            
            print(f"   Total text characters: {total_text_chars:,}")
            print(f"   Pages with text: {pages_with_text}/{len(pdf_reader.pages)}")
            print(f"   Pages with images: {pages_with_images}/{len(pdf_reader.pages)}")
            
            # Diagnosis
            print(f"\n🏥 Diagnosis:")
            if total_text_chars == 0:
                print("   ❌ SCANNED PDF - Contains only images, no searchable text")
                print("   💡 Solution: Use OCR (Optical Character Recognition)")
            elif pages_with_text < len(pdf_reader.pages) * 0.1:
                print("   ⚠️  MOSTLY SCANNED - Very little searchable text")
                print("   💡 Solution: Mixed document, consider OCR for missing pages")
            else:
                print("   ✅ TEXT-BASED PDF - Should work normally")
                print("   🤔 Issue: Possible encoding or extraction problem")
            
    except Exception as e:
        print(f"❌ Error analyzing PDF: {str(e)}")

if __name__ == "__main__":
    pdf_path = "data/In Communion With Consciousness.pdf"
    analyze_pdf_structure(pdf_path)
