# Enterprise Architecture Breakdown Document

**System Name:** MediAssist AI – Enterprise Healthcare Agentic AI Copilot  
**Target Environment:** Containerized Microservices on Azure Cloud Hosting  
**Document Version:** 1.0  

---

## 1. Executive Summary & Architectural Overview

The **MediAssist AI** architecture is engineered as an enterprise-grade, agentic AI platform designed for multi-branch healthcare environments. It bridges unstructured hospital knowledge bases (SOPs, medical records, clinical guidelines) and structured transactional databases (EHR, appointments, lab results, billing) via standardized tool execution layers and intelligent multi-agent orchestration.

### Core Architecture Pillars
1. **Decoupled User & Service Layer:** High-performance FastAPI backend gateway serving an interactive Streamlit UI.
2. **Agentic Orchestration (LangGraph Supervisor):** Dynamic task decomposition, routing, execution, and evaluation managed by specialized autonomous agents.
3. **Model Context Protocol (MCP) Integration:** Secure, protocol-driven tool execution separating LLM agents from direct database connections.
4. **Multimodal & RAG Intelligence:** Vision models for image extraction combined with hybrid vector search and reranking pipelines.
5. **Enterprise Observability & Guardrails:** End-to-end tracing via LangSmith, hallucination scoring, and safety output guardrails.

---

## 2. High-Level Architecture Diagram

```text
┌────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                │
│                   Doctors  │  Admin Staff  │  Insurance                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                             FRONTEND UI                                │
│                            Streamlit App                               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST APIs
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                           BACKEND GATEWAY                              │
│                            FastAPI Backend                             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     LANGGRAPH CENTRAL SUPERVISOR                       │
│                                                                        │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────────┐  │
│  │ Planner Agent  │  │ Retriever Agent│  │        MCP Agent         │  │
│  │ (Task Decomp.) │  │ (Vector Search)│  │ (Tool Execution/Queries) │  │
│  └───────┬────────┘  └───────┬────────┘  └────────────┬─────────────┘  │
│          │                   │                        │                │
│  ┌───────┴────────┐  ┌───────┴────────┐  ┌────────────┴─────────────┐  │
│  │ Vision Agent   │  │ Reasoning Agent│  │ Evaluator & Response Ag. │  │
│  │ (OCR/Extraction)│ │ (Context Syn.) │  │ (Safety/Quality/Guard)   │  │
│  └────────────────┘  └────────────────┘  └──────────────────────────┘  │
└───────┬──────────────────────┬────────────────────────┬────────────────┘
        │                      │                        │
        ▼                      ▼                        ▼
┌───────────────┐      ┌───────────────┐        ┌───────────────┐
│ VECTOR STORE  │      │  MCP SERVER   │        │ LLM ENGINES   │
│ FAISS/ChromaDB│      │  PostgreSQL   │        │ OpenAI / Groq │
└───────┬───────┘      └───────┬───────┘        └───────┬───────┘
        │                      │                        │
        └──────────────────────┼────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     INGESTION & OBSERVABILITY                          │
│     Ingestion Pipeline (Upload/Chunk/Embed)  │  LangSmith Tracing     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Layer-by-Layer Architectural Component Breakdown

### 3.1 User & Frontend Layer
* **Target Users:** Doctors, Hospital Administrative Staff, Front Desk Staff, Insurance Verification Teams, and Clinical Operations Teams.
* **Frontend Application (Streamlit App):** Provides a responsive conversational chat interface (FR-002), document upload components for SOP PDFs (FR-003), image upload for prescriptions/lab reports (FR-004), and evaluation/observability dashboards (FR-015).

### 3.2 Backend Gateway & API Layer
* **API Framework (FastAPI):** Serves as the secure, high-throughput microservice gateway orchestrating API calls between the Streamlit UI and the LangGraph Multi-Agent network.
* **Core API Contracts:** The API layer exposes strict functional contracts:

| HTTP Method | Endpoint Contract | Functional Purpose & Payload |
| :--- | :--- | :--- |
| `POST` | `/upload-document` | Upload healthcare documents (PDF/DOCX/TXT up to 50MB) and trigger ingestion pipeline. |
| `POST` | `/retrieve-chunks` | Execute vector similarity search and extract top-k semantic document chunks with scores. |
| `POST` | `/chat` | Primary conversational chatbot endpoint connecting UI inputs with LangGraph agent graph. |
| `GET` | `/health` | API health check monitoring operational status of backend services and database connectors. |

### 3.3 Multi-Agent Orchestration Layer (LangGraph Supervisor)
The central state machine orchestrates specialized AI agents to execute complex user queries:

| Agent Component | Architectural Responsibilities & Subtasks |
| :--- | :--- |
| **Planner Agent (FR-007)** | Decomposes complex user requests into structured, execution-ready subtasks (e.g., separating report analysis, patient history retrieval, and schedule checks). |
| **Retriever Agent (FR-006)** | Queries vector databases, executes similarity searches, scores semantic chunks, and applies reranking strategies on SOPs and manuals. |
| **MCP Agent (FR-010)** | Dynamically invokes MCP tools to retrieve structured enterprise data from PostgreSQL without raw DB access. |
| **Vision Agent (FR-008)** | Executes OCR, image analysis, and information extraction (medicines, diagnoses, dates, observations) from prescriptions and lab images. |
| **Reasoning Agent (FR-012)** | Fuses multi-source context (vector chunks, PostgreSQL records, vision outputs, prompt) into a grounded summary with source attribution. |
| **Evaluator & Response Agent (FR-013)** | Performs LLM-as-a-Judge validation for faithfulness, grounding, relevance, and hallucination scoring before applying output guardrails. |

### 3.4 Ingestion & Advanced RAG Pipeline
* **Unified Document Loader:** Multi-format document parser accepting PDF, DOCX, and TXT files up to 50 MB.
* **Chunking Strategy:** Configured chunk size and overlap to preserve contextual semantic boundaries while avoiding context window overflow.
* **Embeddings & Vector Store:** Vector storage powered by FAISS or ChromaDB utilizing Hugging Face embedding models.
* **Retrieval Pipeline:** Query-to-embedding conversion, top-k chunk retrieval with similarity scoring, and reranking strategy for relevance optimization.

### 3.5 Data Storage, MCP Protocol & LLM Integration
* **Model Context Protocol (MCP) Server:** Direct database access by AI agents is strictly prohibited (FR-009). All requests route through a Python MCP SDK server exposing standardized tool functions (e.g., `get_patient_history()`, `get_appointments()`, `get_lab_results()`, `get_billing_summary()`).
* **PostgreSQL Database:** Stores ~1.1M records across 10 tables (Patients, Admissions, Appointments, Billing, Prescriptions, Lab Results, Doctors, Departments, Insurance Policies, Hospital Branches) covering 20 multi-location branches.
* **LLM Engine Processing:** OpenAI and Groq APIs providing multi-model reasoning and fast inference execution.
* **Observability & Tracing:** Integrated LangSmith tracing framework monitoring execution graphs, latency, token usage, and hallucination rates.

---

## 4. Functional Specification & User Story Mapping

| Module / Role | FSD Requirement & User Story | Architectural Implementation |
| :--- | :--- | :--- |
| **Doctor** | **US-001:** Upload discharge summary & retrieve patient history for recommendations. | Streamlit PDF upload $\rightarrow$ Ingestion Pipeline $\rightarrow$ Multimodal/MCP Agent $\rightarrow$ Reasoning Agent. |
| **Administrator** | **US-002:** Search compliance policies for audit queries. | Streamlit text search $\rightarrow$ Retriever Agent $\rightarrow$ FAISS/ChromaDB RAG search $\rightarrow$ Grounded response. |
| **Front Desk Staff** | **US-003:** Retrieve appointment information quickly. | Chat interface $\rightarrow$ Planner Agent $\rightarrow$ MCP Agent (`get_appointments`) $\rightarrow$ PostgreSQL query. |
| **Insurance Team** | **US-004:** Verify billing and policy information for claims. | Chat interface $\rightarrow$ MCP Agent (`get_billing_summary` & `get_insurance_details`) $\rightarrow$ Grounded output. |

---

## 5. Production Repository & Folder Layout

The codebase adheres to a modular, production-ready project structure:

```text
MediAssist-AI/
├── README.md                   # System overview & installation instructions
├── requirements.txt            # Production Python dependencies
├── .env                        # Environment configurations & API credentials
├── App/                        # Application Source Code
│   ├── Frontend/               # Streamlit web application interface
│   │   └── app.py
│   ├── Backend/                # FastAPI backend service & router handlers
│   │   ├── main.py
│   │   ├── routers/
│   │   └── schemas/
│   ├── Agents/                 # LangGraph agent definitions & supervisor graph
│   │   ├── supervisor.py
│   │   ├── planner.py
│   │   ├── mcp_agent.py
│   │   ├── retriever_agent.py
│   │   ├── vision_agent.py
│   │   └── evaluator_agent.py
│   ├── MCP_Server/             # MCP Protocol server & PostgreSQL tool connectors
│   │   ├── server.py
│   │   └── db_tools.py
│   ├── RAG/                    # Ingestion parser, vector store & reranking
│   │   ├── ingestion.py
│   │   ├── vector_store.py
│   │   └── reranker.py
│   └── Config/                 # Application configuration & prompts
├── Data/                       # Data persistence directory
│   ├── Raw_data/               # SOPs, compliance PDFs, text manuals
│   ├── Images/                 # Prescriptions, lab reports, screenshots
│   ├── Processed/              # Extracted JSONs & parsed text artifacts
│   └── Vector_store/           # Local FAISS / ChromaDB index persistent storage
└── Project_documents/          # Project documentation repository
    ├── Requirement/            # Functional Specs (FSD) & Requirement Documents
    ├── Architecture/           # System Architecture diagrams & breakdown docs
    ├── Tracker/                # Sprint milestones & development trackers
    └── Technical_document/     # API contracts, RAG specs, and LLM-as-a-Judge docs
```

---

## 6. Non-Functional & System Requirements

* **NFR-001 (Modular Architecture):** Microservice-based separation between UI, Backend API, Agent Graph, and MCP Server.
* **NFR-002 (Dockerized Deployment):** Complete containerization using Docker and Docker Compose for Azure Container Apps hosting.
* **NFR-003 (API-First Design):** RESTful API contract design enforcing strict OpenAPI schemas.
* **NFR-004 & NFR-005 (Logging & Observability):** Comprehensive trace logging, token metrics, and execution graphs via LangSmith.
* **NFR-006 (Config-Driven Architecture):** Externalized environment settings and dynamic prompt template management.
* **NFR-007 (Error Handling & Resiliency):** Circuit breakers, retry mechanisms, and graceful fallback handling across tool calls.
* **NFR-008 (Scalable Retrieval Pipeline):** Sub-15 second end-to-end response times (FR-002) with optimized top-k reranking.