# 🤖 RAG-Based Document Chatbot using Streamlit & Gemini

This project is a **Retrieval-Augmented Generation (RAG) style chatbot** that allows users to upload documents and ask questions based on their content. It is built using **Streamlit** for the UI and **Google Gemini API** for generating intelligent responses.

---

## 🚀 Features

- 📄 Upload **PDF** and **TXT** documents  
- 💬 Ask questions from uploaded documents  
- 🧠 Maintains chat history for better responses  
- 🤖 General AI chat when no document is uploaded  
- ⚡ Fast and simple Streamlit interface  
- 🔐 Secure API key input from sidebar

---

## 🧠 How It Works

1. User uploads a document.  
2. Text is extracted from the file.  
3. User enters a question.  
4. The chatbot sends:
   - Document content (if available)  
   - Previous chat history  
   - System instructions  
   to the **Gemini model**.  
5. Gemini generates a context-aware answer.

---

## 🛠 Tech Stack

- Python  
- Streamlit  
- Google Generative AI (Gemini API)  
- PyPDF2  

---
