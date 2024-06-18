from typing import List, Dict
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from .parse_segments import parse_segments
from .orders_parser import parse_orders
from .pricat_parser import parse_pricat
from .invoic_parser import parse_invoic

router = APIRouter()

import logging

# Definindo o logger
logger = logging.getLogger(__name__)

def decode_and_split_segments(contents: str) -> List[str]:
    cleaned_contents = contents.strip().replace("\n", "").replace("\r", "")
    segments = cleaned_contents.split("'")
    filtered_segments = [segment for segment in segments if segment.strip()]
    
    # Log de depuração para verificar os segmentos encontrados
    logger.debug(f"Segmentos encontrados: {filtered_segments}")
    
    return filtered_segments


@router.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        decoded_contents = contents.decode()

        segments = decode_and_split_segments(decoded_contents)

        if not segments:
            return JSONResponse(status_code=400, content={"error": "No valid EDIFACT segments found"})

        parsed_segments = parse_segments(segments)

        result = []

        unb_data = parsed_segments.get("UNB", {})
        if not unb_data:
            return JSONResponse(status_code=400, content={"error": "No UNB segment found"})

        unb = {
            "UNB": {
                "SyntaxIdentifier_1": unb_data.get("SyntaxIdentifier_1", ""),
                "SyntaxVersionNumber_2": unb_data.get("SyntaxVersionNumber_2", ""),
                "InterchangeSenderIdentification_1": unb_data.get("InterchangeSenderIdentification_1", ""),
                "IdentificationCodeQualifier_2": unb_data.get("IdentificationCodeQualifier_2", ""),
                "InterchangeSenderInternalIdentification_3": unb_data.get("InterchangeSenderInternalIdentification_3", ""),
                "InterchangeRecipientIdentification_1": unb_data.get("InterchangeRecipientIdentification_1", ""),
                "RecipientIdentificationCodeQualifier_2": unb_data.get("RecipientIdentificationCodeQualifier_2", ""),
                "InterchangeRecipientInternalIdentification_3": unb_data.get("InterchangeRecipientInternalIdentification_3", ""),
                "Date_1": unb_data.get("Date_1", ""),
                "Time_2": unb_data.get("Time_2", ""),
                "InterchangeControlReference_5": unb_data.get("InterchangeControlReference_5", ""),
                "ApplicationReference_7": unb_data.get("ApplicationReference_7", ""),
                "AcknowledgementRequest_9": unb_data.get("AcknowledgementRequest_9", ""),
                "TestIndicator_11": unb_data.get("TestIndicator_11", "")
            },
            "Groups": []
        }

        unh_segments = parsed_segments.get("UNH", [])
        if not unh_segments:
            return JSONResponse(status_code=400, content={"error": "No UNH segment found"})

        for unh_segment in unh_segments:
            try:
                parsed_data = parse_orders(parsed_segments)
            except ValueError as ve:
                return JSONResponse(status_code=400, content={"error": str(ve)})

            message_type = parsed_data.get("MessageType_02", "")

            if message_type == "ORDERS":
                parsed_data = parse_orders(parsed_data)
            elif message_type == "PRICAT":
                parsed_data = parse_pricat(parsed_data)
            elif message_type == "INVOIC":
                parsed_data = parse_invoic(parsed_data)
            else:
                continue

            if parsed_data:
                unb["Groups"].append(parsed_data)

        unz_data = parsed_segments.get("UNZ", {})
        if unz_data:
            unz = {
                "UNZTrailers": [{
                    "InterchangeControlCount_1": unz_data.get("InterchangeControlCount_1", ""),
                    "InterchangeControlReference_2": unz_data.get("InterchangeControlReference_2", "")
                }]
            }
            result.append({**unb, **unz})

        final_result = {
            "Result": {
                "LastIndex": len(segments),
                "Details": [],
                "Status": "success"
            },
            "Results": result
        }

        return JSONResponse(content=final_result)

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Internal server error: {str(e)}"})

