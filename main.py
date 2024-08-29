import gradio as gr
from gradio.themes.base import Base
from Database_interface import DataBaseInterface
from FileTextLoader import FileTextLoader
from langchain_openai import OpenAI
import secret_key

# Database Interface Setup
indexName = "alelladoc"
dbName = "Randomcuments"
collectionName = "collection_of_text_blobs"

TextLoader = FileTextLoader()


PineConeinterface = DataBaseInterface(indexName, secret_key.openai_key,
                                      secret_key.pinecone_key,
                                      secret_key.mongodb_uri, dbName,
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
    output1, output2 = analyze_documents(documents)
    return output1, output2

def analyze_documents(documents):
    llm = OpenAI(openai_api_key=secret_key.openai_key, temperature=0)
    as_output = ""
    retriever_output = "Synthetize this text: "
    for document in documents:
        as_output = as_output.join(document)
        retriever_output = retriever_output.join(llm(as_output))

    return as_output, retriever_output

# Gradio Interface
with gr.Blocks(theme=Base(), title="Question Answering App using Vector Search + RAG") as demo:
    gr.Markdown("# Question Answering App using Vector Search + RAG Architecture")
    
    # File upload component
    file_upload = gr.File(label="Upload Files (TXT, PDF, DOCX)", file_count="multiple", type="filepath")
    
    # Button for processing files
    process_button = gr.Button("Process Files", variant="primary")
    
    # Status output for file processing
    process_status = gr.Textbox(lines=1, max_lines=1, label="Processing Status")
    
    # Input for text question
    textbox = gr.Textbox(label="Enter your Question:")
    
    # Button for querying the processed files
    query_button = gr.Button("Submit Question", variant="secondary")
    
    # Output boxes for the query results
    with gr.Column():
        output1 = gr.Textbox(lines=1, max_lines=10, label="Output with just Atlas Vector Search")
        output2 = gr.Textbox(lines=1, max_lines=10, label="Output generated by Langchain Vector Search")

    # Connect the process button to the file processing function
    process_button.click(process_files, inputs=file_upload, outputs=process_status)
    
    # Connect the query button to the question answering function
    query_button.click(query_question, inputs=textbox, outputs=[output1, output2])

# Launch the app
demo.launch()
