from backend.logger import logging

import chromadb
import re

from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
VECTOR_STORE_PATH = BACKEND_ROOT / "data" / "vector_store"  # Path to the vector store directory

# 1. Initialize persistent client
client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)  # Ensure this path exists and is writable

# 2. Create or get a collection
collection = client.get_or_create_collection(name="my_documents")

def add_to_collection(documents, metadatas, ids):
    """
    Add documents, metadata, and IDs to the ChromaDB collection.
    
    :param documents: List of document chunks to add.
    :param metadatas: List of metadata dictionaries corresponding to each document.
    :param ids: List of unique IDs for each document.
    """
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )


def get_all_documents():
    """
    Retrieve all documents from the ChromaDB collection.
    
    :return: List of all documents in the collection.
    """
    return collection.get()


def get_next_id():
    """
    Get the next available ID for a new document in the ChromaDB collection.
    
    :return: The next available ID.
    """
    # 1. Fetch all IDs from your collection
    response = collection.get(include=[])
    ids = response['ids']

    # 2. Extract numbers from IDs formatted like 'chunk_45'
    # Handles formats like 'chunk_45' or 'doc_name_chunk_45'
    chunk_numbers = []
    for doc_id in ids:
        match = re.search(r'chunk_(\d+)', doc_id)
        if match:
            chunk_numbers.append(int(match.group(1)))

    # 3. Find the highest ID
    if chunk_numbers:
        highest_chunk_num = max(chunk_numbers)
        return highest_chunk_num + 1
    else:
        return 0


def search_collection(input: str):
    """
    Search for documents in the ChromaDB collection based on input text.
    
    :param input: The search query.
    :return: List of documents matching the search query.
    """
    return collection.query(
        query_texts=[input],
        n_results=10
    )


def delete_by_filename(filename: str):
    """
    Delete documents from the collection based on filename.
    
    :param filename: The name of the file to delete.
    """
    try: 
        logging.info(f"Attempting to delete documents with metadata filter: {filename}")
        
        # Query to find IDs of documents matching the metadata filter
        results = collection.query(
            query_texts=[""],  # Empty query to get all documents
            n_results=10000,    # Adjust as needed
            where={"source": filename}
        )

        # Safe check to see if the inner list contains any results
        if not results or not results.get("ids") or len(results['ids'][0]) == 0:
            logging.info(f"No documents found matching the filter: {filename}")
            return
        else:
            logging.info(f"Found {len(results['ids'][0])} documents matching the filter: {filename}")
        
        # Extract IDs of documents to delete
        ids_to_delete = results['ids'][0]

        logging.info(f"Attempting to delete documents with IDs: {ids_to_delete} for filename: {filename}")
        
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} documents matching filter: {filename}")
        else:
            print("No documents found matching the filter.")
    except Exception as e:
        logging.error(f"Error deleting documents with filter {filename}: {e}")
        raise
