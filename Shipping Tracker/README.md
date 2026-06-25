# 📦 AI Shipping Assistant

An **AI-powered customer support assistant** for shipping companies.  
This project combines **Streamlit** for the UI, **Groq** for high-speed reasoning, and a **SQL database** for order management.  

The assistant can:  
✅ Track orders by Transaction ID  
✅ Update customer details (email, name, phone number)  
✅ Provide natural language responses to user queries  

---

## 📸 Demo Screenshot
![App Screenshot](./Screenshot%202025-10-04%20091614.png)  
*Example of the AI Shipping Assistant UI in action.*

---

## 🚀 Features
- **Interactive Chat UI** built with Streamlit  
- **AI Agent with tool-calling** (functions for database operations)  
- **Database integration** for real-time order lookups and updates  
- **Polite and clear assistant personality**  

---

## 🛠️ Tech Stack
- Python 3.10+  
- Streamlit – Web UI  
- Groq API – LLM with function calling  
- Pydantic – Data validation  
- MySQL DB – Store and manage shipping orders  

---

## 📂 Project Structure
```text
├── db.py                 # Database utilities (get_order, update_email, etc.)
├── app.py                # Main Streamlit app (AI chat interface)
└── README.md             # Project documentation
