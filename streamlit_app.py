import streamlit as st
import os
import sys
from datetime import datetime
from document_loader import load_documents_from_folder
from gemini_wrapper import GeminiAPIWrapper
from retriever import SimpleRetriever


@st.cache_data
def load_documents():
    """Load documents with caching."""
    return load_documents_from_folder("data/")


def refresh_documents():
    """Force refresh of documents by clearing cache."""
    # Clear all caches to ensure fresh reload
    load_documents.clear()
    st.cache_data.clear()
    st.cache_resource.clear()
    
    # Force reload documents from folder
    return load_documents_from_folder("data/")


@st.cache_resource
def initialize_components(documents):
    """Initialize chatbot components with caching."""
    try:
        retriever = SimpleRetriever(documents)
        gemini = GeminiAPIWrapper()
        return retriever, gemini, None
    except Exception as e:
        return None, None, str(e)


def format_chat_message(role, content, timestamp=None):
    """Format a chat message for display with intelligent structure and image support."""
    
    if role == "user":
        st.chat_message("user").write(content)
    else:
        # Check for images in the content
        import re
        
        # Extract image references
        image_pattern = r'\[IMAGE_\d+: ([^\]]+)\]'
        images = re.findall(image_pattern, content)
        
        # Debug: Print what we found
        if images:
            print(f"🖼️ Found {len(images)} images in content:")
            for i, img_path in enumerate(images):
                print(f"  Image {i}: {img_path}")
                print(f"  Exists: {os.path.exists(img_path)}")
        else:
            # Check if content contains image references at all
            if 'IMAGE_' in content:
                print(f"🔍 Content contains IMAGE_ but no matches found:")
                print(f"Pattern: {image_pattern}")
                # Show first 500 chars of content for debugging
                print(f"Content preview: {content[:500]}")
        
        # Remove image references from text content for processing
        clean_content = re.sub(image_pattern, '', content)
        clean_content = re.sub(r'\[IMAGES_AVAILABLE: \d+ images extracted\]', '', clean_content)
        clean_content = clean_content.strip()
        
        # Smart formatting based on content structure
        if isinstance(clean_content, str) and clean_content:
            # Check if content already has proper bullet structure
            has_bullets = bool(re.search(r'^\s*[-•*]\s+', clean_content, re.MULTILINE))
            has_numbers = bool(re.search(r'^\s*\d+\.\s+', clean_content, re.MULTILINE))
            
            if has_bullets or has_numbers:
                # Content already has proper bullets/numbers - display as is
                st.chat_message("assistant").markdown(clean_content)
            else:
                # Content needs formatting - check if it's a list separated by semicolons or commas
                if ';' in clean_content and len(clean_content.split(';')) > 2:
                    # Semicolon-separated list - convert to bullets
                    items = [item.strip() for item in clean_content.split(';') if item.strip()]
                    bullets = '\n'.join([f'- {item}' for item in items])
                    st.chat_message("assistant").markdown(bullets)
                elif ',' in clean_content and len(clean_content.split(',')) > 3:
                    # Comma-separated list with many items - convert to bullets
                    items = [item.strip() for item in clean_content.split(',') if item.strip()]
                    bullets = '\n'.join([f'- {item}' for item in items])
                    st.chat_message("assistant").markdown(bullets)
                elif '\n' in clean_content and len(clean_content.split('\n')) > 2:
                    # Multi-line content - check if it's actually a list or continuous text
                    lines = [line.strip() for line in clean_content.split('\n') if line.strip()]
                    
                    # Check if lines are actually separate items (short lines) or continuous text
                    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
                    has_sentence_connectors = any(line.lower().startswith(word) for line in lines 
                                                for word in ['therefore', 'however', 'moreover', 'furthermore', 'additionally', 'consequently'])
                    
                    if avg_line_length > 100 or has_sentence_connectors:
                        # This looks like continuous text that was incorrectly split - join it back
                        continuous_text = ' '.join(lines)
                        st.chat_message("assistant").write(continuous_text)
                    else:
                        # This looks like actual separate items - format as list
                        formatted_content = ""
                        for line in lines:
                            # Check if line looks like a heading
                            if (len(line) < 50 and 
                                (line.isupper() or line.endswith(':') or 
                                 any(word in line.upper() for word in ['COMPETENCIES', 'TRAINING', 'EXPERIENCE', 'SKILLS']))):
                                formatted_content += f"\n\n**{line}**\n"
                            elif len(line) > 150:
                                # Long line - treat as paragraph
                                formatted_content += f"\n{line}\n"
                            else:
                                # Short line - treat as bullet point
                                formatted_content += f"- {line}\n"
                        
                        st.chat_message("assistant").markdown(formatted_content)
                else:
                    # Single paragraph or short content
                    st.chat_message("assistant").write(clean_content)
        
        # Display images if any were found
        if images:
            with st.chat_message("assistant"):
                st.markdown("**📸 Related Images:**")
                cols = st.columns(min(len(images), 3))  # Max 3 images per row
                
                for i, image_path in enumerate(images):
                    with cols[i % 3]:
                        try:
                            if os.path.exists(image_path):
                                st.image(image_path, caption=f"Image {i+1}", use_column_width=True)
                            else:
                                st.error(f"Image not found: {image_path}")
                        except Exception as e:
                            st.error(f"Error displaying image: {str(e)}")
        
        # If no clean content and no images, show original content
        if not clean_content and not images:
            st.chat_message("assistant").write(content)


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Query Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-container {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        background: #fafafa;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Increase chat message text size - clean version */
    .stChatMessage {
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
    }
    
    .stChatMessage p {
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
        margin-bottom: 0.8rem !important;
    }
    
    .stChatMessage ul, .stChatMessage ol {
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
    }
    
    .stChatMessage li {
        font-size: 1.3rem !important;
        margin-bottom: 0.6rem !important;
    }
    
    /* Increase chat input text size */
    .stChatInput > div > div > input {
        font-size: 1.2rem !important;
        padding: 0.8rem !important;
    }
    
    /* Make chat messages more readable */
    [data-testid="stChatMessage"] {
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] div {
        font-size: 1.3rem !important;
        line-height: 1.7 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced title and header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Query Assistant</h1>
        <p>Ask questions about your documents and get AI-powered answers!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load documents initially and store in session state
    if 'documents' not in st.session_state or st.session_state.get('reload_documents', False):
        with st.spinner("Loading documents..."):
            st.session_state.documents = load_documents()
            st.session_state.reload_documents = False
            # Clear the initialized flag to force reinitialization of components
            if st.session_state.get('reload_documents', False):
                st.session_state.pop('initialized', None)
                st.session_state.pop('retriever', None)
                st.session_state.pop('gemini', None)
    
    documents = st.session_state.documents
    
    # Sidebar for document management
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📚 Document Management")
        
        # Action buttons with improved layout
        st.markdown("**Quick Actions:**")
        col1, col2 = st.columns(2)
        with col1:
            refresh_clicked = st.button("🔄 Refresh", help="Reload documents from data/ folder", use_container_width=True)
        with col2:
            clear_clicked = st.button("🗑️ Clear Chat", help="Clear chat history", use_container_width=True)
            
        if refresh_clicked:
            with st.spinner("🔄 Refreshing documents..."):
                # Clear all cached data and force reload
                st.session_state.documents = refresh_documents()
                documents = st.session_state.documents
                
                # Force reinitialization of AI components with new documents
                st.session_state.pop('initialized', None)
                st.session_state.pop('retriever', None) 
                st.session_state.pop('gemini', None)
                
                # Set reload flag and timestamp
                st.session_state.reload_documents = True
                st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
                
            st.success(f"✅ Documents refreshed! Found {len(documents)} documents.")
            
            # Show what was found
            if documents:
                st.info(f"📄 Loaded: {', '.join([doc['file_name'] for doc in documents])}")
            
            st.rerun()
        
        if clear_clicked:
            st.session_state.chat_history = []
            st.success("✅ Chat history cleared!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display loaded documents with improved styling
        if documents:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.success(f"✅ Loaded {len(documents)} documents")
            
            # Show last refresh time
            if 'last_refresh' in st.session_state:
                st.caption(f"Last refreshed: {st.session_state.last_refresh}")
            
            # Show document list with enhanced display
            st.markdown("**📄 Document Library:**")
            for i, doc in enumerate(documents, 1):
                file_type_icons = {
                    'pdf': '📄',
                    'docx': '📝', 
                    'txt': '📃'
                }
                icon = file_type_icons.get(doc['file_type'].lower().replace('.', ''), '📄')
                
                with st.expander(f"{icon} {doc['file_name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Type", doc['file_type'].upper().replace('.', ''))
                    with col2:
                        st.metric("Size", f"{len(doc['content']):,} chars")
                    
                    # Enhanced preview
                    st.markdown("**Preview:**")
                    preview_text = doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content']
                    st.text_area("Document Preview", preview_text, height=100, disabled=True, key=f"preview_{i}", label_visibility="collapsed")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ No documents found in 'data/' folder")
            st.info("📁 Please add .pdf, .docx, or .txt files to the 'data/' folder and click refresh.")
            return
        
        # Settings with enhanced styling
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("**⚙️ Settings**")
        max_docs = st.slider("Max relevant documents", 1, 5, 3, help="Number of documents to use for context")
        show_sources = st.checkbox("Show document sources", True, help="Display which documents were used for each answer")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'initialized' not in st.session_state:
        with st.spinner("Initializing AI components..."):
            retriever, gemini, error = initialize_components(documents)
            if error:
                st.error(f"❌ Error initializing AI: {error}")
                st.info("Please check your .env file and ensure GEMINI_API_KEY is set correctly.")
                return
            st.session_state.retriever = retriever
            st.session_state.gemini = gemini
            st.session_state.initialized = True
    
    # Main chat interface with improved layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat history with enhanced styling
        chat_container = st.container()
        with chat_container:
            if st.session_state.chat_history:
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for entry in st.session_state.chat_history:
                    format_chat_message("user", entry["question"], entry["timestamp"])
                    
                    if show_sources and entry.get("sources"):
                        with st.expander("📄 Sources used:"):
                            for source in entry["sources"]:
                                relevance = source.get('similarity_score', 0)
                                st.write(f"- **{source['file_name']}** (relevance: {relevance:.3f})")
                    
                    format_chat_message("assistant", entry["answer"], entry["timestamp"])
                    st.divider()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("👋 Welcome! Ask me anything about your documents.")
    
    with col2:
        # Statistics and metrics
        st.subheader("📊 Statistics")
        with st.container():
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("📚 Documents", len(documents))
                st.metric("💬 Messages", len(st.session_state.chat_history))
            with col_b:
                if st.session_state.chat_history:
                    avg_length = sum(len(entry["answer"]) for entry in st.session_state.chat_history) // len(st.session_state.chat_history)
                    st.metric("📝 Avg Response", f"{avg_length} chars")
                else:
                    st.metric("📝 Avg Response", "0 chars")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_question = st.chat_input("Ask a question about your documents...")
    
    if user_question:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add user question to history immediately
        format_chat_message("user", user_question, timestamp)
        
        with st.spinner("🔍 Searching documents and generating answer..."):
            try:
                # For competency/capability questions, use more documents to get complete info
                search_terms = user_question.lower()
                if any(term in search_terms for term in ['competenc', 'skill', 'service', 'capabilit', 'core', 'all']):
                    # Use more documents for comprehensive answers
                    retrieval_count = min(max_docs + 2, 10)
                else:
                    retrieval_count = max_docs
                
                # Retrieve relevant documents
                relevant_docs = st.session_state.retriever.retrieve_relevant_chunks(
                    user_question, top_k=retrieval_count
                )
                
                # Special handling for SVB queries - ensure SVB document is included
                if 'svb' in user_question.lower() or 'process flow chart' in user_question.lower():
                    # Find SVB document in all documents
                    svb_doc = None
                    for doc in st.session_state.documents:
                        if 'SVB' in doc.get('file_name', '').upper() or 'svb' in doc.get('file_name', '').lower():
                            svb_doc = doc.copy()  # Make a copy
                            svb_doc['similarity_score'] = 1.0  # Set high relevance
                            break
                    
                    # Add SVB document to relevant docs if found and not already included
                    if svb_doc:
                        # Check if already included
                        already_included = any(doc.get('file_name') == svb_doc.get('file_name') for doc in relevant_docs)
                        if not already_included:
                            relevant_docs.insert(0, svb_doc)  # Add at the beginning with highest priority
                            print(f"🎯 Added SVB document to context: {svb_doc.get('file_name')}")
                        else:
                            print(f"🎯 SVB document already in context: {svb_doc.get('file_name')}")
                    else:
                        print(f"⚠️ SVB document not found in loaded documents")
                
                # Show sources if enabled
                if show_sources and relevant_docs:
                    with st.expander("📄 Sources found:"):
                        for doc in relevant_docs:
                            st.write(f"- **{doc['file_name']}** (relevance: {doc['similarity_score']:.3f})")
                
                # Generate answer
                answer = st.session_state.gemini.chat_with_context(
                    user_question, 
                    relevant_docs, 
                    st.session_state.chat_history
                )
                
                # Display answer
                format_chat_message("assistant", answer, timestamp)
                
                # Save to session state
                st.session_state.chat_history.append({
                    "question": user_question,
                    "answer": answer,
                    "sources": relevant_docs,
                    "timestamp": timestamp
                })
                
                # Rerun to update the display
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
