# from dotenv import load_dotenv
# import os
# import sqlite3
# import streamlit as st
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure Genai Key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
#     return response.text.strip()  # Clean the response

# def read_sql_query(sql, db):
#     try:
#         conn = sqlite3.connect(db)
#         cur = conn.cursor()
#         cur.execute(sql)
#         rows = cur.fetchall()
#         conn.close()
#         return rows
#     except sqlite3.Error as e:
#         st.error(f"Database error: {e}")
#         return []

# # Define Your Prompt
# prompt = [
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.
#     \nFor example,\nExample 1 - How many entries of records are present?, 
#     the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
#     \nExample 2 - Tell me all the students studying in Data Science class?, 
#     the SQL command will be something like this SELECT * FROM STUDENT 
#     where CLASS="Data Science"; 
#     The SQL code should not have ``` in beginning or end and SQL word in output.
#     """
# ]

# # Streamlit App
# st.set_page_config(page_title="SQL Query Retriever")
# st.header("📊Retrieve SQL Database App")

# question = st.text_input("Input: ", key="input")
# submit = st.button("Ask any question")

# if submit:
#     if question:
#         response = get_gemini_response(question, prompt)
#         st.subheader("Generated SQL Query:")
#         st.code(response)
        
#         # Execute the query and display results
#         response_data = read_sql_query(response, "student.db")
#         st.subheader("Query Results:")
#         if response_data:
#             for row in response_data:
#                 st.write(row)
#         else:
#             st.write("No results or error in query execution.")
#     else:
#         st.warning("Please enter a question.")


from dotenv import load_dotenv
import os
import sqlalchemy as sa
import streamlit as st
import google.generativeai as genai
from langchain import SQLDatabase

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

# Inputs
db_url = st.text_input("Database URL (e.g., mysql+pymysql://root:root@127.0.0.1/students):", key="db_url")
question = st.text_input("Input your question:", key="input")
submit = st.button("Ask any question")

if submit:
    if db_url and question:
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
        st.warning("Please enter both the database URL and a question.")
