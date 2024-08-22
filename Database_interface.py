import pinecone
from langchain_community.llms import OpenAI
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings

class DataBaseInterface:

    def __init__(self, index_name, OPENAI_key,
                pinecone_api_key, pinecone_environment,
                mongo_URI, mongo_db_name, mongo_collection_name):
        self.index_name = index_name
        self.OPENAI_key = OPENAI_key 

        # Initialize OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_key)

        # Initialize MongoDB
        self.mongo_URI = mongo_URI
        self.mongo_db_name = mongo_db_name
        self.mongo_collection_name = mongo_collection_name

        # Initialize Pinecone
        self.pc_key = pinecone_api_key
        

         # Initialize MongoDB
        self.collection = _connect_to_DB()
        self.mongo_collection = client[self.mongo_db_name][self.mongo_collection_name]

     def _connect_to_DB(self):
        client = MongoClient(self.mongo_URI, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        return client[self.dbName][self.collectionName]
    
    def _connect_to_pc(self):
        pc = pinecone.Pinecone(api_key=self.pc_key)

        # Connect to or create the Pinecone index
        if self.index_name not in pc.list_indexes().names():
                pc.create_index(name='my_index', dimension=1536,
                                metric='euclidean',
                                spec=pinecone.ServerlessSpec(
                                    cloud='aws',
                                    region='us-west-2')
        )
        else:
            self.index = pc.Index(self.index_name)

    def query_data(self, query, top_k=1):
        # Convert the query to an embedding
        query_embedding = self.embeddings.embed_query(query)

        # Perform similarity search in Pinecone
        result = self.index.query(queries=[query_embedding], top_k=top_k)

        # Retrieve the most relevant document
        if result and result['matches']:
            match = result['matches'][0]
            document_id = match['id']
            document = self.index.fetch(ids=[document_id])
            as_output = document['results'][document_id]['text']

            # Use OpenAI to generate an answer
            llm = OpenAI(openai_api_key=self.OPENAI_key, temperature=0)
            retriever_output = llm(as_output)

            return as_output, retriever_output
        else:
            return None, "No documents found."

    def import_documents(self, text_data_from_files):
        
        # Embed each document and store in Pinecone
        for i, text in enumerate(text_data_from_files):
            embedding = self.embeddings.embed_query(text)
            document_id = f"doc_{i}"
            self.index.upsert(vectors=[{"id": document_id,
                                        "values": embedding,
                                        "metadata": {"genre": "comedy", "year": 2020}}])
        
        print("Documents have been successfully imported into Pinecone.")
