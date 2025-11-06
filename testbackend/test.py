import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8501"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    input: str

class QueryResponse(BaseModel):
    output: str
    timestamp: str
    action_logged: bool

@app.post("/query", response_model=QueryResponse)
async def query_route(payload: QueryRequest):
    user_input = payload.input
    await asyncio.sleep(10)  # simulate processing delay

    # Dummy LLM/mock output text
    fake_output = (
        "Project with ID 4 started on 12/31/21, was planned to last 92 days but actually lasted 120 days. "
        "The planned budget was 674785, and the actual cost was 992464. The team size was 8, the complexity was 5, "
        "and the risk level was 2. There were 9 change requests. The cost overrun was 47.08%, and the schedule delay "
        "was 31.00%. The project was not successful."
    )
    return QueryResponse(
        output=fake_output,
        timestamp=str(datetime.now().isoformat()),
        action_logged=True
    )
