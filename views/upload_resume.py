import streamlit as st
import pandas as pd
from utils.util_functions import summarize, readPDF, generate_embeddings
from utils.text_processing import extract_key_details, create_summary_with_details
import json
from Database.Db import load_data, add_entry

st.title("Upload Resume")

name = st.text_input("Name")
department = st.selectbox("Department", options=['Engineering', 'Data Science', 'Product', 'Design', 'Marketing', 'Human Resource','Finance','Customer Support', 'Legal','Sales','Admin','Research','Quality Assurance','Training and Development','Public Relations','Compliance'])
available = st.radio("Is Available?", options=['Yes', 'No'],horizontal=True)
resume_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])




if st.button("Submit"):
    if name and department and available and resume_file:

        #Convert string to bool
        if available == 'Yes':
            available = True
        else:
            available = False


        try:
            with st.spinner("Adding entry please wait!!"):
                temp_file = "./temp.pdf"
                with open(temp_file, "wb") as file:
                    file.write(resume_file.getvalue())
                    file_name = resume_file.name
                    file.close()
                
                document = readPDF(temp_file)[0].page_content
                document_summary = summarize(document)
                key_details = extract_key_details(document)
                
                enhanced_summary = create_summary_with_details(document_summary, key_details)
                
                embeddings = generate_embeddings(enhanced_summary)

                result = add_entry(name=name, department=department, text=enhanced_summary, available=available, embeddings=json.dumps(embeddings))
                if result == 1:
                    load_data()
                    st.success("Record added Successfully") 
                else:
                    st.error("Sorry! could not add entry")       
        except Exception as e:
            st.error(f"Sorry! something went wrong. Error: {str(e)}")  
    else:
        st.error("Please fill in all fields and upload a resume.")