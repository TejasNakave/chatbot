#!/usr/bin/env python3
"""
Test script to verify document loading and refresh functionality
"""

import os
import sys
from document_loader import load_documents_from_folder

def test_document_loading():
    """Test the document loading functionality"""
    print("🔍 Testing Document Loading Functionality")
    print("=" * 50)
    
    # Test loading documents
    print("📂 Loading documents from data/ folder...")
    documents = load_documents_from_folder("data/")
    
    print(f"\n📊 Results:")
    print(f"  • Total documents loaded: {len(documents)}")
    
    if documents:
        print(f"\n📄 Document Details:")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc['file_name']}")
            print(f"     Type: {doc['file_type']}")
            print(f"     Content length: {len(doc['content']):,} characters")
            print(f"     Preview: {doc['content'][:100]}...")
            print()
    else:
        print("  ❌ No documents found!")
        
    return documents

def check_data_folder():
    """Check what files are in the data folder"""
    print("🔍 Checking data/ folder contents...")
    print("=" * 50)
    
    data_path = "data/"
    if not os.path.exists(data_path):
        print(f"❌ Data folder '{data_path}' does not exist!")
        return
        
    files = os.listdir(data_path)
    print(f"📁 Files in {data_path}:")
    
    if files:
        for file in files:
            file_path = os.path.join(data_path, file)
            size = os.path.getsize(file_path)
            print(f"  • {file} ({size:,} bytes)")
    else:
        print("  ❌ No files found in data folder!")
    
    print()
    return files

if __name__ == "__main__":
    print("🚀 Document Loading Test")
    print("=" * 50)
    
    # Check folder contents first
    files = check_data_folder()
    
    # Test document loading
    documents = test_document_loading()
    
    # Summary
    print("📋 Summary:")
    print(f"  • Files in folder: {len(files) if files else 0}")
    print(f"  • Documents loaded: {len(documents)}")
    
    if files and len(documents) != len(files):
        print("  ⚠️  Warning: Some files may not have loaded properly!")
    elif files and documents:
        print("  ✅ All files loaded successfully!")
    else:
        print("  ❌ No documents loaded!")
