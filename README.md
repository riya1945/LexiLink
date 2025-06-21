# 📚 LexiLink – Chat with Your PDF

LexiLink is an intelligent document assistant that lets you **chat with your PDF files** using natural language. It reads your documents, understands their contents using language models, and gives you instant answers, summaries, and insights.

Whether you're a student, researcher, or professional, LexiLink helps you quickly find the information you need without manually skimming pages.

---
<h2>Screenshots</h2>

<p align="center">
  <img src="images/Screenshot 2025-06-21 115140.jpg" width="600"><br><br>
  <img src="images/file uploaded.jpg" width="600"><br><br>
  <img src="images/question asked.jpg" width="600">
</p>

## 🚀 Features

- 🔍 Upload and query any PDF file
- 🧠 Uses Google Generative AI Embeddings for semantic understanding
- 📚 Stores document context in a vector store for fast and relevant retrieval
- 💬 Natural language Q&A interface with Streamlit
- ⚡ Built with LangChain for modular LLM pipelines

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain**
- **Google Generative AI Embeddings**
- **FAISS** (vector database)
- **Streamlit** (for the frontend UI)
- **PyPDF2 / pdfplumber / fitz** (PDF reading)

---

## 📂 Project Structure

## 🔧 Installation
1 **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/LexiLink.git
   cd LexiLink
```
2 **Install dependencies:**
```
pip install -r requirements.txt
```
3 **Set up your API key:**
```
Get your Google Generative AI API key.

Create a .env file and add:
GOOGLE_API_KEY=your_key_here
```
## Run the App
```
streamlit run app.py
```
## 👤 About Me

LexiLink was born out of a desire to make dense documents more accessible. As a student and AI enthusiast, I often found myself buried in long research papers, technical manuals, and course PDFs — wasting time skimming through pages just to find one useful paragraph.

I built LexiLink to change that.

This project combines my passion for **AI**, **natural language processing**, and **user-friendly tools** into a practical assistant that helps anyone interact with information more efficiently. Whether you’re a student, a researcher, or a curious mind, LexiLink aims to save you time and make your documents talk back.

I believe in open-source tools that empower learners. If you find this useful or want to build on it — feel free to fork, modify, and make it your own.

_Thanks for checking out LexiLink — let’s make knowledge more accessible, one PDF at a time._


