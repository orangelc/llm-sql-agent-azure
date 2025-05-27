from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from chains.qa_chain import build_sql_chain
from db.redis_cache import get_cached_answer, set_cached_answer
from config.logging import logger
from dotenv import load_dotenv
import os


app = FastAPI(title="LLM Q&A API", version="1.0")

load_dotenv()

POSTGRES_CONFIG = {
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
    }

API_KEY = "my-secret-key"  # mejor en .env

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_llm(request: QueryRequest, x_api_key: str = Header(...)):

    chain = await build_sql_chain(POSTGRES_CONFIG)

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Pregunta vacía")

    cached = await get_cached_answer(question)
    if cached:
        logger.info("Respuesta obtenida de cache")
        return {"question": question, "answer": cached.decode()}

    try:
        logger.info(f"Pregunta recibida: {question}")
        response = await chain.ainvoke(question)
        await set_cached_answer(question, response)
        return {"question": question, "answer": response}
    except Exception as e:
        logger.error(f"Error al procesar la pregunta: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la solicitud")
