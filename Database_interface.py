import pinecone
from bson import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from langchain_openai import OpenAIEmbeddings

class DataBaseInterface:

    def __init__(self, index_name, OPENAI_key,
                pinecone_api_key, mongo_URI, 
                mongo_db_name, mongo_collection_name):
        self.index_name = index_name
        self.OPENAI_key = OPENAI_key 

        # Initialize OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_key)

        # Initialize MongoDB
        self.mongo_URI = mongo_URI
        self.mongo_db_name = mongo_db_name
        self.mongo_collection_name = mongo_collection_name
        self.mongo_collection = self._connect_to_DB()

        # Initialize Pinecone
        self.pc_key = pinecone_api_key
        self.index = self._connect_to_pc()

    def _connect_to_DB(self):
        client = MongoClient(self.mongo_URI, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        return client[self.mongo_db_name][self.mongo_collection_name]

    
    def _connect_to_pc(self):
        pc = pinecone.Pinecone(api_key=self.pc_key)

        # Connect to or create the Pinecone index
        if self.index_name not in pc.list_indexes().names():
            pc.create_index(name=self.index_name,
                                        dimension=1536,
                                        metric='euclidean',
                                        spec=pinecone.ServerlessSpec(
                                        cloud='aws',
                                        region='us-west-2')
        )
        
        return pc.Index(self.index_name)



    def query_data(self, query, top_k=1):
        # Convert the query to an embedding
        query_embedding = self.embeddings.embed_query(query)
        # Perform similarity search in Pinecone
        result = self.index.query(vector=query_embedding,
                                  include_metadata=True, top_k=top_k)

        # Retrieve the corresponding documents from MongoDB
        if result['matches']:
            texts = []
            for match in result['matches']:
                mongo_id = match['metadata']['mongo_id']
                cursor = self.mongo_collection.find({"_id": ObjectId(mongo_id)})
                # Extract the text from the cursor

                for document in cursor:
                    
                    if 'text' in document:
                        try: 
                            texts.append(str.join(document['text']))
                        except: 
                            pass
        
            return texts  # Returning the list of texts
        else:
            return None

    def import_documents(self, text_data_from_files):
        
         for doc in text_data_from_files:
            # Insert document text into MongoDB
            mongo_result = self.mongo_collection.insert_one({"text": doc})
            mongo_id = mongo_result.inserted_id

            print("Document have been successfully imported into MongoDB.")
            # Generate embedding and store in Pinecone with MongoDB ID as metadata
            embedding = self.embeddings.embed_query(doc)
            self.index.upsert(vectors=[{"id": str(mongo_id),
                                        "values": embedding,
                                        "metadata": {"mongo_id": str(mongo_id)}}])

            print("Document have been successfully imported into Pinecone.")
