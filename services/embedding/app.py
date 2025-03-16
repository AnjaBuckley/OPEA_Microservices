from fastapi import FastAPI, HTTPException
from comps import ServiceType, TextDoc
from typing import Dict
import uvicorn
import numpy as np
import os

app = FastAPI()


def embed_text(input: TextDoc) -> Dict:
    # Placeholder implementation
    # Generate a random embedding for demonstration
    embedding = np.random.rand(384).tolist()  # Using 384 dimensions as an example
    return {"embedding": embedding, "dimensions": len(embedding)}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/embed")
async def embed_endpoint(request: Dict):
    try:
        text = request.get("text", "")
        doc = TextDoc(text=text)
        result = embed_text(doc)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6000)
