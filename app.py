# Importing the necessary libraries
from PyPDF2 import PdfReader
# from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import streamlit as st
import json
import re

load_dotenv()

# Load the Google API key
# google_api_key = os.getenv("google_api_key")
groq_api_key = os.getenv("groq_api_key")

# Load the LLM model
# llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_api_key)
llm = ChatGroq(model="llama-3.1-70b-versatile", groq_api_key=groq_api_key)

# Streamlit app
st.set_page_config(page_title="Fill LinkedIn Profile from Resume")
st.header("Fill LinkedIn Profile from Resume")

# Get the resume file from the user
resume = st.file_uploader("Upload your resume", type="pdf")


# Read and extract data from Resume
resume_info = None
if resume:
    st.session_state.resume = resume
    reader = PdfReader(st.session_state.resume)
    page = reader.pages[0]
    resume_info = page.extract_text()
    st.session_state.resume_info = resume_info
    
work = False
if resume_info:
    work = st.button("Work")


# Prompt templates
prompt1 = PromptTemplate.from_template("""The following data is extracted from a resume which was in a pdf format. 
I want you to read the data and extract useful information like the candidate's name, 
email, phone number, linkedin profile, github profile, education, skills, experience, 
projects, certifications, and any other relevant information.

The data is: {result}

Extract the data and give me the output in a json format.
""")

prompt2 = PromptTemplate.from_template("""The following is a json data of a candidate. 
I want you to read the data and give me 5 short LinkedIn headline for the candidate.
The LinkedIn headline is a short title that describes the candidate's professional identity.
It should capture the candidate's role, industry, and expertise in a concise manner.
It should contain the job title that they have currently and a primary keyword which the candidate wants to be known for, 
you can find that from their degree or skills or from their experience and the college they got their degree from.
Give me only the headline and nothing else.
                                       
Here are some templates that you can use:

1. <job_title> | <primary_keyword> | <college_name>
2. <degree> Graduate | <Studying year at college_name> | Seeking opportunities in <degree related role>
3. <primary_keyword> | <college_name> | <job_title>
4. <primary_keyword> | Aspiring <job_title> | <primary_keyword> Enthusiast
                                       
Do not end the headline with a "Seeking Internships" or "Seeking Opportunities" or any other similar words. Be specific and unique.
Say "Seeking Internships as a <job_title>" or "Seeking Opportunities as a <job_title>" instead of saying "Seeking Internships" or "Seeking Opportunities".
                                       

The json data is: {result}
""")

prompt3 = PromptTemplate.from_template("""I'll give you a JSON data of a candidate. Your 
task is to extract the candidate's work experience and output it as a JSON-formatted list of dictionaries. 
The output must contain the following keys only:

title
company_name
employment_type - this is the type of employment (e.g. full-time, part-time, internship), you can sometimes find it from the title or the description
duration
location
description
The description should be rephrased professionally, sounding natural without third-person phrasing. It should be atleast 30 words.

Important: The output should contain only the JSON-formatted list of dictionaries. Do not include any explanations, notes, or additional commentary.
Trainee is same as intern. And if you don't find any values for any of the keys, just put null in the value. 

The JSON data is: {result}
""")

prompt4 = PromptTemplate.from_template("""I'll give you JSON data of a candidate. Your task is to 
extract the candidate's education details and output them in JSON format. The output must be a list of dictionaries with the 
following keys only:

school_name: The name of the school
degree: The degree of the candidate (e.g., Bachelor's, Master's, PhD)
field_of_study: The field of study (e.g., Biomedical engineering, Computer science)
start_date: The start date of the degree
end_date: The end date of the degree
grade: The grade, percentage, or CGPA
description: A brief description of the degree, the school, and the candidate's achievements, including CGPA, workshops, certifications, and other relevant details. The description must be in the first person and in one continuous sentence.
Important: Output only a JSON-formatted list of dictionaries, and do not include any code, explanations, or additional notes.
CBSE, ICSE are board of education, they are NOT same as field of study.
The JSON data is: {result}
""")

# Parsers
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

# Chains
chain1 = prompt1 | llm 
chain2 = prompt2 | llm | str_parser
chain3 = prompt3 | llm | json_parser
chain4 = prompt4 | llm | json_parser

# Fetch the data for the LinkedIn fields
if work:
    st.session_state.resume_info_as_json = chain1.invoke({"result": st.session_state.resume_info})
    st.session_state.linkedin_headline = chain2.invoke({"result": st.session_state.resume_info_as_json})

    st.subheader("LinkedIn headlines for your profile:")
    st.write(st.session_state.linkedin_headline)

    experience_data = chain3.invoke({"result": st.session_state.resume_info_as_json})
    st.subheader("Work experience:")
    for experience in experience_data:
        st.write("**Title:**", experience["title"])
        st.write("**Company Name:**", experience["company_name"])
        st.write("**Employment Type:**", experience["employment_type"])
        st.write("**Duration:**", experience["duration"])
        st.write("**Location:**", experience["location"])
        st.write("**Description:**", experience["description"])
        st.write("---")
    
    education_data = chain4.invoke({"result": st.session_state.resume_info_as_json})
    st.subheader("Education:")
    for education in education_data:
        st.write("**School Name:**", education["school_name"])
        st.write("**Degree:**", education["degree"])
        st.write("**Field of Study:**", education["field_of_study"])
        st.write("**Start Date:**", education["start_date"])
        st.write("**End Date:**", education["end_date"])
        st.write("**Grade:**", education["grade"])
        st.write("**Description:**", education["description"])
        st.write("---")
    

