from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
embedding_model=GoogleGenerativeAIEmbeddings(model='models/embedding-001',google_api_key=GOOGLE_API_KEY)

def create_vector_store(chunks):
    vector_store=FAISS.from_texts(chunks,embedding_model)
    return vector_store

def get_similar_chunks(query, vector_store, k=3):
    results=vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in vector_store.similarity_search(query, k=k)]



