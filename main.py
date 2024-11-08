from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.search import get_llm_response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    movie: str

class LLMResponse(BaseModel):
    response: dict

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search", response_model=LLMResponse)
async def search_endpoint(request: SearchRequest):
    response = get_llm_response(request.query, request.movie)
    
    if "error" in response:
        error_message = response["error"]
        
        if "timed out" in error_message:
            raise HTTPException(status_code=504, detail="Gateway Timeout: The request to the LLM API timed out.")
        
        elif "HTTP error occurred" in error_message:
            raise HTTPException(status_code=502, detail=error_message)
        
        elif "An error occurred while connecting" in error_message:
            raise HTTPException(status_code=503, detail="Service Unavailable: Error connecting to the LLM API.")
        
        elif "Invalid JSON response" in error_message:
            raise HTTPException(status_code=502, detail="Bad Gateway: Invalid JSON response from the LLM API.")
        
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error: An unexpected error occurred.")
    
    return {"response": response}

origins = [
    "https://thriving-malasada-05ef03.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
