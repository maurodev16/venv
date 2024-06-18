def parse_pricat(parsed_segments):
    parsed_data = {
        "DocumentType": parsed_segments.get("UNH", [])[0][1].split(":")[2],  # Extrai o tipo de documento
        "DocumentInfo": parsed_segments.get("BGM", [])[0][1:],  # Informações do documento
        "DateInfo": parsed_segments.get("DTM", []),  # Informações de data
        "PartyInfo": parsed_segments.get("NAD", []),  # Informações das partes envolvidas
        "LineItems": parsed_segments.get("LIN", []),  # Itens de linha
        "PriceInfo": parsed_segments.get("PRI", [])  # Informações de preço
    }
    
    # Limpar listas vazias dentro de DateInfo
    parsed_data["DateInfo"] = [item for item in parsed_data["DateInfo"] if item]
    
    return parsed_data
