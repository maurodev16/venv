from typing import Dict, List
from .parse_orders_edi_file import *
# Função principal para parse de pedidos (ORDERS)
def parse_orders(parsed_segments: Dict[str, List[List[str]]]) -> Dict:
    transactions = []

    # Mapeamento de segmentos para funções de parsing
    segment_parsers = {
        "UNB": parse_unb_segment,
        "UNH": parse_unh_segment,
        "BGM": parse_bgm_segment,
        "DTM": parse_dtm_segment,
        "PAI": parse_pai_segment,
        "FTX": parse_ftx_segment,
        "RFF": parse_rff_segment,
        "NAD": parse_nad_segment,
        "CTA": parse_cta_segment,
        "COM": parse_com_segment,
        "CUX": parse_cux_segment,
        "TDT": parse_tdt_segment,
        "TOD": parse_tod_segment,
        "LOC": parse_loc_segment,
        "LIN": parse_lin_segment,
        "PIA": parse_pia_segment,
        "IMD": parse_imd_segment,
        "QTY": parse_qty_segment,
        "MOA": parse_moa_segment,
        "PRI": parse_pri_segment,
        "PAC": parse_pac_segment,
        "PCI": parse_pci_segment,
        "TAX": parse_tax_segment,
        "UNS": parse_uns_segment,
        "CNT": parse_cnt_segment,
        "UNT": parse_unt_segment,
        "UNZ": parse_unz_segment,
    }

    parsed_data = {}

    # Adicionar segmento UNB como cabeçalho se presente
    if "UNB" in parsed_segments:
        parsed_data["UNB_SEGMENT"] = segment_parsers["UNB"](parsed_segments["UNB"][0])

    # Processar todos os segmentos e adicionar às transações
    for segment_name, segment_data in parsed_segments.items():
        if segment_name in segment_parsers:
            segment_dict = {f"{segment_name}_SEGMENT": segment_parsers[segment_name](segment_data[0])}

            # Verificar se o segmento requer um loop
            if segment_name == "RFF" or segment_name == "NAD" or segment_name == "LIN" or segment_name == "PAC" or segment_name == "LOC":
                loop_name = segment_name + "Loop"
                loop_items = []

                # Processar cada item do loop correspondente
                for data in segment_data:
                    inner_segment_dict = {f"{segment_name}_SEGMENT": segment_parsers[segment_name](data)}

                    # Verificar se há loops internos para este segmento
                    if loop_name in inner_segment_dict[f"{segment_name}_SEGMENT"]:
                        inner_loop_name = loop_name[:-4]  # Remover "Loop" do nome do loop interno
                        inner_segments = inner_segment_dict[f"{segment_name}_SEGMENT"].pop(loop_name)

                        # Processar cada segmento dentro do loop interno
                        inner_transactions = []
                        for inner_segment_data in inner_segments:
                            inner_segment_dict = {f"{inner_loop_name}_SEGMENT": {}}
                            for inner_segment_name, inner_segment_data in inner_segment_data.items():
                                inner_segment_dict[f"{inner_loop_name}_SEGMENT"][inner_segment_name] = segment_parsers[inner_segment_name](inner_segment_data)
                            inner_transactions.append(inner_segment_dict)

                        segment_dict[f"{segment_name}_SEGMENT"][inner_loop_name] = inner_transactions

                    loop_items.append(inner_segment_dict)

                transactions.append({loop_name: loop_items})
            else:
                transactions.append(segment_dict)

    parsed_data["Groups"] = [{"Transactions": transactions}]

    # Adicionar segmento UNZ como rodapé se presente
    if "UNZ" in parsed_segments:
        parsed_data["UNZ_SEGMENT"] = segment_parsers["UNZ"](parsed_segments["UNZ"][0])

    # Adicionar contagem de segmentos
    parsed_data["SegmentCount"] = sum(len(segment_data) for segment_data in parsed_segments.values())

    return {"ORDERS.txt": parsed_data}
