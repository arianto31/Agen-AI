# 🧠 Career Chatbot AI — Your Personal Interactive Career Chatbot 

[![Chat with Career Chatbot AI ](https://img.shields.io/badge/💬_Try%20the%20Chatbot-Live%20Demo-blue?style=for-the-badge)]([https://<your-chatbot-link>](https://huggingface.co/spaces/papipu31/career_conversations))

![Chatbot Screenshot](Screenshot%202025-10-10%20152606.png)
> *A personalized AI chatbot that represents your professional background.*

Personalized chatbot that represents your professional background, experience, and career profile in a conversational format.  
It reads your resume, understands your summary, and interacts with visitors as if *you* were chatting yourself.  

Built using **Groq/OpenAI models**, **Gradio**, and **Pushover notifications**, this project turns your portfolio into an intelligent and interactive career assistant.  

---

## 🚀 Features  

✅ **AI-Powered Chat Interface** — Visitors can chat directly with your AI persona using Gradio.  
✅ **Personalized Knowledge** — Reads your resume (`Profile.pdf`) and summary to build professional context.  
✅ **Smart Tools Integration** —  
- 📬 Record users who share their email or interest.  
- ❓ Log any question the bot cannot answer.  
✅ **Instant Push Notifications** — Get alerts via **Pushover** when someone interacts or asks a new question.  
✅ **Groq API Ready** — Fast and efficient inference using Groq’s OpenAI-compatible endpoint.  

---

## 🧩 Project Structure  

```text
project_root/
│
├── me/
│ ├── Profile.pdf # Your resume (used as LinkedIn-like context)
│ └── summary.txt # A short professional summary
│
├── main.py # Core chatbot logic
└── .env # Environment variables
