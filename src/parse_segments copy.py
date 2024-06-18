import logging

# Definindo o logger
logger = logging.getLogger(__name__)

# Função para parse dos segmentos EDIFACT
def parse_segments(segments_list):
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
                current_transaction = {"UNH": parse_unh_segment(sub_segments)}
                parsed_data["Groups"].append({"Transactions": [current_transaction]})
            elif segment_name == "BGM":
                if current_transaction:
                    current_transaction["BGM"] = parse_bgm_segment(sub_segments)
            elif segment_name == "DTM":
                if current_transaction:
                    if "DTM" not in current_transaction:
                        current_transaction["DTM"] = []
                    current_transaction["DTM"].append(parse_dtm_segment(sub_segments))
            elif segment_name == "PAI":
                if current_transaction:
                    current_transaction["PAI"] = parse_pai_segment(sub_segments)
            elif segment_name == "FTX":
                if current_transaction:
                    if "FTX" not in current_transaction:
                        current_transaction["FTX"] = []
                    current_transaction["FTX"].append(parse_ftx_segment(sub_segments))
            elif segment_name == "RFF":
                if current_transaction:
                    if "RFF" not in current_transaction:
                        current_transaction["RFF"] = []
                    current_transaction["RFF"].append(parse_rff_segment(sub_segments))
            elif segment_name == "NAD":
                if current_transaction:
                    if "NAD" not in current_transaction:
                        current_transaction["NAD"] = []
                    current_transaction["NAD"].append(parse_nad_segment(sub_segments))
            elif segment_name == "CUX":
                if current_transaction:
                    current_transaction["CUX"] = parse_cux_segment(sub_segments)
            elif segment_name == "TDT":
                if current_transaction:
                    current_transaction["TDT"] = parse_tdt_segment(sub_segments)
            elif segment_name == "TOD":
                if current_transaction:
                    current_transaction["TOD"] = parse_tod_segment(sub_segments)
            elif segment_name == "LOC":
                if current_transaction:
                    if "LOC" not in current_transaction:
                        current_transaction["LOC"] = []
                    current_transaction["LOC"].append(parse_loc_segment(sub_segments))
            elif segment_name == "LIN":
                if current_transaction:
                    if "LIN" not in current_transaction:
                        current_transaction["LIN"] = []
                    current_transaction["LIN"].append(parse_lin_segment(sub_segments))
            elif segment_name == "PIA":
                if current_transaction:
                    if "PIA" not in current_transaction:
                        current_transaction["PIA"] = []
                    current_transaction["PIA"].append(parse_pia_segment(sub_segments))
            elif segment_name == "IMD":
                if current_transaction:
                    if "IMD" not in current_transaction:
                        current_transaction["IMD"] = []
                    current_transaction["IMD"].append(parse_imd_segment(sub_segments))
            elif segment_name == "QTY":
                if current_transaction:
                    if "QTY" not in current_transaction:
                        current_transaction["QTY"] = []
                    current_transaction["QTY"].append(parse_qty_segment(sub_segments))
            elif segment_name == "MOA":
                if current_transaction:
                    if "MOA" not in current_transaction:
                        current_transaction["MOA"] = []
                    current_transaction["MOA"].append(parse_moa_segment(sub_segments))
            elif segment_name == "PRI":
                if current_transaction:
                    if "PRI" not in current_transaction:
                        current_transaction["PRI"] = []
                    current_transaction["PRI"].append(parse_pri_segment(sub_segments))
            elif segment_name == "RFF":
                if current_transaction:
                    if "RFF" not in current_transaction:
                        current_transaction["RFF"] = []
                    current_transaction["RFF"].append(parse_rff_segment(sub_segments))
            elif segment_name == "PAC":
                if current_transaction:
                    current_transaction["PAC"] = parse_pac_segment(sub_segments)
            elif segment_name == "PCI":
                if current_transaction:
                    current_transaction["PCI"] = parse_pci_segment(sub_segments)
            elif segment_name == "UNS":
                if current_transaction:
                    current_transaction["UNS"] = parse_uns_segment(sub_segments)
            elif segment_name == "CNT":
                if current_transaction:
                    if "CNT" not in current_transaction:
                        current_transaction["CNT"] = []
                    current_transaction["CNT"].append(parse_cnt_segment(sub_segments))
            elif segment_name == "UNT":
                if current_transaction:
                    if current_group:
                        current_group["Transactions"].append(current_transaction)
                    current_transaction = None
            elif segment_name == "UNZ":
                current_group = None
            elif segment_name == "LOC":
                if "Groups" not in parsed_data:
                    parsed_data["Groups"] = []
                current_group = {"LOC": parse_loc_segment(sub_segments), "Transactions": []}
                parsed_data["Groups"].append(current_group)
            else:
                logger.warning(f"Ignorando segmento {segment_name} desconhecido ou fora de contexto.")

        except ValueError as ve:
            logger.error(f"Erro ao processar segmento {segment_name}: {ve}")

    return parsed_data

# Função para parse do segmento UNB
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

# Função para parse do segmento UNH
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


# Função para parse do segmento BGM

# Função para parse do segmento BGM (exemplo)
def parse_bgm_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento BGM

    if len(parts) < required_length:
        raise ValueError("Segmento BGM incompleto")

    bgm_dict = {
        "DocumentMessageName_01": parts[1] if len(parts) > 1 else "",
        "DocumentMessageNumber_02": parts[2] if len(parts) > 2 else ""
        # Adicionar mais campos conforme necessário
    }

    return bgm_dict


# Função para parse do segmento UNT
def parse_unt_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento UNT

    if len(parts) < required_length:
        raise ValueError("Segmento UNT incompleto")

    return {
        "NumberOfSegmentsInMessage_01": parts[1] if len(parts) > 1 else "",
        "MessageReferenceNumber_02": parts[2] if len(parts) > 2 else "",
        "MessageTrailerControlReference_03": parts[3] if len(parts) > 3 else ""
    }
# Função para parse do segmento UNZ
def parse_unz_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento UNZ

    if len(parts) < required_length:
        raise ValueError("Segmento UNZ incompleto")

    return {
        "InterchangeControlCount_01": parts[1] if len(parts) > 1 else "",
        "InterchangeControlReference_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento DTM
def parse_dtm_segment(parts):
    qualifier = parts[1] if len(parts) > 1 else ""
    date = parts[2] if len(parts) > 2 else ""
    time = parts[3] if len(parts) > 3 else ""

    return {
        "DateTimePeriodQualifier_01": qualifier,
        "DateTimePeriod_02": date,
        "DateTimePeriodFormatQualifier_03": time
    }

# Função para parse do segmento PAI
def parse_pai_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento PAI

    if len(parts) < required_length:
        raise ValueError("Segmento PAI incompleto")

    return {
        "PaymentTermsTypeCode_01": parts[1] if len(parts) > 1 else "",
        "PaymentTermsBasisCode_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento FTX
def parse_ftx_segment(parts):
    required_length = 5  # Número mínimo de elementos obrigatórios no segmento FTX

    if len(parts) < required_length:
        raise ValueError("Segmento FTX incompleto")

    return {
        "TextSubjectCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "TextLiteral_02": parts[2] if len(parts) > 2 else "",
        "TextLiteral_03": parts[3] if len(parts) > 3 else "",
        "TextLiteral_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento RFF
def parse_rff_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento RFF

    if len(parts) < required_length:
        raise ValueError("Segmento RFF incompleto")

    return {
        "ReferenceCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "ReferenceIdentifier_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento NAD
def parse_nad_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento NAD

    if len(parts) < required_length:
        raise ValueError("Segmento NAD incompleto")

    return {
        "PartyFunctionCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "PartyIdentifier_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento CTA
def parse_cta_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento CTA

    if len(parts) < required_length:
        raise ValueError("Segmento CTA incompleto")

    return {
        "ContactFunctionCode_01": parts[1] if len(parts) > 1 else "",
        "ContactName_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento COM
def parse_com_segment(parts):
    com_dict = {}

    # Iterar sobre os elementos do segmento COM
    for index, part in enumerate(parts[1:], start=1):
        com_dict[f"CommunicationElement_{index:02d}"] = part

    return com_dict


# Função para parse do segmento CUX
# Função para parse do segmento CUX
def parse_cux_segment(parts):
    cux_dict = {}

    # Iterar sobre os elementos do segmento CUX
    for index, part in enumerate(parts[1:], start=1):
        cux_dict[f"CurrencyDetails_{index:02d}"] = part

    return cux_dict

# Função para parse do segmento TDT
def parse_tdt_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento TDT

    if len(parts) < required_length:
        raise ValueError("Segmento TDT incompleto")

    return {
        "TransportStageCode_01": parts[1] if len(parts) > 1 else "",
        "ModeOfTransportCode_02": parts[2] if len(parts) > 2 else "",
        "TransportMeans_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento TOD
def parse_tod_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento TOD

    if len(parts) < required_length:
        raise ValueError("Segmento TOD incompleto")

    return {
        "DeliveryOrTransportTermsFunctionCode_01": parts[1] if len(parts) > 1 else "",
        "TermsOfDeliveryOrTransport_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento LOC
def parse_loc_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento LOC

    if len(parts) < required_length:
        raise ValueError("Segmento LOC incompleto")

    return {
        "LocationQualifier_01": parts[1] if len(parts) > 1 else "",
        "LocationIdentifier_02": parts[2] if len(parts) > 2 else "",
        "LocationName_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento LIN
def parse_lin_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento LIN

    if len(parts) < required_length:
        raise ValueError("Segmento LIN incompleto")

    return {
        "LineItemIdentifier_01": parts[1] if len(parts) > 1 else "",
        "ActionRequestNotificationCode_02": parts[2] if len(parts) > 2 else "",
        "ProductIdentifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento PIA
def parse_pia_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento PIA

    if len(parts) < required_length:
        raise ValueError("Segmento PIA incompleto")

    return {
        "ProductIdentifierCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "ProductIdentifier_02": parts[2] if len(parts) > 2 else "",
        "ProductIdentifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento IMD
def parse_imd_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento IMD

    if len(parts) < required_length:
        raise ValueError("Segmento IMD incompleto")

    return {
        "ItemDescriptionTypeCode_01": parts[1] if len(parts) > 1 else "",
        "ItemCharacteristicCode_02": parts[2] if len(parts) > 2 else "",
        "ItemDescription_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento QTY
def parse_qty_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento QTY

    if len(parts) < required_length:
        raise ValueError("Segmento QTY incompleto")

    return {
        "QuantityQualifier_01": parts[1] if len(parts) > 1 else "",
        "Quantity_02": parts[2] if len(parts) > 2 else "",
        "MeasureUnitCode_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento MOA
def parse_moa_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento MOA

    if len(parts) < required_length:
        raise ValueError("Segmento MOA incompleto")

    return {
        "MonetaryAmountTypeCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "MonetaryAmount_02": parts[2] if len(parts) > 2 else "",
        "CurrencyIdentificationCode_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento PRI
# Função para parse do segmento PRI
def parse_pri_segment(parts):
    pri_dict = {}

    # Iterar sobre os elementos do segmento PRI
    for index, part in enumerate(parts[1:], start=1):
        if index == 1:
            pri_dict["PriceCodeQualifier_01"] = part
        elif index == 2:
            pri_dict["PriceAmount_02"] = part
        elif index == 3:
            pri_dict["CurrencyIdentificationCode_03"] = part
        else:
            pri_dict[f"AdditionalInfo_{index:02d}"] = part

    return pri_dict

# Função para parse do segmento TAX
def parse_tax_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento TAX

    if len(parts) < required_length:
        raise ValueError("Segmento TAX incompleto")

    return {
        "DutyOrTaxOrFeeTypeCode_01": parts[1] if len(parts) > 1 else "",
        "DutyOrTaxOrFeeRate_02": parts[2] if len(parts) > 2 else "",
        "DutyOrTaxOrFeeRateBasisCode_03": parts[3] if len(parts) > 3 else "",
        "DutyOrTaxOrFeeCategoryCode_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento TDT
def parse_tdt_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento TDT

    if len(parts) < required_length:
        raise ValueError("Segmento TDT incompleto")

    return {
        "TransportStageCode_01": parts[1] if len(parts) > 1 else "",
        "ModeOfTransportCode_02": parts[2] if len(parts) > 2 else "",
        "TransportMeans_03": parts[3] if len(parts) > 3 else "",
        "CarrierName_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento ALC
def parse_alc_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento ALC

    if len(parts) < required_length:
        raise ValueError("Segmento ALC incompleto")

    return {
        "AllowanceOrChargeCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "AllowanceOrChargeIdentifier_02": parts[2] if len(parts) > 2 else "",
        "AllowanceOrChargeQualifier_03": parts[3] if len(parts) > 3 else "",
        "AllowanceOrChargeAmount_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento SCC
def parse_scc_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento SCC

    if len(parts) < required_length:
        raise ValueError("Segmento SCC incompleto")

    return {
        "DeliveryPlanScheduleTypeCode_01": parts[1] if len(parts) > 1 else "",
        "DeliveryPlanFrequencyCode_02": parts[2] if len(parts) > 2 else "",
        "DeliveryPatternTimeCode_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento PCI
def parse_pci_segment(parts):
    pci_dict = {}

    # Iterar sobre os elementos do segmento PCI
    for index, part in enumerate(parts[1:], start=1):
        if index == 1:
            pci_dict["MarkingInstructionsCode_01"] = part
        elif index == 2:
            pci_dict[f"PackageMarking_{index:02d}"] = part
        else:
            pci_dict[f"AdditionalInfo_{index:02d}"] = part

    return pci_dict

# Função para parse do segmento SEQ
def parse_seq_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento SEQ

    if len(parts) < required_length:
        raise ValueError("Segmento SEQ incompleto")

    return {
        "SequenceInformation_01": parts[1] if len(parts) > 1 else "",
        "SequenceNumber_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento DOC
def parse_doc_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento DOC

    if len(parts) < required_length:
        raise ValueError("Segmento DOC incompleto")

    return {
        "DocumentNameCode_01": parts[1] if len(parts) > 1 else "",
        "DocumentIdentifier_02": parts[2] if len(parts) > 2 else "",
        "DocumentStatusCode_03": parts[3] if len(parts) > 3 else "",
        "DocumentSource_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento PCD
def parse_pcd_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento PCD

    if len(parts) < required_length:
        raise ValueError("Segmento PCD incompleto")

    return {
        "PercentageDetails_01": parts[1] if len(parts) > 1 else "",
        "PercentageDetails_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento CNT
def parse_cnt_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento CNT

    if len(parts) < required_length:
        raise ValueError("Segmento CNT incompleto")

    return {
        "ControlTotalTypeCode_01": parts[1] if len(parts) > 1 else "",
        "ControlTotalValue_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento HAN
def parse_han_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento HAN

    if len(parts) < required_length:
        raise ValueError("Segmento HAN incompleto")

    return {
        "HandlingInstructionsCode_01": parts[1] if len(parts) > 1 else "",
        "HandlingInstructions_02": parts[2] if len(parts) > 2 else "",
        "HandlingInstructions_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento SG20
def parse_sg20_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento SG20

    if len(parts) < required_length:
        raise ValueError("Segmento SG20 incompleto")

    return {
        "ShipmentHandlingCode_01": parts[1] if len(parts) > 1 else "",
        "ShipmentHandlingCodeQualifier_02": parts[2] if len(parts) > 2 else "",
        "ShipmentHandlingInstructions_03": parts[3] if len(parts) > 3 else "",
        "ShipmentHandlingInstructions_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento PIA
def parse_pia_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento PIA

    if len(parts) < required_length:
        raise ValueError("Segmento PIA incompleto")

    return {
        "ProductIdentifierCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "ProductIdentifier_02": parts[2] if len(parts) > 2 else "",
        "ProductIdentifier_03": parts[3] if len(parts) > 3 else ""
    }


# Função para parse do segmento STS
def parse_sts_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento STS

    if len(parts) < required_length:
        raise ValueError("Segmento STS incompleto")

    return {
        "StatusReasonCode_01": parts[1] if len(parts) > 1 else "",
        "StatusReasonCodeQualifier_02": parts[2] if len(parts) > 2 else "",
        "StatusReasonCodeQualifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento AUT
def parse_aut_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento AUT

    if len(parts) < required_length:
        raise ValueError("Segmento AUT incompleto")

    return {
        "AuthenticationResult_01": parts[1] if len(parts) > 1 else "",
        "AuthenticationResult_02": parts[2] if len(parts) > 2 else "",
        "AuthenticationResult_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento TSR
def parse_tsr_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento TSR

    if len(parts) < required_length:
        raise ValueError("Segmento TSR incompleto")

    return {
        "TransportServiceCode_01": parts[1] if len(parts) > 1 else "",
        "TransportServiceCodeQualifier_02": parts[2] if len(parts) > 2 else "",
        "TransportServiceCodeQualifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento DMS
def parse_dms_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento DMS

    if len(parts) < required_length:
        raise ValueError("Segmento DMS incompleto")

    return {
        "DocumentMessageSummary_01": parts[1] if len(parts) > 1 else "",
        "DocumentMessageSummary_02": parts[2] if len(parts) > 2 else "",
        "DocumentMessageSummary_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento DOC
def parse_doc_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento DOC

    if len(parts) < required_length:
        raise ValueError("Segmento DOC incompleto")

    return {
        "DocumentMessageName_01": parts[1] if len(parts) > 1 else "",
        "DocumentMessageIdentifier_02": parts[2] if len(parts) > 2 else "",
        "DocumentMessageStatusCode_03": parts[3] if len(parts) > 3 else "",
        "DocumentMessageSource_04": parts[4] if len(parts) > 4 else ""
    }


# Função para parse do segmento QVR
def parse_qvr_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento QVR

    if len(parts) < required_length:
        raise ValueError("Segmento QVR incompleto")

    return {
        "QuantityVarianceInformation_01": parts[1] if len(parts) > 1 else "",
        "QuantityVarianceInformation_02": parts[2] if len(parts) > 2 else "",
        "QuantityVarianceInformation_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento TCC
def parse_tcc_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento TCC

    if len(parts) < required_length:
        raise ValueError("Segmento TCC incompleto")

    return {
        "TransportChargePaymentMethodCode_01": parts[1] if len(parts) > 1 else "",
        "TransportChargePaymentMethod_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento SGP
def parse_sgp_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento SGP

    if len(parts) < required_length:
        raise ValueError("Segmento SGP incompleto")

    return {
        "ShipmentSplitIndicator_01": parts[1] if len(parts) > 1 else "",
        "ShipmentSplitReasonCode_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento EQN
def parse_eqn_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento EQN

    if len(parts) < required_length:
        raise ValueError("Segmento EQN incompleto")

    return {
        "EquipmentQuantityTypeCode_01": parts[1] if len(parts) > 1 else "",
        "EquipmentQuantity_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento TPL
def parse_tpl_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento TPL

    if len(parts) < required_length:
        raise ValueError("Segmento TPL incompleto")

    return {
        "TransportMovementPriorityCode_01": parts[1] if len(parts) > 1 else "",
        "TransportMovementPriorityCodeQualifier_02": parts[2] if len(parts) > 2 else "",
        "TransportMovementPriorityCodeQualifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento APR
def parse_apr_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento APR

    if len(parts) < required_length:
        raise ValueError("Segmento APR incompleto")

    return {
        "AdditionalPriceInformation_01": parts[1] if len(parts) > 1 else "",
        "AdditionalPriceInformation_02": parts[2] if len(parts) > 2 else "",
        "AdditionalPriceInformation_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento SGP
def parse_sgp_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento SGP

    if len(parts) < required_length:
        raise ValueError("Segmento SGP incompleto")

    return {
        "SplitGoodsInformation_01": parts[1] if len(parts) > 1 else "",
        "SplitGoodsInformation_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento NAD
def parse_nad_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento NAD

    if len(parts) < required_length:
        raise ValueError("Segmento NAD incompleto")

    return {
        "PartyFunctionCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "PartyIdentifier_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento CTA
def parse_cta_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento CTA

    if len(parts) < required_length:
        raise ValueError("Segmento CTA incompleto")

    return {
        "ContactFunctionCode_01": parts[1] if len(parts) > 1 else "",
        "ContactName_02": parts[2] if len(parts) > 2 else ""
    }



# Função para parse do segmento UNZ
def parse_unz_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento UNZ

    if len(parts) < required_length:
        raise ValueError("Segmento UNZ incompleto")

    return {
        "InterchangeControlCount_01": parts[1] if len(parts) > 1 else "",
        "InterchangeControlReference_02": parts[2] if len(parts) > 2 else ""
    }



# Função para parse do segmento CPS
def parse_cps_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento CPS

    if len(parts) < required_length:
        raise ValueError("Segmento CPS incompleto")

    return {
        "ConsignmentPackingSequenceNumber_01": parts[1] if len(parts) > 1 else "",
        "ConsignmentPackingSequenceNumber_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento FTX
def parse_ftx_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento FTX

    if len(parts) < required_length:
        raise ValueError("Segmento FTX incompleto")

    return {
        "FreeTextTypeCode_01": parts[1] if len(parts) > 1 else "",
        "FreeTextQualifier_02": parts[2] if len(parts) > 2 else "",
        "FreeTextQualifier_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento PAC
def parse_pac_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento PAC

    if len(parts) < required_length:
        raise ValueError("Segmento PAC incompleto")

    return {
        "NumberOfPackages_01": parts[1] if len(parts) > 1 else "",
        "NumberOfPackages_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento CNT
def parse_cnt_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento CNT

    if len(parts) < required_length:
        raise ValueError("Segmento CNT incompleto")

    return {
        "ControlTotalTypeCode_01": parts[1] if len(parts) > 1 else "",
        "ControlTotalValue_02": parts[2] if len(parts) > 2 else ""
    }

# Função para parse do segmento QTY
def parse_qty_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento QTY

    if len(parts) < required_length:
        raise ValueError("Segmento QTY incompleto")

    return {
        "QuantityQualifier_01": parts[1] if len(parts) > 1 else "",
        "Quantity_02": parts[2] if len(parts) > 2 else ""
    }



# Função para parse do segmento FTX
def parse_ftx_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento FTX

    if len(parts) < required_length:
        raise ValueError("Segmento FTX incompleto")

    return {
        "FreeTextQualifier_01": parts[1] if len(parts) > 1 else "",
        "FreeText_02": parts[2] if len(parts) > 2 else "",
        "FreeText_03": parts[3] if len(parts) > 3 else ""
    }


# Função para parse do segmento ALC
def parse_alc_segment(parts):
    required_length = 4  # Número mínimo de elementos obrigatórios no segmento ALC

    if len(parts) < required_length:
        raise ValueError("Segmento ALC incompleto")

    return {
        "AllowanceOrChargeCodeQualifier_01": parts[1] if len(parts) > 1 else "",
        "AllowanceOrChargeIdentifier_02": parts[2] if len(parts) > 2 else "",
        "AllowanceOrChargeQualifier_03": parts[3] if len(parts) > 3 else "",
        "AllowanceOrChargeAmount_04": parts[4] if len(parts) > 4 else ""
    }

# Função para parse do segmento LOC
def parse_loc_segment(parts):
    required_length = 3  # Número mínimo de elementos obrigatórios no segmento LOC

    if len(parts) < required_length:
        raise ValueError("Segmento LOC incompleto")

    return {
        "PlaceLocationQualifier_01": parts[1] if len(parts) > 1 else "",
        "PlaceLocationIdentification_02": parts[2] if len(parts) > 2 else "",
        "PlaceLocationDescription_03": parts[3] if len(parts) > 3 else ""
    }

# Função para parse do segmento GIS
def parse_gis_segment(parts):
    required_length = 2  # Número mínimo de elementos obrigatórios no segmento GIS

    if len(parts) < required_length:
        raise ValueError("Segmento GIS incompleto")

    return {
        "GeneralIndicator_01": parts[1] if len(parts) > 1 else "",
        "GeneralIndicatorCode_02": parts[2] if len(parts) > 2 else ""
    }

def parse_uns_segment(parts):
    required_length = 1  # Número mínimo de elementos obrigatórios no segmento UNS

    if len(parts) < required_length:
        raise ValueError("Segmento UNS incompleto")

    return {
        "SectionIdentification_01": parts[1] if len(parts) > 1 else ""
    }
