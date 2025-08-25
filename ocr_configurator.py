#!/usr/bin/env python3
"""
Configurable OCR Document Processor
Allows you to process different numbers of pages based on your needs
"""

import os
from document_loader import load_documents_from_folder, extract_text_with_ocr

def process_pdf_with_custom_pages(pdf_path, max_pages):
    """Process a specific PDF with custom page limit"""
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return None
    
    print(f"🔍 Processing {os.path.basename(pdf_path)} with OCR")
    print(f"📄 Page limit: {max_pages} pages")
    print("=" * 60)
    
    # Estimate processing time
    estimated_minutes = max_pages * 3 / 60  # 3 seconds per page average
    print(f"⏱️  Estimated processing time: {estimated_minutes:.1f} minutes")
    
    # Ask for confirmation if it's a lot of pages
    if max_pages > 50:
        response = input(f"\n⚠️  Processing {max_pages} pages will take approximately {estimated_minutes:.1f} minutes. Continue? (y/n): ")
        if response.lower() != 'y':
            print("❌ Processing cancelled")
            return None
    
    try:
        result = extract_text_with_ocr(pdf_path, max_pages)
        
        print(f"\n📊 OCR Results:")
        print(f"   Content length: {len(result):,} characters")
        print(f"   Average per page: {len(result) // max_pages:,} characters")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def get_processing_options():
    """Show different processing options"""
    print("🎯 OCR Processing Options for Large PDFs:")
    print()
    print("1. 📄 Quick Sample (10 pages) - 30 seconds")
    print("   Good for: Testing, getting main topics")
    print()
    print("2. 📖 Medium Sample (50 pages) - 2.5 minutes") 
    print("   Good for: Substantial content, chapter summaries")
    print()
    print("3. 📚 Large Sample (100 pages) - 5 minutes")
    print("   Good for: Comprehensive analysis, research")
    print()
    print("4. 📜 Full Document (215 pages) - 10-15 minutes")
    print("   Good for: Complete searchable archive")
    print()
    print("5. 🎛️  Custom page range")
    print("   Good for: Specific chapters or sections")
    print()

def interactive_ocr_processor():
    """Interactive OCR processor with options"""
    pdf_path = "data/In Communion With Consciousness.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print("🤖 Interactive OCR Document Processor")
    print("=" * 50)
    
    get_processing_options()
    
    try:
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            max_pages = 10
        elif choice == "2":
            max_pages = 50
        elif choice == "3":
            max_pages = 100
        elif choice == "4":
            max_pages = 215
        elif choice == "5":
            try:
                max_pages = int(input("Enter number of pages to process (1-215): "))
                if max_pages < 1 or max_pages > 215:
                    print("❌ Invalid page number. Using 10 pages.")
                    max_pages = 10
            except ValueError:
                print("❌ Invalid input. Using 10 pages.")
                max_pages = 10
        else:
            print("❌ Invalid choice. Using 10 pages.")
            max_pages = 10
        
        print(f"\n🚀 Processing {max_pages} pages...")
        result = process_pdf_with_custom_pages(pdf_path, max_pages)
        
        if result:
            # Save result to file
            output_file = f"ocr_output_{max_pages}_pages.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            print(f"\n✅ OCR Complete!")
            print(f"📁 Result saved to: {output_file}")
            print(f"📊 Total characters: {len(result):,}")
            
            # Show preview
            print(f"\n📖 Content Preview (first 500 characters):")
            print("-" * 50)
            print(result[:500])
            print("-" * 50)
            
            # Option to update document loader
            update_choice = input(f"\n🔄 Update document loader to use {max_pages} pages for this PDF? (y/n): ")
            if update_choice.lower() == 'y':
                update_document_loader_pages(max_pages)
                print("✅ Document loader updated!")
        
    except KeyboardInterrupt:
        print("\n❌ Processing interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def update_document_loader_pages(new_max_pages):
    """Update the document loader to use more pages"""
    # Read current file
    with open('document_loader.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the max_pages value
    old_line = "return extract_text_with_ocr(file_path, max_pages=10)"
    new_line = f"return extract_text_with_ocr(file_path, max_pages={new_max_pages})"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Write back
        with open('document_loader.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated document_loader.py to process {new_max_pages} pages")
    else:
        print("⚠️  Could not automatically update document_loader.py")

def estimate_full_processing():
    """Show estimates for full document processing"""
    print("📊 Full Document Processing Estimates:")
    print("=" * 40)
    print(f"📄 Total pages: 215")
    print(f"⏱️  Estimated time: 10-15 minutes")
    print(f"💾 Estimated text: ~460,000 characters") 
    print(f"📏 Estimated size: ~450 KB of text")
    print(f"🧠 Memory usage: ~500 MB during processing")
    print()
    print("💡 Recommendation:")
    print("  - Start with 50 pages to test performance")
    print("  - Process full document during break/lunch")
    print("  - Run overnight for multiple large PDFs")

if __name__ == "__main__":
    print("🔍 Current Status: Processing 10 pages from 215-page PDF")
    print()
    
    # Show estimates
    estimate_full_processing()
    print()
    
    # Ask what user wants to do
    print("What would you like to do?")
    print("1. 🚀 Start interactive OCR processor")
    print("2. 📊 Just show processing estimates")
    print("3. 🔧 Quick update to 50 pages")
    
    choice = input("\nChoose (1-3): ").strip()
    
    if choice == "1":
        interactive_ocr_processor()
    elif choice == "3":
        update_document_loader_pages(50)
        print("✅ Updated to process 50 pages. Run document refresh in Streamlit!")
    else:
        print("📋 Processing estimates shown above.")
