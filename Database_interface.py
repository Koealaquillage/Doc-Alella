from pymongo import MongoClient
from langchain_community.document_loaders import DirectoryLoader, PDFLoader, DocxLoader
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

class DataBaseInterface:

    def __init__(self, dbName, collectionName, URI, OPENAI_key):
        self.collection = []
        self.dbName = dbName
        self.collectionName = collectionName
        self.URI = URI
        self.OPENAI_key = OPENAI_key  # Add this to store the OpenAI key

        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_key)
        self.collection = self._connect_to_DB()
        self.vectorStore = MongoDBAtlasVectorSearch(self.collection, self.embeddings)

    def _connect_to_DB(self):
        client = MongoClient(self.URI)
        return client[self.dbName][self.collectionName]  # Return the collection

    def query_data(self, query):
        docs = self.vectorStore.similarity_search(query, k=1)  # 'k' should be lowercase
        as_output = docs[0].page_content

        llm = OpenAI(openai_api_key=self.OPENAI_key, temperature=0)
        retriever = self.vectorStore.as_retriever()
        qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
        retriever_output = qa.run(query)

        return as_output, retriever_output

    def load_txt_files(self, files):
        data = []
        for file in files:
            with open(file.name, 'r') as f:
                data.append(f.read())
        return data

    def load_pdf_files(self, files):
        pdf_loader = PDFLoader()
        data = []
        for file in files:
            pdf_data = pdf_loader.load(file.name)
            data.extend(pdf_data)
        return data

    def load_docx_files(self, files):
        docx_loader = DocxLoader()
        data = []
        for file in files:
            docx_data = docx_loader.load(file.name)
            data.extend(docx_data)
        return data

    def load_all_files(self, files):
        txt_files = [file for file in files if file.name.endswith('.txt')]
        pdf_files = [file for file in files if file.name.endswith('.pdf')]
        docx_files = [file for file in files if file.name.endswith('.docx')]

        txt_data = self.load_txt_files(txt_files)
        pdf_data = self.load_pdf_files(pdf_files)
        docx_data = self.load_docx_files(docx_files)

        all_data = txt_data + pdf_data + docx_data
        return all_data
