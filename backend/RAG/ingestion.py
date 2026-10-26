## Responsible for 1. Taking the documents. 2. Chunking 3. Embedding 4. ChromaDB

from pathlib import Path

from backend.logger import logging  ## for logging

from backend.managers.chroma_manager import add_to_collection, get_next_id  ## for storing vectors in chromadb

from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader   ## to process pdf doc
from langchain_text_splitters import RecursiveCharacterTextSplitter  ## Used for chunking


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR/ "data" / "raw"  ## Path to the raw data directory


### STEP 1: LOAD DOCS
def load_docs(filename: str = None):
    """Load documents from the raw data directory. If a filename is provided, load only that file; otherwise, load all PDF files in the directory."""
    if not RAW_DIR.is_dir():
        raise RuntimeError(
            f"Raw data directory not found at {RAW_DIR}. Please ensure the directory exists and contains PDF files."
        )

    pdf_files = []
    docx_files = []
    txt_files = []   
    docs = []
    
    if filename and filename.lower().endswith(".pdf"):
        pdf_files = [RAW_DIR / filename]
    elif filename and filename.lower().endswith(".docx"):
        docx_files = [RAW_DIR / filename]
    elif filename and filename.lower().endswith(".txt"):
        txt_files = [RAW_DIR / filename]
    else:
        # Recursively find all PDF files (case-insensitive)
        pdf_files = [file for file in RAW_DIR.rglob("*") 
                        if file.is_file() and file.suffix.lower() == ".pdf"]

    # Print the list of found PDF files
    for pdf in pdf_files:
        logging.info(f"Loading..: {pdf.name}")

        loader = PyPDFLoader(str(pdf))  ## PyPDFLoader reads the PDF and extracts text.

        docs.extend(loader.load())

    # Print the list of txt files 
    for docx in docx_files:
        logging.info(f"Loading..: {docx.name}")
    
        loader = Docx2txtLoader(str(docx))  ## TextLoader reads the DOCX file and extracts text.
    
        docs.extend(loader.load())    

    # Print the list of txt files 
    for txt in txt_files:
        logging.info(f"Loading..: {txt.name}")

        loader = TextLoader(str(txt))  ## TextLoader reads the TXT file and extracts text.

        docs.extend(loader.load()) 
           
    return docs


### STEP 2: SPLIT DOCS into Chunks
def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000, ##approx size of each chunk is 1000 characters. 
        ## This is a good size for embeddings and also for LLMs to process.
        chunk_overlap = 150
    )
    return splitter.split_documents(docs)


## STEP 3: STORE chunks in chromadb
def store_chunks(chunks, filename: str = None):
    """
    Store the provided chunks and their corresponding metadata in the ChromaDB collection.
    
    :param chunks: List of document chunks to store.
    :param filename: The name of the file from which the chunks were extracted.
    """
    next_id = get_next_id()
    text_documents = [doc.page_content for doc in chunks]
    metadatas = [{"source": filename} for i in range(len(text_documents))]  # Create metadata for each chunk
    ids = [f"chunk_{i}" for i in range(next_id, next_id + len(text_documents))]  # Generate unique IDs for each chunk
    add_to_collection(text_documents, metadatas, ids)


## STEP 4: MAIN INGESTION PIPELINE
def ingest_documents(filename: str = None):
    """
    Ingest documents from the data directory, split them into chunks, and store them in the ChromaDB collection.
    """

    if not filename:
        logging.info("No filename provided. Ingesting all documents in the data directory.")

    docs = []

    ## 1 load the md doc
    docs.extend(load_docs(filename))
    logging.info(f"Loaded {len(docs)} document pages.")

    ## 2. Split docs into Chunks
    chunks = split_docs(docs)
    logging.info(f"Split into {len(chunks)} chunks.")

    ## 4. Store vectors and chunk
    store_chunks(chunks, filename)

    logging.info(
        f"Processed {len(docs)} document pages "
        f"into {len(chunks)} chunks "
        f"and stored into ChromaDB."
    )
