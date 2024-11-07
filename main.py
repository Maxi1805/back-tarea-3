from fastapi import FastAPI
from pydantic import BaseModel
from src.search import get_llm_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

class LLMResponse(BaseModel):
    response: dict

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search", response_model=LLMResponse)
async def search_endpoint(request: SearchRequest):
    response = get_llm_response(request.query)
    return {"response": response}
