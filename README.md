# SemantiStore

SemantiStore is a web application designed to enable semantic search in large collections of documents. This project leverages advanced vector search techniques to retrieve relevant documents based on the meaning behind user queries, rather than simple keyword matching.

## Repository Structure

- **main.py**: The entry point of the application. This script contains the streamlit interface that connects the frontend with the backend functionalities.
- **Database_interface.py**: This file contains the `DatabaseInterface` class, which manages connections to the MongoDB and Pinecone databases, as well as document querying and uploading operations.
- **FileTextLoader.py**: This file contains the `FileTextLoader` class, responsible for handling file uploads and storing documents in the database in various formats (txt, doc, docx, pdf).

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/semantistore.git
   cd semantistore

## Copyrights and Ownership

### License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** License. This means that:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial**: You may not use the material for commercial purposes without explicit permission from the author.

### Summary

You are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material.

Under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial**: You may not use the material for commercial purposes.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

### Full License Text

For full details, you can view the license here: [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

### Ownership

The code and intellectual property of this project are owned by **Guillaume Koenig**. While you are welcome to use and modify the project for non-commercial purposes, commercial exploitation requires prior permission from the owner.
