import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os
from typing import Optional

st.set_page_config(
    page_title="Document Q&A Assistant",
    page_icon="📚",
    layout="wide"
)

SYSTEM_PROMPT = """You are a helpful AI assistant created by Chetan. You can answer questions about uploaded documents or provide general assistance. 

If someone asks about who created you or how you are, respond that you were made by Chetan.

When answering questions about uploaded documents, provide accurate and detailed responses based on the content. For general questions without document context, provide helpful and informative answers."""

def configure_gemini():
    """Configure Gemini API"""
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def read_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def read_txt(file) -> str:
    """Extract text from TXT file"""
    try:
        return file.read().decode('utf-8')
    except Exception as e:
        st.error(f"Error reading TXT file: {str(e)}")
        return ""

def get_gemini_response(prompt: str, document_content: Optional[str] = None, chat_history: list = None) -> str:
    """Get response from Gemini model with conversation history"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest') # change to your preferred model
        
        # Build conversation context
        conversation_context = ""
        if chat_history:
            conversation_context = "\n\nPrevious Conversation:\n"
            for q, a in chat_history[-5:]:  # Include last 5 exchanges for context
                conversation_context += f"User: {q}\nAssistant: {a}\n\n"
        
        # Build full prompt with all context
        if document_content:
            full_prompt = f"{SYSTEM_PROMPT}\n\nDocument Content:\n{document_content}{conversation_context}\nCurrent User Question: {prompt}"
        else:
            full_prompt = f"{SYSTEM_PROMPT}{conversation_context}\nCurrent User Question: {prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    st.title("📚 Document Q&A Assistant")
    st.markdown("Upload a PDF or TXT file and ask questions about it, or ask general questions!")
    
    # Sidebar for API configuration
    st.sidebar.title("Configuration")
    api_configured = configure_gemini()
    
    if not api_configured:
        st.warning("Please enter your Gemini API key in the sidebar to continue.")
        return
    
    # File upload section
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=['pdf', 'txt'],
        help="Upload a document to ask questions about its content"
    )
    
    # Initialize session state
    if 'document_content' not in st.session_state:
        st.session_state.document_content = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Process uploaded file
    if uploaded_file is not None:
        with st.spinner("Processing document..."):
            if uploaded_file.type == "application/pdf":
                document_text = read_pdf(uploaded_file)
            else:  # txt file
                document_text = read_txt(uploaded_file)
            
            if document_text:
                st.session_state.document_content = document_text
                st.success(f"✅ Document '{uploaded_file.name}' processed successfully!")
                
                # Show document preview
                with st.expander("📖 Document Preview"):
                    st.text_area(
                        "Document Content (first 1000 characters)",
                        document_text[:1000] + "..." if len(document_text) > 1000 else document_text,
                        height=200,
                        disabled=True
                    )
    
    # Chat interface
    st.header("💬 Ask Questions")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**You:** {question}")
            st.markdown(f"**Assistant:** {answer}")
            st.divider()
    
    # Input for new question
    user_question = st.text_input(
        "Ask a question about the document or anything else:",
        placeholder="Type your question here..."
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        ask_button = st.button("Ask Question", type="primary")
    
    with col2:
        clear_button = st.button("Clear Chat History")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if ask_button and user_question:
        with st.spinner("Generating response..."):
            response = get_gemini_response(
                user_question, 
                st.session_state.document_content,
                st.session_state.chat_history
            )
            
            # Add to chat history
            st.session_state.chat_history.append((user_question, response))
            st.rerun()
    
    # Information section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ How to use:")
    st.sidebar.markdown("""
    1. Enter your Gemini API key
    2. Upload a PDF or TXT file (optional)
    """)
    
    st.sidebar.markdown("### 🔧 Features:")
    st.sidebar.markdown("""
    - PDF and TXT file support
    - Document-based Q&A
    - Multi-turn conversations with context
    - Chat history with memory
    """)

if __name__ == "__main__":
    main()
