#!/usr/bin/env python3

import os
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from threading import Thread

# Load environment variables with defaults
MODEL = os.environ.get("MODEL", "tinyllama:latest")
EMBEDDINGS_MODEL_NAME = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
PERSIST_DIRECTORY = os.environ.get("PERSIST_DIRECTORY", "db")
TARGET_SOURCE_CHUNKS = int(os.environ.get("TARGET_SOURCE_CHUNKS", 4))

class QAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QA App")

        self.create_widgets()
        self.initialize_model()

    def create_widgets(self):
        # Query label and entry
        self.query_label = tk.Label(self.root, text="Enter your query:")
        self.query_label.pack(pady=5)
        
        self.query_entry = tk.Entry(self.root, width=80)
        self.query_entry.pack(pady=5)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_query)
        self.submit_button.pack(pady=5)

        # Result display
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=20)
        self.result_text.pack(pady=5)

        # Source display
        self.source_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=10)
        self.source_text.pack(pady=5)

        # Hide sources checkbox
        self.hide_source_var = tk.BooleanVar()
        self.hide_source_check = tk.Checkbutton(self.root, text="Hide sources", variable=self.hide_source_var)
        self.hide_source_check.pack(pady=5)

    def initialize_model(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL_NAME)
        self.db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=self.embeddings)
        self.retriever = self.db.as_retriever(search_kwargs={"k": TARGET_SOURCE_CHUNKS})
        self.llm = Ollama(model=MODEL)
        self.qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)

    def submit_query(self):
        query = self.query_entry.get()
        if not query.strip():
            messagebox.showwarning("Warning", "Query cannot be empty!")
            return

        # # Display confirmation message
        # messagebox.showinfo("Confirmation", "Query submitted successfully!")
        
        # Clear the query entry box
        self.query_entry.delete(0, tk.END)

        # Display the query in the result box
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Question: {query}\n\nProcessing...\n")

        # Clear the source text box
        self.source_text.delete(1.0, tk.END)

        # Run the QA in a separate thread to keep the UI responsive
        Thread(target=self.get_answer, args=(query,)).start()

    def get_answer(self, query):
        start_time = time.time()
        response = self.qa(query)
        answer = response['result']
        source_docs = response['source_documents'] if not self.hide_source_var.get() else []

        # Update the result text box with the answer
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Question: {query}\n\nAnswer:\n{answer}\n")
        self.result_text.insert(tk.END, f"\nResponse Time: {time.time() - start_time:.2f} seconds")

        # Update the source text box with the source documents
        if source_docs:
            for doc in source_docs:
                self.source_text.insert(tk.END, f"{doc.metadata['source']}:\n{doc.page_content}\n\n")

def main():
    root = tk.Tk()
    app = QAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
