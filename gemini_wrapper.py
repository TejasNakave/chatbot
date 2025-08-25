import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime


class GeminiAPIWrapper:
    """
    A wrapper class for the Gemini API that handles question-answering with context.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini API wrapper.
        
        Args:
            api_key (Optional[str]): Gemini API key. If None, loads from environment.
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in .env file or pass it directly.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model with increased output tokens
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2048,  # Increased from default
            temperature=0.7,
        )
        self.model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        
        print("Gemini API wrapper initialized successfully!")
    
    def ask_question(self, question: str, context: str = "", max_tokens: int = 1000) -> str:
        """
        Ask a question to Gemini with optional context.
        
        Args:
            question (str): The question to ask
            context (str): Additional context to provide to the model
            max_tokens (int): Maximum number of tokens in the response
            
        Returns:
            str: The model's response
        """
        try:
            # Construct the prompt
            if context.strip():
                prompt = f"""Based on the following context, please answer the question:

Context:
{context}

Question: {question}

Instructions:
- Provide a clear, comprehensive answer based on the context
- Use bullet points when listing multiple items or features
- Make the response descriptive and well-structured
- Do NOT include any references, citations, or page numbers
- Focus on being helpful and informative

Answer the question clearly and descriptively:"""
            else:
                prompt = f"""Question: {question}

Instructions:
- Provide a clear, comprehensive answer
- Use bullet points when listing multiple items or features
- Make the response descriptive and well-structured
- Focus on being helpful and informative

Answer the question clearly and descriptively:"""
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                return "I'm sorry, I couldn't generate a response to your question."
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat_with_context(self, question: str, documents: list, chat_history: list = None) -> str:
        """
        Answer a question using the provided documents as context and chat history.
        
        Args:
            question (str): The question to ask
            documents (list): List of document dictionaries with 'content' key
            chat_history (list): Previous conversation history for context
            
        Returns:
            str: The model's response without citations, with global fallback
        """
        # Build conversation context from chat history
        conversation_context = ""
        if chat_history and len(chat_history) > 0:
            # Include last few exchanges for context (limit to avoid token overflow)
            recent_history = chat_history[-3:] if len(chat_history) > 3 else chat_history
            conversation_context = "Recent conversation context:\n"
            for entry in recent_history:
                conversation_context += f"User: {entry.get('question', '')}\n"
                conversation_context += f"Assistant: {entry.get('answer', '')}\n\n"
            conversation_context += "Current question follows:\n\n"
        
        # First try to answer using provided documents
        if documents and len(documents) > 0:
            # Combine all document content as context
            context = ""
            
            for i, doc in enumerate(documents):
                doc_name = doc.get('file_name', f'Document {i+1}')
                content = doc.get('content', '')
                if content.strip():
                    context += f"Document: {doc_name}\n{content}\n\n"
            
            # Check if we have any actual content
            if context.strip():
                # Limit context length to avoid token limits
                if len(context) > 12000:  # Increased limit for longer responses
                    context = context[:12000] + "...\n[Content truncated due to length]"
                
                # Try answering with document context first
                current_date = datetime.now().strftime("%A, %B %d, %Y")
                current_time = datetime.now().strftime("%I:%M %p")
                
                document_prompt = f"""Current Date: {current_date}
Current Time: {current_time}

You are an AI assistant that provides clear, descriptive answers. Always give the most helpful answer possible.

{conversation_context}Document Content:
{context}

Question: {question}

Instructions:
- Consider the conversation context when answering
- If the question refers to "it", "this", "that", or "more details", refer to the previous conversation
- If asked about current date/time, use the provided current date and time above
- Search through the document content for relevant information
- If asking about competencies, skills, services, or capabilities, provide the COMPLETE list from the documents
- Do not truncate lists - include ALL items mentioned in the documents
- If the documents contain the answer, use that information
- CRITICAL: If you see "[IMAGE_X: path]" references in the content, you MUST include them EXACTLY in your answer
- CRITICAL: If you see "[IMAGES_AVAILABLE: X images extracted]", you MUST mention this in your response
- CRITICAL: When answering about visual content (charts, diagrams, processes), ALWAYS include any image references found
- CRITICAL: Copy image references exactly as they appear: [IMAGE_0: full_path]
- If the documents do NOT contain the answer, respond ONLY with: "GLOBAL_SEARCH_NEEDED"
- Do NOT explain that the document doesn't contain the information
- Do NOT mention the document at all if it doesn't have the answer
- Either provide the document-based answer (including any image references EXACTLY as found) OR respond with exactly "GLOBAL_SEARCH_NEEDED"

Answer:"""

                try:
                    # Debug: Print what we're sending to AI
                    if "SVB" in question.upper() or "PROCESS" in question.upper():
                        print(f"🤖 DEBUG: Sending to AI:")
                        print(f"  Question: {question}")
                        print(f"  Context length: {len(context)} chars")
                        if "[IMAGE_" in context:
                            print(f"  ✅ Context contains image references")
                            import re
                            image_refs = re.findall(r'\[IMAGE_\d+: [^\]]+\]', context)
                            for ref in image_refs:
                                print(f"    - {ref}")
                        else:
                            print(f"  ❌ No image references found in context")
                    
                    response = self.model.generate_content(document_prompt)
                    if response.text and response.text.strip():
                        doc_answer = response.text.strip()
                        
                        # Debug: Print what AI responded
                        if "SVB" in question.upper() or "PROCESS" in question.upper():
                            print(f"🤖 DEBUG: AI Response:")
                            print(f"  Response length: {len(doc_answer)} chars")
                            if "[IMAGE_" in doc_answer:
                                print(f"  ✅ Response contains image references")
                                import re
                                image_refs = re.findall(r'\[IMAGE_\d+: [^\]]+\]', doc_answer)
                                for ref in image_refs:
                                    print(f"    - {ref}")
                            else:
                                print(f"  ❌ No image references in response")
                                print(f"  First 200 chars: {doc_answer[:200]}")
                        
                        # Check for explicit global search signal
                        if doc_answer == "GLOBAL_SEARCH_NEEDED":
                            return self._get_global_answer(question, conversation_context)
                        
                        # Check if the answer indicates information wasn't found
                        not_found_indicators = [
                            "document does not specify", "document does not mention", 
                            "document does not provide", "document does not contain",
                            "text does not include", "document focuses on", "therefore, i cannot",
                            "based on the given text", "document appears to be empty",
                            "no content available", "couldn't be processed",
                            "provided text", "does not specify", "does not include",
                            "text about", "does not mention", "is not provided",
                            "information is not", "details are not", "not mentioned in",
                            "provided document", "guide for", "does not contain information"
                        ]
                        
                        # If the document-based answer seems incomplete, try global search
                        if any(indicator in doc_answer.lower() for indicator in not_found_indicators):
                            return self._get_global_answer(question, conversation_context)
                        else:
                            return doc_answer
                except Exception:
                    pass  # Fall through to global search
        
        # Fallback to global search if no documents or document search failed
        return self._get_global_answer(question, conversation_context)
    
    def _get_global_answer(self, question: str, conversation_context: str = "") -> str:
        """
        Provide a global answer when information isn't found in documents.
        
        Args:
            question (str): The question to answer
            conversation_context (str): Previous conversation context
            
        Returns:
            str: A comprehensive answer from global knowledge
        """
        # Get current date and time
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        global_prompt = f"""Current Date: {current_date}
Current Time: {current_time}

Provide a clear, comprehensive answer to this question using your general knowledge:

{conversation_context}Question: {question}

Instructions:
- Consider the conversation context when answering
- If the question refers to "it", "this", "that", or "more details", refer to the previous conversation
- If asked about current date/time, use the provided current date and time above
- Provide a detailed, informative answer
- Use bullet points when listing multiple items or features
- Make the response descriptive and well-structured
- Do NOT mention that this information comes from general knowledge
- Do NOT say the information wasn't found in documents
- Provide the best possible answer you can

Answer the question clearly and descriptively:"""
        
        try:
            response = self.model.generate_content(global_prompt)
            if response.text:
                return response.text.strip()
            else:
                return "I'm sorry, I couldn't generate a response to your question."
        except Exception as e:
            return f"Error generating response: {str(e)}"


def test_gemini_wrapper():
    """Test function for the Gemini API wrapper."""
    try:
        gemini = GeminiAPIWrapper()
        
        # Test simple question
        response = gemini.ask_question("What is the capital of France?")
        print("Test Question: What is the capital of France?")
        print(f"Response: {response}\n")
        
        # Test with context
        context = "Python is a high-level programming language. It was created by Guido van Rossum."
        question = "Who created Python?"
        response = gemini.ask_question(question, context)
        print(f"Test Question with Context: {question}")
        print(f"Context: {context}")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error testing Gemini wrapper: {str(e)}")


if __name__ == "__main__":
    test_gemini_wrapper()
