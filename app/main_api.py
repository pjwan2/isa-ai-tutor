import os
import uvicorn
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, BaseMessage
from main import create_isa_app

app = FastAPI(
    title="ISA - Intelligent Study Assistant API",
    description="Refined RAG Engine with Node-Level Filtering",
    version="1.4.0"
)

# Global singleton: Loading 2,244 knowledge chunks into memory
print("[*] Booting Knowledge Engine...")
isa_graph = create_isa_app()
print("[*] ISA Engine Online.")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.4.0"}

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Optimized streaming endpoint that filters out internal 
    LangGraph routing and auditing JSON.
    """
    async def event_generator():
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # Using astream_events v2 to access granular node metadata
        async for event in isa_graph.astream_events(inputs, version="v2"):
            kind = event["event"]
            
            # Filter: Only stream tokens from the 'answer_agent' node
            # This ignores supervisor routing and evaluation JSON
            if kind == "on_chat_model_stream":
                node_name = event.get("metadata", {}).get("langgraph_node", "")
                
                if node_name == "answer_agent":
                    content = event["data"]["chunk"].content
                    if content:
                        yield content

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.post("/chat")
async def chat_standard(request: ChatRequest):
    """Non-streaming endpoint with clean extraction."""
    try:
        inputs = {"messages": [HumanMessage(content=request.message)]}
        result = await isa_graph.ainvoke(inputs)
        
        # Robust extraction: Get the content of the very last message
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            final_answer = last_msg.content if isinstance(last_msg, BaseMessage) else str(last_msg)
        else:
            final_answer = "The engine could not synthesize an answer."

        return {"response": final_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main_api:app", host="0.0.0.0", port=port, log_level="info")