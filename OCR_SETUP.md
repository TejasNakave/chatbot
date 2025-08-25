# OCR Setup Instructions for Scanned PDFs

## Quick Setup for Windows

1. **Install Python packages:**
```bash
pip install pytesseract pillow pdf2image
```

2. **Install Tesseract OCR:**
```bash
# Using winget (recommended)
winget install UB-Mannheim.TesseractOCR

# Or download manually from:
# https://github.com/UB-Mannheim/tesseract/wiki
```

3. **Install Poppler for PDF conversion:**
```bash
# Download from: https://blog.alivate.com.au/poppler-windows/
# Extract to C:\poppler and add C:\poppler\bin to your PATH
```

4. **Test OCR setup:**
```bash
python ocr_pdf_loader.py
```

## Alternative: Use Google Drive or Online OCR

1. Upload your PDF to Google Drive
2. Open with Google Docs (it will OCR automatically)
3. Download as a Word document or text file
4. Place the text file in your data/ folder

## Why This Happens

- **Scanned PDFs** = Photos of text pages (like taking pictures of a book)
- **Text PDFs** = Actual digital text (like typing in Word)
- **Your PDF**: 215 pages of scanned images, 38MB size
- **OCR**: Converts images of text back into searchable text

## Current Status

✅ Your chatbot works perfectly with text-based PDFs
✅ Your "testing.pdf" works great (39K characters extracted)
❌ "In Communion With Consciousness.pdf" needs OCR (scanned images only)

The system now properly detects and labels scanned PDFs so you know which ones need OCR processing.
