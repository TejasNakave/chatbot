#!/usr/bin/env python3
"""
Cache Builder for OCR Results
Pre-processes documents and caches OCR results for instant loading
"""

import os
from document_loader import load_documents_from_folder

def build_cache():
    """Pre-process all documents and build cache"""
    print("🚀 Building document cache...")
    print("=" * 50)
    
    # This will process all documents and save OCR results to cache
    documents = load_documents_from_folder()
    
    print("\n" + "=" * 50)
    print("✅ Cache building complete!")
    print(f"📚 Cached {len(documents)} documents")
    
    for doc in documents:
        print(f"   📄 {doc['file_name']}: {len(doc['content']):,} characters")
    
    print("\n🚀 Your Streamlit app will now load instantly!")
    print("💡 Run: streamlit run streamlit_app.py")

if __name__ == "__main__":
    build_cache()
