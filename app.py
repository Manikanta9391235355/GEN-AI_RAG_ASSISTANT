from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from rag import load_documents, retrieve

# Load environment variables
load_dotenv()

app = FastAPI()

# ✅ Enable CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def home():
    return {"message": "GenAI RAG Assistant is running 🚀"}

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load documents at startup
load_documents()

# In-memory session storage
sessions = {}

class ChatRequest(BaseModel):
    sessionId: str
    message: str


@app.post("/api/chat")
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        # Retrieve relevant chunks
        retrieved_results = retrieve(request.message)

        if not retrieved_results:
            return {
                "reply": "I don’t have enough information to answer that.",
                "tokensUsed": 0,
                "retrievedChunks": 0
            }

        # Extract context
        context = "\n\n".join([item[1]["content"] for item in retrieved_results])

        # Get conversation history
        history = sessions.get(request.sessionId, [])

        history.append({"role": "user", "content": request.message})

        # Keep last 6 messages (3 pairs)
        history = history[-6:]
        sessions[request.sessionId] = history

        conversation_history = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in history]
        )

        # Grounded prompt
        prompt = f"""
You are a helpful AI assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say you don't know.

Context:
{context}

Conversation History:
{conversation_history}

User Question:
{request.message}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content
        tokens_used = response.usage.total_tokens

        # Save assistant reply in memory
        sessions[request.sessionId].append({
            "role": "assistant",
            "content": reply
        })

        return {
            "reply": reply,
            "tokensUsed": tokens_used,
            "retrievedChunks": len(retrieved_results)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))