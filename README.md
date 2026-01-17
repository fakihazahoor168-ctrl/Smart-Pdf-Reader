# AI PDF Reader & Question Generator

This project is an AI-based system that reads PDF files and generates summaries, questions, and MCQs using Transformer-based NLP models.

## Features
- Upload PDF files  
- Generate summary  
- Generate questions  
- Generate MCQs  
- Easy / Medium / Hard difficulty  
- Short & Long questions  

## Models Used
- **BART (facebook/bart-large-cnn)** – for text summarization  
- **T5 (valhalla/t5-base-qg-hl)** – for question and MCQ generation  

## Technologies
- Python  
- Streamlit  
- Hugging Face Transformers  
- PyPDF2  

## How It Works
1. Upload PDF  
2. Extract text  
3. AI model processes text  
4. Output is generated  

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
