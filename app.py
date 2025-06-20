import streamlit as st
from utils.vector_store import create_vector_store
from utils.vector_store import get_similar_chunks
from utils.chunker import split_text
from utils.pdf_reader import extract_text_from_pdf
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', google_api_key=GOOGLE_API_KEY)

# Page configuration
st.set_page_config(
    page_title="LexiLink - Chat with your PDF",
    page_icon="📄",
    layout='wide',
    initial_sidebar_state="expanded"
)

# Custom CSS matching the HTML design
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
        color: white;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        color: white;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        border: 2px dashed #dee2e6;
        margin-bottom: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e6f0ff 100%);
    }
    
    .status-card {
        background: #d1f2eb;
        border: 1px solid #a3e4d7;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
    }
    
    .processing-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
    }
    
    .pending-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        animation: fadeIn 0.3s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        margin-left: 2rem;
        margin-right: 0;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border-left: 4px solid #9c27b0;
        margin-right: 2rem;
        margin-left: 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    .file-info {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        width: 75%;
        border-radius: 4px;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .sidebar .stButton > button {
        background: #f8f9fa;
        color: #495057;
        border: 1px solid #dee2e6;
        font-weight: normal;
        text-align: left;
    }
    
    .sidebar .stButton > button:hover {
        background: #e9ecef;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stSidebar"] {
        background: #f8f9fa;
    }
    
    .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = ""
if 'pdf_size' not in st.session_state:
    st.session_state.pdf_size = ""
if 'chunk_count' not in st.session_state:
    st.session_state.chunk_count = 0
if 'processing_time' not in st.session_state:
    st.session_state.processing_time = 0

# Header
st.markdown("""
<div class="main-header">
    <h1>📄 LexiLink: Chat with your PDF</h1>
    <p>Upload a PDF and ask intelligent questions about its content</p>
</div>
""", unsafe_allow_html=True)

# Main Content
if not st.session_state.pdf_processed:
    # Upload Section
    uploaded_file = st.file_uploader("📤 Choose a PDF file", type=["pdf"])
    
    if uploaded_file:
        start_time = time.time()
        
        # Store file info
        st.session_state.pdf_name = uploaded_file.name
        st.session_state.pdf_size = f"{uploaded_file.size / (1024*1024):.1f} MB"
        
        with st.spinner("🔄 Processing your PDF..."):
            # Extract text
            text = extract_text_from_pdf(uploaded_file)
            
            # Split into chunks
            chunks = split_text(text)
            st.session_state.chunk_count = len(chunks)
            
            # Create vector store
            vector_store = create_vector_store(chunks)
            st.session_state.vector_store = vector_store
            st.session_state.pdf_processed = True
            
            # Calculate processing time
            end_time = time.time()
            st.session_state.processing_time = f"{end_time - start_time:.1f}s"
            
            st.rerun()

else:
    # Chat Interface
    st.markdown(f"## 💬 Chat with: {st.session_state.pdf_name}")
    
    # Processing Status Cards
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        st.markdown("""
        <div class="status-card">
            ✅ Text extracted from PDF
        </div>
        """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown(f"""
        <div class="status-card">
            ✅ Split into {st.session_state.chunk_count} chunks
        </div>
        """, unsafe_allow_html=True)
    
    with col_status3:
        st.markdown("""
        <div class="status-card">
            ✅ Document indexed successfully
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {chat['question']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>LexiLink:</strong> {chat['answer']}
        </div>
        """, unsafe_allow_html=True)
    
    # Question input
    question = st.text_input("Ask a question about your PDF...", key="question_input")
    
    col_ask, col_clear, col_new = st.columns([2, 1, 1])
    with col_ask:
        if st.button("🔍 Ask", key="ask_btn"):
            if question and st.session_state.vector_store:
                with st.spinner("🤔 Thinking..."):
                    # Get similar chunks
                    matched_chunks = get_similar_chunks(question, st.session_state.vector_store)
                    context = "\n".join(matched_chunks)
                    
                    # Create prompt
                    prompt = f"""You are a helpful assistant. Answer the following question using only the context below:

Context:
{context}

Question: {question}"""
                    
                    # Get response
                    response = llm.invoke(prompt)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": response.content
                    })
                    
                    st.rerun()
    
    with col_clear:
        if st.button("🗑️ Clear Chat", key="clear_btn"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_new:
        if st.button("📄 New Document", key="new_doc_btn"):
            st.session_state.pdf_processed = False
            st.session_state.chat_history = []
            st.session_state.vector_store = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 2rem;">
    <small>
        Made with ❤️ using Streamlit • 
        <a href="#" style="color: #667eea;">Documentation</a> • 
        <a href="#" style="color: #667eea;">Support</a>
    </small>
</div>
""", unsafe_allow_html=True)