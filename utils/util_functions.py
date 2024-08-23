from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os


#google API
google_api_key = os.environ.get('GOOGLE_API_KEY')

#PDF to text
def readPDF(file_name):

    loader = PyPDFLoader(file_name)
    pages = loader.load_and_split()
    return pages


def summarize(resume_content):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a Professional Resume summarizer. I will provide you resume in text format."),
            ("user","Summarize the following resume in less than 500 words, focusing on key qualifications, skills, work experience, and education and personal information. Capture the essence of the candidate's professional profile, highlighting their most relevant achievements and expertise. Provide a concise overview that would be useful for HR professionals and talent acquisition specialists in quickly assessing the candidate's fit for potential roles. Avoid using any formatting symbols or new line characters. Present the summary as a continuous paragraph of text. \n RESUME: {resume}")
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        max_retries=2,
        api_key=google_api_key
    )
    outputParser = StrOutputParser()
    chain = prompt | llm | outputParser

    resume_summary = chain.invoke({"resume": resume_content})
    return resume_summary

def generate_embeddings(text):

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
    embedding = embedding_model.embed_query(text=text)

    return embedding

def analyze_missing_skills(job_description, resume_summary):
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        max_retries=2,
        api_key=google_api_key
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant specialized in analyzing job requirements and candidate resumes. Your task is to identify key skills or technologies mentioned in the job description that are not evident in the candidate's resume summary."),
        ("user", "Job Description: {job_description}\n\nResume Summary: {resume_summary}\n\nPlease list only the key skills or technologies mentioned in the job description that are missing or not clearly demonstrated in the resume summary. Present the results as a comma-separated list of keywords. If there are no missing skills, respond with 'None'.")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"job_description": job_description, "resume_summary": resume_summary})


def remove_employee(employee_list,employee_id):
    return [emp for emp in employee_list if emp[0] != employee_id]

def bool_to_string(value):
    if value == 1:
        return "True"
    else:
        return "False"

