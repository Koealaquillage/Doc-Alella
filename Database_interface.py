import pinecone
from langchain_community.llms import OpenAI

from langchain_openai import OpenAIEmbeddings
import fitz 
import mammoth 
import docx  

class DataBaseInterface:

    def __init__(self, index_name, OPENAI_key, pinecone_api_key, pinecone_environment):
        self.index_name = index_name
        self.OPENAI_key = OPENAI_key 

        # Initialize OpenAI Embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.OPENAI_key)

        # Initialize Pinecone
        pc = pinecone.Pinecone(api_key=pinecone_api_key)


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

    def load_txt_files(self, files):
        data = []
        for file in files:
            with open(file.name, 'r') as f:
                data.append(f.read())
        return data

    def load_pdf_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_pdf(file.name)
            data.append(text)
        return data

    def _extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def load_doc_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_doc(file.name)
            data.append(text)
        return data

    def _extract_text_from_doc(self, doc_path):
        with open(doc_path, "rb") as doc_file:
            result = mammoth.convert_to_text(doc_file)
            return result.value

    def load_docx_files(self, files):
        data = []
        for file in files:
            text = self._extract_text_from_docx(file.name)
            data.append(text)
        return data

    def _extract_text_from_docx(self, docx_path):
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def load_all_files(self, files):
        txt_files = [file for file in files if file.name.endswith('.txt')]
        pdf_files = [file for file in files if file.name.endswith('.pdf')]
        docx_files = [file for file in files if file.name.endswith('.docx')]
        doc_files = [file for file in files if file.name.endswith('.doc')]

        txt_data = self.load_txt_files(txt_files)
        pdf_data = self.load_pdf_files(pdf_files)
        docx_data = self.load_docx_files(docx_files)
        doc_data = self.load_doc_files(doc_files)

        all_data = txt_data + pdf_data + docx_data + doc_data
        return all_data

    def import_documents(self, files):
        # Load all data from files
        all_data = self.load_all_files(files)
        
        # Embed each document and store in Pinecone
        for i, text in enumerate(all_data):
            embedding = self.embeddings.embed_query(text)
            document_id = f"doc_{i}"
            self.index.upsert(vectors=[{"id": document_id,
                                        "values": embedding,
                                        "metadata": {"genre": "comedy", "year": 2020}}])
        
        print("Documents have been successfully imported into Pinecone.")
