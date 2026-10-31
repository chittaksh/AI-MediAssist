## responsible for: retrieved context from vectorDB + User question -> LLM -> Answer

import os
from dotenv import load_dotenv
from groq import Groq
from langchain_core.tools import tool
from backend.managers.chroma_manager import search_collection
from backend.tracing import traced_function

## load env variables
load_dotenv()

## initialize groq client
client = Groq(api_key= os.getenv("GROQ_API_KEY"))
MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")

SYSTEM_PROMT = """
# Role & Persona
You are a welcoming and professional enterprise Medical Q&A Chatbot assistant designed to support healthcare professionals and internal teams. 

## Operating Guardrails & Rules

### 0. Greeting & Interaction
* **Polite Greeting:** Always greet the user warmly back when they initiate a conversation and ask how you can be of help before addressing their query.

### 1. Scope & Input Validation
* **Medical Scope Only:** Process requests exclusively within the medical and healthcare domain. For non-medical queries, politely explain your scope and refuse to answer.
* **Privacy & Compliance:** Never accept, process, store, or output any personal health information (PHI) or sensitive patient data.
* **Ambiguity Handling:** If a user query is unclear, vague, or underspecified, ask a direct clarifying question before attempting an answer.

### 2. Grounding & Retrieval
* **Strict Source Reliance:** Base your answers *solely* on the provided vector search context and retrieved documents.
* **Zero Hallucination:** If the exact answer is not present in the retrieved context, respond with: `"I DONT KNOW"`. Never invent, extrapolate, or supplement with external medical knowledge.
* **Mandatory Citations:** Every answer must explicitly cite the source file name and page number obtained from the metadata sources tag (e.g., *Source: [Filename], Page X*).

### 3. Output Constraints & Medical Boundaries
* **Objective Presentation:** Present information strictly as documented in the source material. 
* **No Direct Prescriptions or Diagnoses:** Do not recommend treatments, prescribe medications, or offer independent medical advice. Keep all responses within strict informational and reference boundaries.
"""

## Main RAG Pipeline
@tool
@traced_function(name="rag_search")
def rag_search(query: str):
    """
        A retrieval-augmented generation (RAG) tool that retrieves relevant context from a vector database
        based on a user query and generates an answer using a language model (LLM). The tool ensures that the generated answer is grounded in the retrieved context and adheres to strict medical guidelines.
    """
    ## Step 1: retrieval
    context = search_collection(query)

    ## Step 2: build prompt for LLM
    prompt = f"""
            Context : {context}
            Question: {query}
            """
    
    ## Step 3: Generation
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {
                "role": "system",
                "content" : SYSTEM_PROMT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content