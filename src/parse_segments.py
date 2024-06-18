import logging

# Definindo o logger
logger = logging.getLogger(__name__)

# Função para parse dos segmentos EDIFACT
from typing import List, Dict

def parse_segments(segments_list: List[str]) -> Dict:
    parsed_data = {}
    current_transaction = None
    current_group = None

    for segment in segments_list:
        sub_segments = segment.split("+")
        segment_name = sub_segments[0]

        try:
            if segment_name == "UNB":
                parsed_data["UNB"] = parse_unb_segment(sub_segments)
            elif segment_name == "UNH":
                if "Groups" not in parsed_data:
                    parsed_data["Groups"] = []
                if parsed_data["Groups"] and "Transactions" not in parsed_data["Groups"][-1]:
                    parsed_data["Groups"][-1]["Transactions"] = []
                current_transaction = {"UNH": parse_unh_segment(sub_segments)}
                parsed_data["Groups"][-1]["Transactions"].append(current_transaction)
            elif segment_name == "BGM":
                if current_transaction:
                    current_transaction["BGM"] = parse_bgm_segment(sub_segments)
            elif segment_name == "DTM":
                if current_transaction:
                    if "DTM" not in current_transaction:
                        current_transaction["DTM"] = []
                    current_transaction["DTM"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "PAI":
                if current_transaction:
                    if "PAI" not in current_transaction:
                        current_transaction["PAI"] = []
                    current_transaction["PAI"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "FTX":
                if current_transaction:
                    if "FTX" not in current_transaction:
                        current_transaction["FTX"] = []
                    current_transaction["FTX"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "RFF":
                if current_transaction:
                    if "RFF" not in current_transaction:
                        current_transaction["RFF"] = []
                    current_transaction["RFF"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "NAD":
                if current_transaction:
                    if "NAD" not in current_transaction:
                        current_transaction["NAD"] = []
                    current_transaction["NAD"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "CTA":
                if current_transaction:
                    if "CTA" not in current_transaction:
                        current_transaction["CTA"] = []
                    current_transaction["CTA"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "COM":
                if current_transaction:
                    if "COM" not in current_transaction:
                        current_transaction["COM"] = []
                    current_transaction["COM"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "CUX":
                if current_transaction:
                    if "CUX" not in current_transaction:
                        current_transaction["CUX"] = []
                    current_transaction["CUX"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "TDT":
                if current_transaction:
                    if "TDT" not in current_transaction:
                        current_transaction["TDT"] = []
                    current_transaction["TDT"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "TOD":
                if current_transaction:
                    if "TOD" not in current_transaction:
                        current_transaction["TOD"] = []
                    current_transaction["TOD"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "LOC":
                if current_transaction:
                    if "LOC" not in current_transaction:
                        current_transaction["LOC"] = []
                    current_transaction["LOC"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "LIN":
                if current_transaction:
                    if "LIN" not in current_transaction:
                        current_transaction["LIN"] = []
                    current_transaction["LIN"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "PIA":
                if current_transaction:
                    if "PIA" not in current_transaction:
                        current_transaction["PIA"] = []
                    current_transaction["PIA"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "IMD":
                if current_transaction:
                    if "IMD" not in current_transaction:
                        current_transaction["IMD"] = []
                    current_transaction["IMD"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "QTY":
                if current_transaction:
                    if "QTY" not in current_transaction:
                        current_transaction["QTY"] = []
                    current_transaction["QTY"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "MOA":
                if current_transaction:
                    if "MOA" not in current_transaction:
                        current_transaction["MOA"] = []
                    current_transaction["MOA"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "PRI":
                if current_transaction:
                    if "PRI" not in current_transaction:
                        current_transaction["PRI"] = []
                    current_transaction["PRI"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "PAC":
                if current_transaction:
                    if "PAC" not in current_transaction:
                        current_transaction["PAC"] = []
                    current_transaction["PAC"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "PCI":
                if current_transaction:
                    if "PCI" not in current_transaction:
                        current_transaction["PCI"] = []
                    current_transaction["PCI"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "TAX":
                if current_transaction:
                    if "TAX" not in current_transaction:
                        current_transaction["TAX"] = []
                    current_transaction["TAX"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "UNS":
                if current_transaction:
                    if "UNS" not in current_transaction:
                        current_transaction["UNS"] = []
                    current_transaction["UNS"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "CNT":
                if current_transaction:
                    if "CNT" not in current_transaction:
                        current_transaction["CNT"] = []
                    current_transaction["CNT"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "UNT":
                if current_transaction:
                    if "UNT" not in current_transaction:
                        current_transaction["UNT"] = []
                    current_transaction["UNT"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            elif segment_name == "UNZ":
                if current_transaction:
                    if "UNZ" not in current_transaction:
                        current_transaction["UNZ"] = []
                    current_transaction["UNZ"].append({"SegmentName": segment_name, "Elements": sub_segments[1:]})
            else:
                logger.warning(f"Ignorando segmento {segment_name} desconhecido ou fora de contexto.")

        except ValueError as ve:
            logger.error(f"Erro ao processar segmento {segment_name}: {ve}")

    return parsed_data


# Função genérica para parse de segmentos não específicos
def handle_generic_segment(current_transaction, segment_name, sub_segments):
    if current_transaction is None:
        logger.warning(f"Ignorando segmento {segment_name} fora de uma transação.")
    else:
        if segment_name not in current_transaction:
            current_transaction[segment_name] = []
        current_transaction[segment_name].append(parse_generic_segment(sub_segments))

# Função genérica para parse de segmentos não específicos
def parse_generic_segment(parts):
    return {
        "SegmentName": parts[0],
        "Elements": parts[1:]
    }

# Funções específicas de parse para cada segmento
def parse_unb_segment(parts):
    required_length = 12  # Número mínimo de elementos obrigatórios no segmento UNB

    if len(parts) < required_length:
        raise ValueError("Segmento UNB incompleto")

    unb_dict = {
        "SyntaxIdentifier_1": parts[1] if len(parts) > 1 else "",
        "SyntaxVersionNumber_2": parts[2] if len(parts) > 2 else "",
    }

    for index in range(3, len(parts)):
        key = f"Element_{index-1:02d}"  # Constrói chaves dinâmicas para os elementos restantes
        unb_dict[key] = parts[index]

    return unb_dict

def parse_unh_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento UNH

    if len(parts) < required_length:
        raise ValueError("Segmento UNH incompleto")

    # Ajustar para lidar com os elementos dinamicamente, se houver mais que 3 elementos
    unh_dict = {
        "MessageReferenceNumber_01": parts[1] if len(parts) > 1 else "",
        "MessageType_02": parts[2].split(":")[0] if len(parts) > 2 else "",
        "MessageVersionNumber_03": parts[3] if len(parts) > 3 else ""
    }

    # Adicionar informações adicionais se existirem
    for index in range(4, len(parts)):
        key = f"AdditionalInformation_{index - 3:02d}"  # Nomeia as chaves dinamicamente
        unh_dict[key] = parts[index]

    return unh_dict

def parse_bgm_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento BGM

    if len(parts) < required_length:
        raise ValueError("Segmento BGM incompleto")

    bgm_dict = {
        "DocumentName_01": parts[1] if len(parts) > 1 else "",
        "DocumentNumber_02": parts[2] if len(parts) > 2 else ""
    }

    return bgm_dict

# Exemplo de uso:
edi_data = [
    "UNB+UNOB:1+SENDER1:14:ZZUK+RECEIVER1:1:ZZUK+071101:1701+131++ORDERS++1++1'",
    "UNH+000000101+ORDERS:D:96A:UN'",
    "BGM+220+128576+9'",
    "DTM+137:20020830:102",
    "PAI+::42",
    "FTX+ZZZ+1+001::91",
    "RFF+CT:652744",
    "NAD+BY+5412345000013::9",
    "RFF+VA:87765432",
    "CTA+OC+:P FORGET",
    "COM+0044715632478:TE",
    "NAD+SU+4012345500004::9",
    "RFF+VA:56225432",
    "CUX+2:GBP:9+3:EUR:4+1.67",
    "TDT+20++30+31",
    "TOD+3++CIF:23:9",
    "LOC+1+BE-BRU",
    "LIN+1++4000862141404:SRS",
    "PIA+1+ABC1234:IN",
    "IMD+C++TU::9",
    "QTY+21:48",
    "MOA+203:699.84",
    "PRI+AAA:14.58:CT:AAE:1:KGM",
    "PAC+2+:51+CS",
    "PCI+14",
    "LOC+7+3312345502000::9",
    "QTY+11:24",
    "LOC+7+3312345501003::9",
    "QTY+11:24",
    "TAX+7+VAT+++:::17.5+S",
    "UNS+S",
    "CNT+2:1",
    "UNT+38+000000101",
    "UNZ+1+131"
]

parsed_data = parse_segments(edi_data)
print(parsed_data)
