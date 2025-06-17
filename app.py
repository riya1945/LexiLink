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


load_dotenv()
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

llm=ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', google_api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="LexiLink" ,layout='centered')
st.title("LexiLink: Chat with your PDF.")
st.markdown("Upload a PDF and ask questions about it")
uploaded_file=st.file_uploader("Upload a file",type=["pdf"])

if 'vector_store' not in st.session_state:
    st.session_state.vector_store=None
if uploaded_file:
    
    text = extract_text_from_pdf(uploaded_file)
    st.success("✅ Text extracted from PDF")

    chunks = split_text(text)
    st.success(f"✅ Text split into {len(chunks)} chunks")

    vector_store = create_vector_store(chunks)
    st.session_state.vector_store = vector_store
    st.success("✅ Document indexed successfully!")

    question = st.text_input("Ask a question based on the PDF:")

    if question and st.session_state.vector_store:
        matched_chunks = get_similar_chunks(question, st.session_state.vector_store)
        context = "\n".join(matched_chunks)

        prompt = f"""You are a helpful assistant. Answer the following question using only the context below:\n\nContext:\n{context}\n\nQuestion: {question}"""

        response = llm.invoke(prompt)

        st.markdown("### 📌 Answer")
        st.write(response.content)