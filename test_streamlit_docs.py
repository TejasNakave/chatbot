#!/usr/bin/env python3
"""
Quick test to verify all documents are loading properly for Streamlit
"""

from document_loader import load_documents_from_folder

def test_streamlit_documents():
    """Test what documents Streamlit will see"""
    print("🌐 Streamlit Document Loading Test")
    print("=" * 50)
    
    documents = load_documents_from_folder("data/")
    
    print(f"📚 Document Management")
    print(f"✅ Loaded {len(documents)} documents")
    print()
    print("📄 Document Library:")
    
    for doc in documents:
        file_type_icons = {
            'pdf': '📄',
            'docx': '📝', 
            'txt': '📃'
        }
        icon = file_type_icons.get(doc['file_type'].lower().replace('.', ''), '📄')
        print(f"{icon} {doc['file_name']}")
        
        # Show content type
        if "scanned images" in doc['content']:
            print(f"   ⚠️  Scanned PDF - no searchable text")
        else:
            print(f"   ✅ {len(doc['content']):,} characters extracted")
    
    return documents

if __name__ == "__main__":
    docs = test_streamlit_documents()
    print(f"\n🎉 Ready! Streamlit will show {len(docs)} documents in the sidebar.")
