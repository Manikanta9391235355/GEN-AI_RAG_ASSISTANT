🚀 GenAI RAG Assistant

A Retrieval-Augmented Generation (RAG) powered AI assistant built using FastAPI, Vector Search, and LLM integration.

This system retrieves relevant document chunks using embeddings and generates context-aware responses using a Large Language Model.

🏗 Architecture Diagram
                ┌─────────────────────┐
                │      User (UI)      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     FastAPI API     │
                │   (/api/chat)       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Embedding Model    │
                │ (Query → Vector)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Vector Store (DB)  │
                │ Similarity Search   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Retrieved Chunks   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     LLM Model       │
                │  (Prompt + Context) │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Generated Answer  │
                └─────────────────────┘
🔄 RAG Workflow Explanation

The system follows the Retrieval-Augmented Generation pipeline:

Step 1 — User Query

The user sends a message to /api/chat.

Step 2 — Query Embedding

The user message is converted into a vector embedding using an embedding model.

Step 3 — Similarity Search

The embedding is compared against stored document embeddings in the vector database using cosine similarity.

Step 4 — Context Retrieval

Top-K most relevant document chunks are retrieved.

Step 5 — Prompt Construction

The retrieved chunks are injected into a structured prompt template.

Step 6 — LLM Generation

The prompt is passed to the LLM, which generates a grounded response based on retrieved context.

Step 7 — Response Return

The API returns:

reply

tokensUsed

retrievedChunks

🧠 Embedding Strategy
Model Used

A transformer-based embedding model is used to convert both:

Documents

User queries

into dense vector representations.

Why Embeddings?

Embeddings allow semantic search instead of keyword matching.

Example:

User asks:

"How do I recover my password?"

System can match:

"Reset your password via Security Settings"

Even if wording is different.

Chunking Strategy

Documents are:

Split into fixed-size chunks

Overlap added (optional) to preserve context continuity

This improves retrieval accuracy.

🔍 Similarity Search Explanation

The system uses vector similarity (typically cosine similarity).

Cosine Similarity Formula
similarity = (A · B) / (||A|| ||B||)

Where:

A = Query embedding

B = Document embedding

Higher score → More semantically similar.

Why Top-K Retrieval?

Instead of retrieving a single document:

Top 3–5 chunks are retrieved

Improves answer grounding

Reduces hallucination

🧩 Prompt Design Reasoning

Prompt structure:

You are a helpful assistant.
Use the provided context to answer the question.
If the answer is not in the context, say you don't know.

Context:
{retrieved_chunks}

Question:
{user_question}
Why This Structure?

Prevents hallucinations

Forces grounding in retrieved documents

Encourages safe fallback behavior

Makes output deterministic and reliable

🛠 Tech Stack

Python

FastAPI

Uvicorn

Embedding Model (e.g. OpenAI / HuggingFace)

Vector Store (e.g. FAISS / ChromaDB)

LLM (OpenAI / Local model)

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone <your-repo-url>
cd genai-rag-assistant
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Set Environment Variables

Create .env file:

OPENAI_API_KEY=your_api_key_here
5️⃣ Run Backend
uvicorn app:app --reload

Open:

http://127.0.0.1:8000/docs
6️⃣ Test API

Use Swagger UI:

POST → /api/chat

Example Request:

{
  "sessionId": "123",
  "message": "How can I reset my password?"
}
📊 Example Response
{
  "reply": "You can reset your password from Settings > Security...",
  "tokensUsed": 101,
  "retrievedChunks": 1
}
