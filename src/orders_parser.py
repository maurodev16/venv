
from typing import Dict, List
from .parse_segments import parse_unb_segment, parse_unh_segment, parse_bgm_segment

# Função principal para parse de pedidos (ORDERS)
def parse_orders(parsed_segments: Dict[str, List[List[str]]]) -> Dict:
    parsed_data = {
        "UNBInfo": parse_unb_segment(parsed_segments.get("UNB", [])[0]),  # Informações do segmento UNB
        "UNHInfo": parse_unh_segment(parsed_segments.get("UNH", [])[0]),  # Informações do segmento UNH
        "BGMInfo": parse_bgm_segment(parsed_segments.get("BGM", [])[0]),  # Informações do segmento BGM
        # "DTMInfo": parse_dtm_segment(parsed_segments.get("DTM", [])),  # Informações de segmentos DTM
        # "NADInfo": parse_nad_segment(parsed_segments.get("NAD", [])),  # Informações de segmentos NAD
        # "LINInfo": parse_lin_segment(parsed_segments.get("LIN", [])),  # Informações de segmentos LIN
        # "PRIInfo": parse_pri_segment(parsed_segments.get("PRI", [])),  # Informações de segmentos PRI
        # "QTYInfo": parse_qty_segment(parsed_segments.get("QTY", [])),  # Informações de segmentos QTY
        # "MOAInfo": parse_moa_segment(parsed_segments.get("MOA", [])),  # Informações de segmentos MOA
        # "RFFInfo": parse_rff_segment(parsed_segments.get("RFF", [])),  # Informações de segmentos RFF
        # "DTMDateInfo": parse_dtm_segment(parsed_segments.get("DTM", [])),  # Informações de segmentos DTM para datas
        # "PAIInfo": parse_pai_segment(parsed_segments.get("PAI", [])),  # Informações de segmentos PAI
        # "FTXInfo": parse_ftx_segment(parsed_segments.get("FTX", [])),  # Informações de segmentos FTX
        # "CTAInfo": parse_cta_segment(parsed_segments.get("CTA", [])),  # Informações de segmentos CTA
        # "COMInfo": parse_com_segment(parsed_segments.get("COM", [])),  # Informações de segmentos COM
        # "CUXInfo": parse_cux_segment(parsed_segments.get("CUX", [])),  # Informações de segmentos CUX
        # "TDTInfo": parse_tdt_segment(parsed_segments.get("TDT", [])),  # Informações de segmentos TDT
        # "TODInfo": parse_tod_segment(parsed_segments.get("TOD", [])),  # Informações de segmentos TOD
        # "LOCInfo": parse_loc_segment(parsed_segments.get("LOC", [])),  # Informações de segmentos LOC
        # "IMDInfo": parse_imd_segment(parsed_segments.get("IMD", [])),  # Informações de segmentos IMD
        # "PACInfo": parse_pac_segment(parsed_segments.get("PAC", [])),  # Informações de segmentos PAC
        # "PCIInfo": parse_pci_segment(parsed_segments.get("PCI", [])),  # Informações de segmentos PCI
        # "TAXInfo": parse_tax_segment(parsed_segments.get("TAX", [])),  # Informações de segmentos TAX
        # "UNSInfo": parse_uns_segment(parsed_segments.get("UNS", [])),  # Informações de segmentos UNS
        # "CNTInfo": parse_cnt_segment(parsed_segments.get("CNT", [])),  # Informações de segmentos CNT
        # "UNTInfo": parse_unt_segment(parsed_segments.get("UNT", [])[0]),  # Informações de segmento UNT
        # "UNZInfo": parse_unz_segment(parsed_segments.get("UNZ", [])[0]),  # Informações de segmento UNZ
        # "PIAInfo": parse_pia_segment(parsed_segments.get("PIA", [])),  # Informações de segmentos PIA
    }

    return parsed_data
