# LinkedIn Profile Generator from Resume

This Streamlit application automatically generates LinkedIn profile content from a user's uploaded resume.

## Features

- PDF resume upload
- Extraction of key information from resume
- Generation of LinkedIn headlines
- Formatting of work experience for LinkedIn
- Structuring of education details for LinkedIn

## Requirements

- Python 3.7+
- Streamlit
- PyPDF2
- langchain
- python-dotenv

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```
   groq_api_key=your_api_key_here
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Upload a PDF resume
3. Click "Work" to generate LinkedIn profile content

## Note

This project uses the Groq API with the Gemma 2 9B model for natural language processing tasks.
