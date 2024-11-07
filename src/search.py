from langchain_postgres import PGVector
from src.CustomEmbeddings import CustomEmbeddings
import requests
from requests.exceptions import RequestException, HTTPError, Timeout
import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL")
POSTGRES_CONNECTION = os.getenv("POSTGRES_CONNECTION")

def search():
    collection_name = "movies"

    vectorstore = PGVector(
        embeddings=CustomEmbeddings(),
        collection_name=collection_name,
        connection=POSTGRES_CONNECTION,
        use_jsonb=True,
    )

    results = vectorstore.similarity_search("movies_scripts/script_Logan: Como es la relacion entre Logan y su hija?", k=5)
    return results

def get_llm_response(message):
    try:
        # Retrieve and format information for the query
        info = [data.page_content for data in search()]
        info = "\n".join(info)

        # Make the POST request to the LLM API
        res = requests.post(LLM_API_URL, json={
            "model": "integra-LLM",
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": f'Mensaje:{message} Contexto: {info}'
                }
            ]
        })

        res.raise_for_status()

        return res.json()

    except Timeout:
        return {"error": "The request to the LLM API timed out. Please try again later."}

    except HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}

    except RequestException as req_err:
        return {"error": f"An error occurred while connecting to the LLM API: {req_err}"}

    except ValueError:
        return {"error": "Invalid JSON response from the LLM API."}

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == '__main__':
    print(get_llm_response("Como es la relacion entre Logan y su hija?"))
