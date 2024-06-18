from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src  import file_handler_router

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(  title="Minha API EDIFACT",
    description="API para processamento de arquivos EDIFACT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc")
app.include_router(file_handler_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)