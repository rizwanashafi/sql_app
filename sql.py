from dotenv import load_dotenv
import os
import sqlalchemy as sa
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()  # Clean the response

def read_sql_query(sql, db_url):
    try:
        engine = sa.create_engine(db_url)
        with engine.connect() as connection:
            result = connection.execute(sql)
            rows = result.fetchall()
        return rows
    except Exception as e:
        st.error(f"Database error: {e}")
        return []

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.
    \nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    The SQL code should not have ``` in beginning or end and SQL word in output.
    """
]

# Streamlit App
st.set_page_config(page_title="SQL Query Retriever")
st.header("📊 Retrieve SQL Database App")

# Sidebar Inputs
st.sidebar.header("Database Connection Settings")
host = st.sidebar.text_input("Database Host (e.g., 127.0.0.1):", key="host")
port = st.sidebar.text_input("Database Port (e.g., 3306):", key="port")
username = st.sidebar.text_input("Database Username (e.g., root):", key="username")
password = st.sidebar.text_input("Database Password (e.g., root):", type="password", key="password")
database = st.sidebar.text_input("Database Name (e.g., students):", key="database")

# Main Area Input
# st.sidebar.header("Ask a Question")
question = st.text_input("Input your question:", key="input")
submit = st.button("Ask any question")

if submit:
    if host and port and username and password and database and question:
        # Construct the database URL
        db_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        
        # Generate SQL query from the question
        response = get_gemini_response(question, prompt)
        st.subheader("Generated SQL Query:")
        st.code(response)
        
        # Execute the query and display results
        response_data = read_sql_query(response, db_url)
        st.subheader("Query Results:")
        if response_data:
            for row in response_data:
                st.write(row)
        else:
            st.write("No results or error in query execution.")
    else:
        st.warning("Please enter all the required fields and a question.")
