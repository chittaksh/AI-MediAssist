# Requirement Understanding Document: MediAssist AI

**Project Title:** MediAssist AI – Enterprise Healthcare Agentic AI Copilot
**Target Environment:** Containerized Azure Cloud Hosting (Azure Container Apps)
**Document Type:** Requirement Understanding Document (RUD)

---

## 1. Project Executive Summary
**MediAssist AI** is an enterprise-grade Healthcare AI Copilot designed to unify multi-agent AI orchestration, multimodal understanding, enterprise retrieval systems (Advanced RAG), and standardized Model Context Protocol (MCP) integrations into a single platform. The platform simulates a real-world multi-branch hospital network assistant that streamlines information retrieval, automates clinical and operational workflows, and generates grounded clinical insights.

---

## 2. Business Problem & Solution Scope

### 2.1 Current Enterprise Challenges
* **Data Fragmentation & Silos:** Healthcare data spans unstructured SOPs, clinical PDFs, multimodal medical reports/prescriptions, and structured transactional records (e.g., electronic health records, billing systems).
* **Inefficient Operations:** Slow information retrieval and manual workflow management across multi-location hospital branches.
* **Interoperability Deficit:** Lack of a standardized protocol allowing AI systems to securely query enterprise databases and tool layers without direct, unmonitored database access.

### 2.2 Core Objective
To construct a unified, containerized Generative AI platform capable of handling operational lookup, complex multimodal analysis, analytical enterprise reasoning, and automated workflow execution across **~1.1 million structured data records** and unstructured enterprise documents.

---

## 3. Data Landscape & System Inputs

### 3.1 Provided Data Assets
* **Unstructured Documents:** PDF, DOCX, and TXT files covering Hospital SOPs, clinical workflow guidelines, compliance policies, discharge summaries, and operational manuals.
* **Multimodal Assets:** Scanned prescription images, sample medical reports, and lab result screenshots.
* **Structured PostgreSQL Database:** ~1.1M total records spanning a 20-branch enterprise hospital network:
  * **Patients:** 25,000 records
  * **Admissions:** 50,000 records
  * **Appointments:** 200,000 records
  * **Billing:** 100,000 records
  * **Prescriptions:** 250,000 records
  * **Lab Results:** 500,000 records
  * **Doctors:** 250 records
  * **Departments:** 25 records
  * **Insurance Policies:** 500 records
  * **Hospital Branches:** 20 records

---

## 4. User Personas & Core Use Cases

| User Persona | Key Capabilities & Responsibilities |
| :--- | :--- |
| **Doctor** | Summarize patient medical history, retrieve lab/radiology findings, check prescription records. |
| **Hospital Administrator** | Run cross-branch operational analytics, compliance monitoring, and department utilization summaries. |
| **Front Desk Staff** | Lookup patient records, verify schedules, handle multi-branch appointment inquiries. |
| **Insurance Team** | Review billing records, verify claims against active policy rules. |
| **Clinical Operations** | Execute workflow escalations, track admission trends, monitor department workloads. |

---

## 5. Architectural Principles & System Components

### 5.1 Architecture & Flow Diagram
```text
User → Streamlit UI
         │
         ▼
  FastAPI Backend
         │
         ▼
LangGraph Orchestrator
  ├── Planner Agent ─────────► Breaks query into subtasks
  ├── Retriever Agent ───────► FAISS / ChromaDB (RAG on SOPs/PDFs)
  ├── MCP Agent ─────────────► MCP Server ──► PostgreSQL DB (~1.1M records)
  └── Multimodal Agent ──────► Vision Models (BLIP / LLaVA)
         │
         ▼
  Reasoning Agent ───────────► Synthesizes multi-source context
         │
         ▼
  Evaluation Agent ──────────► LLM-as-a-Judge validation
         │
         ▼
   Final AI Response