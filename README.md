# SemantiStore

SemantiStore is a web application designed to enable semantic search in large collections of documents. This project leverages advanced vector search techniques to retrieve relevant documents based on the meaning behind user queries, rather than simple keyword matching.

## Repository Structure

- **main.py**: The entry point of the application. This script contains the Gradio interface that connects the frontend with the backend functionalities.
- **Database_interface.py**: This file contains the `DatabaseInterface` class, which manages connections to the MongoDB and Pinecone databases, as well as document querying and uploading operations.
- **FileTextLoader.py**: This file contains the `FileTextLoader` class, responsible for handling file uploads and storing documents in the database in various formats (txt, doc, docx, pdf).

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/semantistore.git
   cd semantistore
