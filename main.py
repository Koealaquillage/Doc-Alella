import streamlit as st
from Database_interface import DataBaseInterface
from FileTextLoader import FileTextLoader
from langchain_openai import OpenAI
#import secret_key
# Database Interface Setup
indexName = "alelladoc"
dbName = "Randomcuments"
collectionName = "collection_of_text_blobs"

TextLoader = FileTextLoader()

PineConeinterface = DataBaseInterface(indexName, st.secrets["openai_key"],
                                      st.secrets["pinecone_key"],
                                      st.secrets["mongodb_uri"], dbName,
                                      collectionName)

# Define a function to process the uploaded files
def process_files(files):
    if files:
        text_data_from_files = TextLoader.load_all_files(files)
        PineConeinterface.import_documents(text_data_from_files)
        return "Files processed successfully."
    return "No files to process."

# Define a function to query the database with a question
def query_question(question):
    documents = PineConeinterface.query_data(question)
    output1= analyze_documents(documents, question)
    return output1

def analyze_documents(documents, question):
    llm = OpenAI(openai_api_key=secret_key.openai_key,
                 model_name="gpt-4-turbo-mini",
                 temperature=0)
    as_output = ""
    for document in documents:
        as_output = as_output.join(document)
        query_to_ai = "Try to answer this question with the text you are provided".join(question)
        # You may want to use the OpenAI call here if needed
        # retriever_output = retriever_output.join(llm.invoke(query_to_ai.join(as_output)))

    return as_output

# Streamlit Interface
st.title("Question Answering App using Vector Search")

# File upload component
uploaded_files = st.file_uploader("Upload Files (TXT, PDF, DOCX)", accept_multiple_files=True, type=["txt", "pdf", "docx"])

# Button for processing files
if st.button("Process Files"):
    if uploaded_files:
        process_status = process_files(uploaded_files)
        st.success(process_status)
    else:
        st.warning("Please upload at least one file.")

# Input for text question
question = st.text_input("Enter your Question:")

# Button for querying the processed files
if st.button("Submit Question"):
    if question:
        output1 = query_question(question)
        st.text_area("File retrieved in the database", value=output1, height=200)
    else:
        st.warning("Please enter a question.")
