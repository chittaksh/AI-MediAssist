# AI MediAssist

AI MediAssist is a document-grounded medical information assistant built with FastAPI, Streamlit, ChromaDB, LangChain, and Groq. Users can register or log in, upload PDF, DOCX, and TXT documents, and ask questions answered from the uploaded content.

> **Medical disclaimer:** This project is for educational and research purposes only. It does not provide medical advice, diagnosis, or treatment and must not replace a qualified healthcare professional.

## Features

- Streamlit-based login, registration, document management, and chat interface
- FastAPI backend with health, query, authentication, file, and ChromaDB endpoints
- Retrieval-augmented generation (RAG) over uploaded documents
- Persistent document vectors in ChromaDB
- SQLite-based user storage
- PDF, DOCX, and TXT ingestion with configurable chunk size and overlap
- Docker Compose setup for the API and web client

## Architecture

```text
Streamlit frontend -> FastAPI backend -> ChromaDB vector store
                                      -> Groq-hosted language model
                                      -> SQLite user database
```

The frontend is in `frontend/`, and the backend is in `backend/`. Uploaded documents are stored under `backend/data/raw`, while extracted vectors are stored under `backend/data/vector_store`.

## Prerequisites

- Docker and Docker Compose
- A Groq API key for answer generation

For local development without Docker, install Python 3.12 or newer.

## Configuration

Create a `.env` file in the project root before starting the Docker services:

```dotenv
GROQ_API_KEY=gsk_your_groq_api_key
MODEL_NAME=openai/gpt-oss-120b

FIRSTNAME=John
LASTNAME=Doe
USERNAME=johndoe
PASSWORD=johndoe
```

`MODEL_NAME` is optional and defaults to `openai/gpt-oss-120b`. The `FIRSTNAME`, `LASTNAME`, `USERNAME`, and `PASSWORD` values seed a default SQLite user. Authentication credentials are stored in plaintext for this prototype and should not be used as-is in production.

## Run with Docker Compose

```bash
docker compose up --build
```

Open:

- Web application: http://localhost:8501
- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs

Docker Compose persists application data in a named volume mounted at `/app/backend/data`.

To stop the services:

```bash
docker compose down
```

## Run Locally

From the project root, create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the backend from another terminal:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Start the frontend in a third terminal:

```bash
MEDIASSIST_API_URL=http://127.0.0.1:8000 streamlit run frontend/app.py
```

The Streamlit application will normally be available at http://localhost:8501.

## Usage

1. Open the Streamlit interface and log in with the seeded credentials, or register a new account.
2. Upload a PDF, DOCX, or TXT document from the sidebar. The upload limit is 50 MB.
3. Ask questions in the chat interface.
4. The backend retrieves relevant document chunks and passes them, with the question, to the configured Groq model.
5. Use the sidebar controls to manage uploaded files.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Check API status |
| `POST` | `/query` | Generate an answer from retrieved document context |
| `POST` | `/search-documents` | Search the ChromaDB collection |
| `POST` | `/users/login` | Authenticate a user |
| `POST` | `/users/register` | Register a user |
| `GET` | `/files/list` | List uploaded files |
| `POST` | `/files/upload` | Upload and ingest a document |
| `DELETE` | `/files/delete/{file_name}` | Remove an uploaded file and its vectors |
| `GET` | `/chromadb/documents` | Retrieve all stored ChromaDB documents |

Example question request:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"input":"What does the uploaded document say about the recommended treatment?"}'
```

## Project Structure

```text
backend/
  main.py                 # FastAPI application and route registration
  logger.py               # Logging configuration
  data/                   # Persistent application data
  managers/               # Authentication and ChromaDB management
  routers/                # API route modules
  RAG/                    # Document ingestion and response generation
frontend/
  app.py                  # Streamlit login page
  pages/                  # Registration and chat pages
Dockerfile.server          # FastAPI image
Dockerfile.client          # Streamlit image
docker-compose.yaml        # Multi-service runtime configuration
requirements.txt           # Python dependencies
```

## Development Notes

- The API creates the SQLite user table and default seed account when it starts.
- Uploaded text is split into chunks of approximately 1,000 characters with 150-character overlap.
- The current implementation expects document types supported by the configured loaders and does not require a separate ingestion command.
- The Docker client is configured by Compose to reach the API at `http://server:8000`; local clients use `http://127.0.0.1:8000` by default.

## License

No license has been specified for this project. Add a license file before distributing or publishing the code.
