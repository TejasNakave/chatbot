#!/usr/bin/env python3
"""
Command Line Interface for the Document-based Chatbot
"""

import os
import sys
from document_loader import load_documents_from_folder
from gemini_wrapper import GeminiAPIWrapper
from retriever import SimpleRetriever


class ChatbotCLI:
    """
    Command-line interface for the chatbot.
    """
    
    def __init__(self):
        """Initialize the chatbot CLI."""
        self.documents = []
        self.retriever = None
        self.gemini = None
        self.chat_history = []
        
    def initialize(self):
        """Initialize the chatbot components."""
        print("🤖 Initializing Document Chatbot...")
        print("=" * 50)
        
        # Load documents
        print("📄 Loading documents from 'data/' folder...")
        self.documents = load_documents_from_folder("data/")
        
        if not self.documents:
            print("⚠️  No documents found in 'data/' folder.")
            print("Please add some .pdf, .docx, or .txt files to the 'data/' folder.")
            return False
        
        # Initialize retriever
        print("🔍 Setting up document retriever...")
        self.retriever = SimpleRetriever(self.documents)
        
        # Initialize Gemini API
        print("🧠 Connecting to Gemini API...")
        try:
            self.gemini = GeminiAPIWrapper()
        except Exception as e:
            print(f"❌ Error initializing Gemini API: {str(e)}")
            print("Please check your API key in the .env file.")
            return False
        
        print("✅ Chatbot initialized successfully!")
        print(f"📚 Loaded {len(self.documents)} documents")
        print("=" * 50)
        return True
    
    def show_help(self):
        """Show available commands."""
        print("\n📋 Available Commands:")
        print("  help, h       - Show this help message")
        print("  list, l       - List loaded documents")
        print("  refresh, r    - Reload documents from data/ folder")
        print("  summarize, s  - Summarize all loaded documents")
        print("  history       - Show chat history")
        print("  clear         - Clear chat history")
        print("  quit, q       - Exit the chatbot")
        print("  Or just type your question!\n")
    
    def list_documents(self):
        """List all loaded documents."""
        print(f"\n📚 Loaded Documents ({len(self.documents)}):")
        for i, doc in enumerate(self.documents, 1):
            print(f"  {i}. {doc['file_name']} ({doc['file_type']})")
        print()
    
    def show_history(self):
        """Show chat history."""
        if not self.chat_history:
            print("\n💭 No chat history yet.\n")
            return
        
        print("\n💭 Chat History:")
        print("-" * 30)
        for i, (question, answer) in enumerate(self.chat_history, 1):
            print(f"\n{i}. Q: {question}")
            print(f"   A: {answer[:200]}{'...' if len(answer) > 200 else ''}")
        print("-" * 30 + "\n")
    
    def clear_history(self):
        """Clear chat history."""
        self.chat_history.clear()
        print("🗑️  Chat history cleared.\n")
    
    def refresh_documents(self):
        """Reload documents from the data/ folder."""
        print("\n🔄 Refreshing documents from 'data/' folder...")
        
        # Reload documents
        old_count = len(self.documents)
        self.documents = load_documents_from_folder("data/")
        new_count = len(self.documents)
        
        if not self.documents:
            print("⚠️  No documents found in 'data/' folder.")
            print("Please add some .pdf, .docx, or .txt files to the 'data/' folder.")
            self.retriever = None
            return
        
        # Rebuild the retriever with new documents
        print("🔍 Rebuilding document index...")
        self.retriever = SimpleRetriever(self.documents)
        
        # Show update summary
        if new_count > old_count:
            print(f"✅ Added {new_count - old_count} new document(s)")
        elif new_count < old_count:
            print(f"ℹ️  Removed {old_count - new_count} document(s)")
        else:
            print("ℹ️  No changes detected")
        
        print(f"📚 Total documents loaded: {new_count}")
        print("🔄 Document refresh completed!\n")
    
    def summarize_documents(self):
        """Generate a summary of all loaded documents."""
        if not self.documents or not self.gemini:
            print("❌ No documents loaded or Gemini not initialized")
            return
        
        print("\n📋 Generating document summary...")
        print("🔍 Processing all documents...")
        
        # Prepare summary prompt
        all_content = ""
        for i, doc in enumerate(self.documents, 1):
            content = doc.get('content', '')[:2000]  # Limit content per doc
            all_content += f"\n\nDocument {i} - {doc['file_name']}:\n{content}"
        
        # Limit total content to avoid token limits
        if len(all_content) > 10000:
            all_content = all_content[:10000] + "\n\n[Content truncated due to length...]"
        
        summary_prompt = f"""Please provide a comprehensive summary of the following documents. 
        Include:
        1. Main topics covered
        2. Key points from each document
        3. Common themes across documents
        4. Important dates, names, or facts mentioned

        Documents:
        {all_content}
        
        Please provide a well-structured summary."""
        
        print("🧠 Generating summary with Gemini...")
        
        try:
            summary = self.gemini.ask_question(summary_prompt)
            print(f"\n📋 Document Summary:")
            print("=" * 50)
            print(summary)
            print("=" * 50)
            
            # Save to history
            self.chat_history.append(("Summarize all documents", summary))
            
        except Exception as e:
            print(f"❌ Error generating summary: {str(e)}")
        
        print("\n✅ Summary completed!\n")
    
    def ask_question(self, question: str):
        """Process a user question."""
        print(f"\n🤔 Question: {question}")
        print("🔍 Searching for relevant documents...")
        
        # Retrieve relevant documents
        relevant_docs = self.retriever.retrieve_relevant_chunks(question, top_k=3)
        
        if relevant_docs:
            print(f"📄 Found {len(relevant_docs)} relevant documents:")
            for doc in relevant_docs:
                print(f"  - {doc['file_name']} (relevance: {doc['similarity_score']:.3f})")
        else:
            print("📄 No highly relevant documents found, using general knowledge...")
        
        print("🧠 Generating answer...")
        
        # Get answer from Gemini
        answer = self.gemini.chat_with_context(question, relevant_docs)
        
        print(f"\n💡 Answer:\n{answer}\n")
        
        # Save to history
        self.chat_history.append((question, answer))
        
        return answer
    
    def run(self):
        """Run the main CLI loop."""
        # Initialize components
        if not self.initialize():
            return
        
        # Show welcome message
        print("\n🎉 Welcome to the Document Chatbot!")
        print("Type 'help' for available commands, or ask any question.")
        print("Type 'quit' to exit.\n")
        
        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Process commands
                command = user_input.lower()
                
                if command in ['quit', 'q', 'exit']:
                    print("👋 Goodbye! Thanks for using the Document Chatbot!")
                    break
                elif command in ['help', 'h']:
                    self.show_help()
                elif command in ['list', 'l']:
                    self.list_documents()
                elif command in ['refresh', 'r']:
                    self.refresh_documents()
                elif command in ['summarize', 's']:
                    self.summarize_documents()
                elif command == 'history':
                    self.show_history()
                elif command == 'clear':
                    self.clear_history()
                else:
                    # Treat as a question
                    self.ask_question(user_input)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Document Chatbot!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again.\n")


def main():
    """Main entry point."""
    chatbot = ChatbotCLI()
    chatbot.run()


if __name__ == "__main__":
    main()
