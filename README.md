# 🧠 Job Portal & CV Analyzer

A **Flask-based web application** that connects job seekers and employers through intelligent keyword matching.  
The system analyzes uploaded CVs against job descriptions using **string matching algorithms (Brute Force, KMP, and Rabin-Karp)** to identify relevant skills efficiently.



## 🚀 Features
- Upload and analyze CVs in PDF or DOCX format  
- Batch analysis for multiple CVs  
- Role-based keyword detection  
- Real-time performance and comparison metrics  
- Frontend built with **HTML, CSS, JavaScript**  
- Backend powered by **Python (Flask)**  

## 📂 Folder Structure
```plaintext
Job-Portal-CV-Analyzer/
│
├── app.py                 # Main Flask application (entry point)
│
├── templates/             # HTML templates (home, single, batch, performance, etc.)
│
├── static/                # Frontend assets: CSS, JS, images
│
├── utils/                 # Core logic: string matching algorithms and helper functions
│
├── uploads/               # Folder for uploaded CVs
│
├── DataSet/               # Contains sample or batch CV data for testing
│
└── results/               # Stores analysis and performance results


