def parse_invoic(segments):
    parsed_data = {}
    for segment in segments:
        elements = segment.split('+')
        segment_name = elements[0]
        
        if segment_name == "UNH":
            document_type = elements[2]
            parsed_data["DocumentType"] = document_type
        elif segment_name == "BGM":
            document_info = elements[1:]
            parsed_data["DocumentInfo"] = document_info
        elif segment_name == "LIN":
            item_details = elements[1:]
            parsed_data.setdefault("ItemDetails", []).append(item_details)
        # Adicionar outros segmentos específicos do INVOIC conforme necessário
    return parsed_data
