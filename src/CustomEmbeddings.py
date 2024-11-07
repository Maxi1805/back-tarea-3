from langchain_core.embeddings.embeddings import Embeddings
import requests

class CustomEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return embedding_function(texts)

    def embed_query(self, text):
        return embedding_function(text)[0]

def embedding_function(texts):
    while True:
        try:
            res = requests.post("http://tormenta.ing.puc.cl/api/embed", json={
                "model": "nomic-embed-text",
                "input": texts
            })
            return res.json()["embeddings"]
        except:
            continue