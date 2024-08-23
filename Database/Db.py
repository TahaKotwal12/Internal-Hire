import pymysql
import json
import pandas as pd
import streamlit as st
import os
from utils.util_functions import generate_embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

def database_connection():
    connection = pymysql.connect(
        host = os.environ.get('HOST'),
        port = int(os.environ.get('PORT')),
        user = os.environ.get('USER'),
        password = os.environ.get('PASSWORD'),
        database = os.environ.get('DATABASE'),
        ssl_verify_cert = True,
        ssl_verify_identity = True,
        ssl_ca = os.environ.get('SSL_CA')
    )
    return connection

def load_data():
    connection = database_connection()
    cursor = connection.cursor()
    sql = "SELECT id, name, department, text, available FROM core_mstrs_organization_resumes"
    result = cursor.execute(sql)
    records = cursor.fetchall()
    records = list(records)
    connection.close()
    df = pd.DataFrame(records, columns=['ID', 'NAME', 'DEPARTMENT', 'RESUME SUMMARY', 'AVAILABILITY'])
    st.session_state.df = df

def add_entry(name, department, text, available, embeddings):
    connection = database_connection()
    cursor = connection.cursor()
    sql = "INSERT INTO core_mstrs_organization_resumes (name, department, text, available, embedding) VALUES (%s, %s, %s, %s, %s)"
    values = (name, department, text, available, embeddings)
    result = cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return result

def delete_entry(id):
    connection = database_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM core_mstrs_organization_resumes WHERE id = %s;"
    values = id
    result = cursor.execute(sql, values)
    connection.commit()
    connection.close()
    return result

def similarity_search(query):
    query_embedding = generate_embeddings(text=query)
    query_embedding = json.dumps(query_embedding)
    
    connection = database_connection()
    cursor = connection.cursor()
    sql = "SELECT id, name, department, text, available, 1 - Vec_Cosine_Distance(embedding, %s) AS similarity_score FROM core_mstrs_organization_resumes ORDER BY similarity_score DESC LIMIT 5"
    values = query_embedding
    result = cursor.execute(sql, values)
    nearest = cursor.fetchall()
    connection.close()
    return list(nearest)

def generate_response(question, result, job_description):
    # Concatenate all relevant information from the search results
    context = f"Job Description: {job_description}\n\n"
    context += "Candidate Information:\n"
    for r in result:
        context += f"""
        Name: {r[1]}
        Department: {r[2]}
        Resume Summary: {r[3]}
        Available: {"Yes" if r[4] == 1 else "No"}
        Match Score: {int(r[5] * 100)}%
        ---
        """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Professional HR Bot. Your task is to assist with questions about job candidates based on the provided context. Follow these guidelines:

        1. Answer questions as detailed as possible using the provided context of job description and candidate information.
        2. When asked to compare candidates, use the job description and candidate information to provide a thorough analysis.
        3. If asked about a specific candidate, only provide information that is explicitly stated in the context for that candidate.
        4. If information about a specific candidate is not in the context, clearly state that you don't have information about that candidate.
        5. Do not invent or assume any information that is not provided in the context.
        6. Avoid using any formatting symbols or new line characters in your responses.
        7. Do not answer any questions that are outside the scope of the provided context.
        8. If asked to rank or recommend candidates, base your analysis on the match scores and how well the candidates' skills align with the job description.

        Remember, your responses should be helpful for HR professionals in making informed decisions about candidates."""),
                ("user", f"CONTEXT: {context} \n QUESTION: {question}")
            ])
    
    google_api_key = os.environ.get('GOOGLE_API_KEY')
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        max_retries=2,
        api_key=google_api_key
    )

    outputParser = StrOutputParser()
    chain = prompt | llm | outputParser
    
    response = chain.invoke({"context": context, "question": question})
    return response