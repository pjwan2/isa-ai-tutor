from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel
import time

# Initialize FastAPI app
app = FastAPI(
    title="ISA - Intelligent Study Assistant API",
    description="Refined RAG Engine with Node-Level Filtering",
    version="1.4.0"
)

# Enable CORS for frontend communication (Streamlit or React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Data Model
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

# 1. Root Route: Redirects to /docs to avoid "Not Found" error
@app.get("/", include_in_schema=False)
async def root():
    """Redirects the user to the API documentation page."""
    return RedirectResponse(url="/docs")

# 2. Health Check: Verifies if the service is running
@app.get("/health", tags=["default"])
async def health_check():
    """Standard health check endpoint for Cloud Run."""
    return {"status": "healthy", "timestamp": time.time()}

# 3. Chat Stream: Optimized endpoint for LangGraph streaming
@app.post("/chat/stream", tags=["chat"])
async def chat_stream(request: ChatRequest):
    """
    Optimized streaming endpoint that filters out internal 
    LangGraph routing and auditing JSON.
    """
    async def event_generator():
        # Placeholder for your LangGraph/RAG logic
        # Replace this with your actual graph.astream() call
        response_text = f"Hello! I am your ISA mentor. You said: {request.message}"
        for word in response_text.split():
            yield f"data: {word} \n\n"
            time.sleep(0.1)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)