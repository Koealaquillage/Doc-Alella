from pymongo import MongoClient
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

class DataBaseInterface():

    __init__(self, dbName, collectionName, URI, OPENAI_key):
    self.collection = []
    self.dbName = dbName
    self.collectionName = collectionName
    self.URI = URI

    self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_key)
    self.collection = self._connect_to_DB()
    self.vectorStore = MongoDBAtlasVectorSearch(self.collection,
                                                self.embeddings)

    def _connect_to_DB(self):
        client = MongoClient(self.URI)
        self.collection = client[self.dbName][self.collectionName]
    
    def query_data(self, query):
    docs = self.vectorStore.similarity_search(query, K=1)
    as_output = docs[0].page_content

    llm = OpenAI(openai_api_key=self.OPENAI_key, temperature=0)
    retriever = self.vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.run(query)

    return as_output, retriever_output

    def load_txt_from_directory(self, directory):
        loader = DirectoryLoader(directory, glob = './*.txt',
                         show_progress = True)

        data = loader.load()

