from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from src.search import get_llm_response

app = FastAPI()

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
