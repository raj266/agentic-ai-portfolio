from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
from langgraph_agent import build_graph

class AgentRequest(BaseModel):
    query: str
    mode: str = "parallel"

class AgentResponse(BaseModel):
    final_answer: str
    elapsed_time: float
    mode_used: str

app = FastAPI(title="Agentic AI – Priority Multi‑Agent", version="1.0")

# Allow CORS for all origins (for demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agent", response_model=AgentResponse)
async def agent_endpoint(request: AgentRequest):
    start_time = time.time()
    try:
        graph = build_graph(mode=request.mode)
        initial_state = {
            "query": request.query,
            "legal_opinion": "",
            "budget_opinion": "",
            "location_opinion": "",
            "final_answer": ""
        }
        final_state = graph.invoke(initial_state)
        elapsed = time.time() - start_time
        return AgentResponse(
            final_answer=final_state["final_answer"],
            elapsed_time=elapsed,
            mode_used=request.mode
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
