import os
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from src.orders_parser import parse_orders
from src.xml_converter import convert_edi_to_xml

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

@app.post("/convert_edi_to_json/")
async def convert_edi_to_json(files: List[UploadFile] = File(...)):
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

        try:
            edi_data = parse_orders(parsed_segments)  # Parse EDI para JSON
            
            parsed_data[file.filename] = {
                "edi_data": edi_data
            }
        
        except Exception as e:
            return {"error": str(e)}

    return parsed_data

@app.post("/convert_edi_to_xml/")
async def convert_edi_to_xml_endpoint(files: List[UploadFile] = File(...)):
    parsed_data = {}

    for file in files:
        contents = await file.read()
        
        try:
            edi_data = parse_orders(contents.decode('utf-8'))  # Parse EDI para dict
            xml_filepath = convert_edi_to_xml(edi_data, file.filename)   # Converta EDI para XML e obtenha o caminho do arquivo

            parsed_data[file.filename] = {
                "xml_filepath": xml_filepath
            }
        
        except Exception as e:
            return {"error": str(e)}

    return parsed_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload=True)
