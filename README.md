# 🧠 QuizCraft

Turn any **PDF into an AI-powered multiple-choice quiz**!

## 🚀 Features
- 📂 Upload PDFs and extract text automatically
- 🤖 Generate 15+ MCQs with 4 options each using Groq LLaMA-3
- 📝 Interactive quiz with instant results and scoring

## 🛠️ Tech Stack
- **Streamlit** – Web interface
- **pdfplumber** – PDF text extraction
- **Groq API** – AI MCQ generation

## 📦 Installation
Clone the repository: `git clone https://github.com/kazishakkhar17/QuizCraft.git` and `cd QuizCraft`.  
Install dependencies: `pip install -r requirements.txt`.  
Create `.streamlit/secrets.toml` and add your Groq API key: `GROQ_API_KEY = "your_api_key_here"`.  
Run the app: `streamlit run main.py`.

## ⚡ Usage
1. Upload a PDF
2. Click **Start Your Test**
3. Take the quiz and see your score

## 🌐 Live Demo
Try it online here: [https://quizcraftbykazi.streamlit.app/](https://quizcraftbykazi.streamlit.app/)

## 📌 Example MCQ Output
{
  "question": "Which organ filters blood?",
  "options": ["Heart", "Kidney", "Lungs", "Liver"],
  "correct_option": 1
}

## 🤝 License
MIT License
