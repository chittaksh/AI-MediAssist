# Project Milestone & Sprint Tracker (6-Week Accelerated Plan)

**Project Name:** MediAssist AI – Enterprise Healthcare Agentic AI Copilot  
**Project Lifecycle:** 6 Weeks Accelerated Delivery Plan  
**Target Host:** Azure Container Apps  
**Document Version:** 2.0  

---

## 1. Accelerated Lifecycle Strategy & Weekly Overview

To deliver the MediAssist AI platform within a **6-week timeline**, tasks are condensed into high-velocity weekly sprints combining ingestion, tool integration, agent orchestration, evaluation, and cloud deployment.

| Week / Sprint | Focus Domain | Key Functional Deliverables & Tasks | Target Milestone Output |
| :--- | :--- | :--- | :--- |
| **Week 1** | **Project Setup, Ingestion & RAG** | VS Code repo scaffolding, Unified Document Parser (PDF/DOCX/TXT), chunking/embedding strategy, FAISS/ChromaDB indexing, FastAPI RAG endpoints. | **RAG Pipeline Baseline** |
| **Week 2** | **PostgreSQL & MCP Server Layer** | PostgreSQL schema & ~1.1M records provisioning, Python MCP SDK Server, parameterized tools (`get_patient_history`, `get_appointments`, `get_lab_results`, `get_billing_summary`). | **Secure MCP Tool Layer** |
| **Week 3** | **Multimodal Vision Processing** | Medical image ingestion (JPG/PNG/JPEG), Vision-Language Models (BLIP / LLaVA) for OCR and entity extraction, LangGraph Vision Agent. | **Multimodal Engine** |
| **Week 4** | **LangGraph Multi-Agent Orchestration** | Central Supervisor graph, Planner Agent (subtask decomposition), Retriever Agent, MCP Agent, Reasoning Agent context synthesis, multi-turn state. | **Agent Orchestrator** |
| **Week 5** | **Evaluation, Guardrails & Streamlit UI** | LLM-as-a-Judge Evaluation Agent (Faithfulness, Grounding, Hallucination Risk), LangSmith tracing, safety guardrails, Streamlit chat interface & dashboard. | **Full Application Baseline** |
| **Week 6** | **Dockerization & Azure Cloud Deployment** | Multi-container Docker Compose configuration, Azure Container Apps hosting, end-to-end performance benchmarking (<15s response latency), repository packaging. | **Production Cloud Release** |

---

## 2. Detailed Weekly Task Backlogs & Acceptance Criteria

### Week 1: Environment Setup & Enterprise RAG Pipeline
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-101** | Setup Project Structure & Repository | Project Layout | Initialize `App/`, `Data/`, `Project_documents/`, `README.md`, `requirements.txt`, `.env`. | 3 |
| **TSK-102** | Build Unified Document Parser | FR-003, FR-005 | Support PDF, DOCX, TXT uploads up to 50MB with clean text extraction and metadata tags. | 5 |
| **TSK-103** | Chunking & Embedding Pipeline | FR-005 | Configure chunk size/overlap reasoning; generate Hugging Face embeddings. | 5 |
| **TSK-104** | Vector Store Indexing & Retrieval | FR-006 | Index chunks in FAISS / ChromaDB with semantic search, similarity score output, and top-$k$ reranking. | 5 |
| **TSK-105** | FastAPI RAG Endpoints | FR-016, NFR-003 | Implement `POST /upload-document`, `POST /retrieve-chunks`, and `GET /health`. | 5 |

### Week 2: PostgreSQL Database & MCP Server Integration
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-201** | Database Provisioning (~1.1M Records) | FR-011 | Provision PostgreSQL schema across 10 tables (Patients, Appointments, Billing, Labs, Branches, etc.). | 5 |
| **TSK-202** | Build Python MCP Protocol Server | FR-009 | Setup MCP Python SDK server ensuring direct raw DB access by AI agents is strictly prohibited. | 5 |
| **TSK-203** | Expose Parameterized Healthcare Tools | FR-009, FR-010 | Implement `get_patient_history()`, `get_appointments()`, `get_lab_results()`, `get_billing_summary()`. | 8 |
| **TSK-204** | Tool Execution & Security Validation | FR-010 | Validate secure structured data retrieval and parameter passing through the MCP layer. | 5 |

### Week 3: Multimodal Processing & Vision Agent
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-301** | Medical Image Ingestion Pipeline | FR-004 | Support JPG, PNG, JPEG uploads for prescriptions, lab report screenshots, and scanned documents. | 5 |
| **TSK-302** | Vision Model Integration (BLIP / LLaVA) | FR-008 | Extract structured information (medicines, diagnoses, dates, observations) from images. | 8 |
| **TSK-303** | Build LangGraph Vision Agent Node | FR-008, Module 3 | Integrate OCR and vision extraction node into the central agentic workflow graph. | 5 |

### Week 4: LangGraph Multi-Agent Orchestration
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-401** | Supervisor Graph Architecture | Module 3, FR-016 | Build central LangGraph state machine orchestrating Planner, Retriever, MCP, Vision, and Reasoning Agents. | 8 |
| **TSK-402** | Implement Planner Agent Node | FR-007 | Decompose complex multi-step user queries into structured subtask execution plans. | 5 |
| **TSK-403** | Connect MCP & Retriever Agent Nodes | FR-006, FR-010 | Wire state graph to vector retrieval pipelines and MCP database tools. | 5 |
| **TSK-404** | Implement Reasoning Agent Node | FR-012 | Synthesize multi-source context (RAG chunks + DB records + vision output) into grounded responses with citations. | 8 |
| **TSK-405** | Multi-turn Session State Management | FR-014 | Preserve conversation history and multi-turn context continuation across chat prompts. | 3 |

### Week 5: Evaluation Framework, Guardrails & Streamlit UI
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-501** | LLM-as-a-Judge Evaluation Agent | FR-013 | Implement automated scoring for Faithfulness, Grounding, Answer Relevance, and Hallucination Risk. | 8 |
| **TSK-502** | LangSmith Observability Tracing | NFR-004, NFR-005 | Track agent execution graphs, API latencies, token consumption, and evaluation metrics. | 5 |
| **TSK-503** | Safety Guardrails & Output Filters | Module 7 | Implement prompt injection detection, PII protection, and unsafe clinical recommendation checks. | 5 |
| **TSK-504** | Streamlit UI Chat & Dashboards | FR-002, FR-015 | Build chat interface, streaming responses, PDF/image upload components, and observability dashboards. | 8 |

### Week 6: Dockerization & Azure Cloud Deployment
| Task ID | User Story / Technical Task | FSD Ref / Module | Acceptance Criteria & Subtasks | Est. Pts |
| :--- | :--- | :--- | :--- | :--- |
| **TSK-601** | Multi-Container Docker Configuration | Module 8, NFR-002 | Create Dockerfiles for FastAPI, Streamlit, and MCP Server; configure `docker-compose.yml`. | 5 |
| **TSK-602** | Azure Container Apps Deployment | Module 9, FR-016 | Deploy containerized services to Azure Container Apps and configure public-facing endpoints. | 8 |
| **TSK-603** | End-to-End Testing & Benchmarking | NFR-008 | Verify sub-15s response latencies, query accuracy, and edge-case resilience. | 5 |
| **TSK-604** | Repository Packaging & Handover | Deliverables 1-5 | Finalize GitHub repo, Architecture Documentation, Evaluation Report, and Live Demo video. | 5 |