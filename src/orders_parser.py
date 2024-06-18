
from typing import Dict, List
from .parse_orders_edi_file import *

# Função principal para parse de pedidos (ORDERS)

def parse_orders(parsed_segments: Dict[str, List[List[str]]]) -> Dict:
    parsed_data = {
       "UNB_SEGMENT": parse_unb_segment(parsed_segments.get("UNB", [[""]])[0])if "UNB" in parsed_segments else {},  # Informações do segmento UNB
       "UNH_SEGMENT": parse_unh_segment(parsed_segments.get("UNH", [[""]])[0])if "UNH" in parsed_segments else {},  # Informações do segmento UNH
       "BGM_SEGMENT": parse_bgm_segment(parsed_segments.get("BGM", [[""]])[0])if "BGM" in parsed_segments else {},  # Informações do segmento BGM
       "DTM_SEGMENT": parse_dtm_segment(parsed_segments.get("DTM", [[""]])[0])if "DTM" in parsed_segments else {},  # Informações de segmentos DTM
       "NAD_SEGMENT": parse_nad_segment(parsed_segments.get("NAD", [[""]])[0])if "NAD" in parsed_segments else {},  # Informações de segmentos NAD
       "PAI_SEGMENT": parse_pai_segment(parsed_segments.get("PAI", [[""]])[0])if "PAI" in parsed_segments else {},  # Informações de segmentos PAI
       "FTX_SEGMENT": parse_ftx_segment(parsed_segments.get("FTX", [[""]])[0])if "FTX" in parsed_segments else {},  # Informações de segmentos FTX
       "RFF_SEGMENT": parse_rff_segment(parsed_segments.get("RFF", [[""]])[0])if "RFF" in parsed_segments else {},  # Informações de segmentos RFF
       "CTA_SEGMENT": parse_cta_segment(parsed_segments.get("CTA", [[""]])[0])if "CTA" in parsed_segments else {},  # Informações de segmentos CTA
       "COM_SEGMENT": parse_com_segment(parsed_segments.get("COM", [[""]])[0])if "COM" in parsed_segments else {},  # Informações de segmentos COM
       "CUX_SEGMENT": parse_cux_segment(parsed_segments.get("CUX", [[""]])[0])if "CUX" in parsed_segments else {},  # Informações de segmentos CUX
       "TDT_SEGMENT": parse_tdt_segment(parsed_segments.get("TDT", [[""]])[0])if "TDT" in parsed_segments else {},  # Informações de segmentos TDT
       "TOD_SEGMENT": parse_tod_segment(parsed_segments.get("TOD", [[""]])[0])if "TOD" in parsed_segments else {},  # Informações de segmentos TOD
       "LOC_SEGMENT": parse_loc_segment(parsed_segments.get("LOC", [[""]])[0])if "LOC" in parsed_segments else {},  # Informações de segmentos LOC
       "LIN_SEGMENT": parse_lin_segment(parsed_segments.get("LIN", [[""]])[0])if "LIN" in parsed_segments else {},
       "PIA_SEGMENT": parse_pia_segment(parsed_segments.get("PIA", [[""]])[0])if "PIA" in parsed_segments else {},  # Informações de segmentos PIA
       "IMD_SEGMENT": parse_imd_segment(parsed_segments.get("IMD", [[""]])[0])if "IMD" in parsed_segments else {},  # Informações de segmentos IMD
       "QTY_SEGMENT": parse_qty_segment(parsed_segments.get("QTY", [[""]])[0])if "QTY" in parsed_segments else {},  # Informações de segmentos QTY
       "MOA_SEGMENT": parse_moa_segment(parsed_segments.get("MOA", [[""]])[0])if "MOA" in parsed_segments else {},
       "PRI_SEGMENT": parse_pri_segment(parsed_segments.get("PRI", [[""]])[0])if "PRI" in parsed_segments else {},
       "PAC_SEGMENT": parse_pac_segment(parsed_segments.get("PAC", [[""]])[0])if "PAC" in parsed_segments else {},  # Informações de segmentos PAC
       "PCI_SEGMENT": parse_pci_segment(parsed_segments.get("PCI", [[""]])[0])if "PCI" in parsed_segments else {},  # Informações de segmentos PCI
       "TAX_SEGMENT": parse_tax_segment(parsed_segments.get("TAX", [[""]])[0])if "TAX" in parsed_segments else {},  # Informações de segmentos TAX
       "UNS_SEGMENT": parse_uns_segment(parsed_segments.get("UNS", [[""]])[0])if "UNS" in parsed_segments else {},  # Informações de segmentos UNS
       "CNT_SEGMENT": parse_cnt_segment(parsed_segments.get("CNT", [[""]])[0])if "CNT" in parsed_segments else {},  # Informações de segmentos CNT
       "UNT_SEGMENT": parse_unt_segment(parsed_segments.get("UNT", [[""]])[0])if "UNT" in parsed_segments else {},  # Informações de segmento UNT
       "UNZ_SEGMENT": parse_unz_segment(parsed_segments.get("UNZ", [[""]])[0])if "UNZ" in parsed_segments else {},  # Informações de segmento UNZ
      
    }
    print(parsed_data)
    

    return parsed_data

