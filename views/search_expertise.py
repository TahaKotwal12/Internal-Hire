import streamlit as st
from Database.Db import similarity_search, generate_response
from utils.ui_function import create_donut_chart
from utils.util_functions import analyze_missing_skills

# Set page configuration
#st.set_page_config(page_title="Expertise Search", layout="wide")

# Initialize session state variables
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to analyze missing skills using AI


# Main title
st.title("Expertise Search")

# Custom CSS for styling
st.markdown("""
<style>
    .missing-skills {
        background-color: #fff3cd;
        border-left: 5px solid #ffeeba;
        padding: 10px;
        margin-bottom: 10px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #ffffff;
        border-bottom-right-radius: 0;
    }
    .chat-message.bot {
        background-color: #475063;
        color: #ffffff;
        border-top-left-radius: 0;
    }
    .chat-message .message {
        width: 100%;
        padding: 0;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# Create two columns for the main layout
col1, col2 = st.columns([3, 2])

with col1:
    # Search interface
    st.header("Search")
    search_query = st.text_area("Enter job description or required skills", value=st.session_state.search_query, height=100)

    if st.button("Search", key="search_button"):
        if search_query:
            with st.spinner("Searching for matching candidates..."):
                try:
                    all_results = similarity_search(search_query)
                    st.session_state.search_results = [result for result in all_results if result[4] == 1]  # Only available employees
                    st.session_state.search_query = search_query
                    st.session_state.messages = []  # Clear previous chat history
                except Exception as e:
                    st.error(f"An error occurred during the search: {str(e)}")
        else:
            st.warning("Please enter a job description or required skills to search.")

    # Display search results
    if st.session_state.search_results:
        st.header("Search Results")
        for idx, result in enumerate(st.session_state.search_results):
            with st.expander(f"{result[1]} - Match Score: {int(result[5] * 100)}%", expanded=False):
                col_result1, col_result2 = st.columns([2, 1])
                with col_result1:
                    st.subheader(result[1])
                    st.write(f"Department: {result[2]}")
                    with st.spinner("Analyzing skills..."):
                        missing_skills = analyze_missing_skills(search_query, result[3])
                        st.markdown('<div class="missing-skills">', unsafe_allow_html=True)
                        st.markdown("**Missing Skills:**")
                        if missing_skills.lower() == 'none':
                            st.success("No missing skills identified.")
                        else:
                            skills_list = missing_skills.split(", ")
                            for skill in skills_list:
                                st.markdown(f"- {skill}")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with col_result2:
                    chart = create_donut_chart(input_response=int(result[5] * 100), input_text="Match", input_color='green')
                    st.altair_chart(chart, use_container_width=True)

with col2:

    # Sidebar with current search info and clear button
    if st.button("Clear Search Results"):
        st.session_state.search_results = None
        st.session_state.search_query = ""
        st.session_state.messages = []
        st.rerun()

    messages = st.container(height=500)

    # Chat interface
    messages.header("Chat with AI about Candidates")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            messages.markdown(f'<div class="chat-message user"><div class="message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            messages.markdown(f'<div class="chat-message bot"><div class="message">{message["content"]}</div></div>', unsafe_allow_html=True)

    # Chat input
    if question := st.chat_input("Ask a question about the candidates"):
        st.session_state.messages.append({"role": "user", "content": question})
        messages.markdown(f'<div class="chat-message user"><div class="message">{question}</div></div>', unsafe_allow_html=True)

        if st.session_state.search_results:
            with st.spinner("Analyzing candidates and generating response..."):
                try:
                    response = generate_response(question=question, result=st.session_state.search_results, job_description=st.session_state.search_query)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    messages.markdown(f'<div class="chat-message bot"><div class="message">{response}</div></div>', unsafe_allow_html=True)
                except Exception as e:
                    st.toast(f"An error occurred while generating the response: {str(e)}")
        else:
            st.warning("Please perform a search first to chat about the candidates.")

