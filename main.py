from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from src.orders_parser import parse_orders

# Define um modelo Pydantic para a resposta JSON
class ParsedData(BaseModel):
    parsed_data: dict

app = FastAPI(
    title="Mauro EDI",
    description="API para processamento de arquivos EDIFACT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.post("/upload_orders_edi/")
async def upload_orders_edi(files: List[UploadFile] = File(...)):
    parsed_data = {}

    for file in files:
        contents = await file.read()
        segments_list = contents.decode('utf-8').split('\n')
        
        parsed_segments = {}
        for segment in segments_list:
            segment_type = segment.split('+')[0]
            if segment_type not in parsed_segments:
                parsed_segments[segment_type] = []
            parsed_segments[segment_type].append(segment.split('+'))

        parsed_data[file.filename] = parse_orders(parsed_segments)

    return parsed_data



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
