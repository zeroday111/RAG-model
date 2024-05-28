# RAG-model
README for QA Application
Overview
This application provides a Question Answering (QA) system using a language model and a document retrieval system. Users can input queries through a graphical user interface (GUI), and the system will return answers along with the relevant source documents.

Features
Graphical User Interface (GUI): Built with Tkinter, allowing users to input queries and view results.
Model Integration: Uses HuggingFace embeddings and an Ollama language model for QA.
Document Retrieval: Retrieves relevant documents from a Chroma vector store.
Multithreading: Ensures the UI remains responsive by processing queries in a separate thread.
Customizable: Environment variables allow for easy customization of the model, embeddings, and other parameters.
Installation
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/qa-app.git
cd qa-app
Install dependencies:

sh
Copy code
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the project directory with the following content (modify as needed):

sh
Copy code
MODEL=tinyllama:latest
EMBEDDINGS_MODEL_NAME=all-MiniLM-L6-v2
PERSIST_DIRECTORY=db
TARGET_SOURCE_CHUNKS=4
SOURCE_DIRECTORY=source_documents
Usage
Running the QA Application
Start the QA application:

sh
Copy code
python qa_app.py
Enter your query in the text entry box and click "Submit".

View the answer and source documents in the respective text areas.

Ingesting Documents
To populate the document database for retrieval, run the ingestion script:

Prepare your documents: Place your documents in the source_documents directory. Supported formats are PDF, DOC, and DOCX.
Run the ingestion script:
sh
Copy code
python ingest_documents.py
This will process the documents, split them into chunks, and store their embeddings in the Chroma vector store.

Code Explanation
qa_app.py
This is the main file for the QA application.

Environment Variables: Loads configuration settings from environment variables.
QAApp Class: Manages the GUI and the QA system.
Widgets: Sets up the Tkinter widgets for user interaction.
Model Initialization: Initializes the embeddings, retriever, and QA chain.
Submit Query: Handles query submission, runs the QA process in a separate thread, and updates the UI with the results.
ingest_documents.py
This script processes and ingests documents into the Chroma vector store.

Load and Process Documents: Loads documents from the source_documents directory, splits them into chunks, and processes them for storage.
Vector Store Management: Checks if a vector store already exists and either appends new documents or creates a new vector store.
Constants
constants.py

Contains settings and configurations for the Chroma vector store.

Environment Variables
MODEL: Specifies the language model to use.
EMBEDDINGS_MODEL_NAME: Name of the embeddings model.
PERSIST_DIRECTORY: Directory to store the Chroma vector store.
TARGET_SOURCE_CHUNKS: Number of source document chunks to retrieve.
SOURCE_DIRECTORY: Directory containing the source documents to be ingested.
