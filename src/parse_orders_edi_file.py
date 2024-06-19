import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_orders_edi_file(segments_list):
    parsed_data = {"Groups": []}
    current_group = {"Transactions": []}
    current_transaction = None

    for segment in segments_list:
        try:
            parts = segment.split("+")
            segment_name = parts[0]

            if segment_name == "UNB":
                parsed_data["UNB"] = parse_unb_segment(parts)
            elif segment_name == "UNH":
                if current_transaction:
                    current_group["Transactions"].append(current_transaction)
                current_transaction = {"UNH": parse_unh_segment(parts)}
            elif segment_name == "BGM":
                current_transaction["BGM"] = parse_bgm_segment(parts)
            elif segment_name == "DTM":
                if "DTM" not in current_transaction:
                    current_transaction["DTM"] = []
                current_transaction["DTM"].append(parse_dtm_segment(parts))
            elif segment_name == "NAD":
                if "NADLoop" not in current_transaction:
                    current_transaction["NADLoop"] = []
                current_transaction["NADLoop"].append({"NAD": parse_nad_segment(parts)})
            elif segment_name == "PAI":
                if "PAILoop" not in current_transaction:
                    current_transaction["PAILoop"] = []
                current_transaction["PAILoop"].append({"PAI": parse_pai_segment(parts)})
            elif segment_name == "FTX":
                if "FTXLoop" not in current_transaction:
                    current_transaction["FTXLoop"] = []
                current_transaction["FTXLoop"].append({"FTX": parse_ftx_segment(parts)})
            elif segment_name == "RFF":
                if "RFFLoop" not in current_transaction:
                    current_transaction["RFFLoop"] = []
                current_transaction["RFFLoop"].append({"RFF": parse_rff_segment(parts)})
            elif segment_name == "CTA":
                if "CTALoop" not in current_transaction:
                    current_transaction["CTALoop"] = []
                current_transaction["CTALoop"].append({"CTA": parse_cta_segment(parts)})
            elif segment_name == "COM":
                if "COMLoop" not in current_transaction:
                    current_transaction["COMLoop"] = []
                current_transaction["COMLoop"].append({"COM": parse_com_segment(parts)})
            elif segment_name == "CUX":
                if "CUXLoop" not in current_transaction:
                    current_transaction["CUXLoop"] = []
                current_transaction["CUXLoop"].append({"CUX": parse_cux_segment(parts)})
            elif segment_name == "TDT":
                if "TDTLoop" not in current_transaction:
                    current_transaction["TDTLoop"] = []
                current_transaction["TDTLoop"].append({"TDT": parse_tdt_segment(parts)})
            elif segment_name == "TOD":
                if "TODLoop" not in current_transaction:
                    current_transaction["TODLoop"] = []
                current_transaction["TODLoop"].append({"TOD": parse_tod_segment(parts)})
            elif segment_name == "LOC":
                if "LOCLoop" not in current_transaction:
                    current_transaction["LOCLoop"] = []
                current_transaction["LOCLoop"].append({"LOC": parse_loc_segment(parts)})
            elif segment_name == "LIN":
                if "LINLoop" not in current_transaction:
                    current_transaction["LINLoop"] = []
                current_transaction["LINLoop"].append({"LIN": parse_lin_segment(parts)})
            elif segment_name == "PIA":
                if "PIALoop" not in current_transaction:
                    current_transaction["PIALoop"] = []
                current_transaction["PIALoop"].append({"PIA": parse_pia_segment(parts)})
            elif segment_name == "IMD":
                if "IMDLoop" not in current_transaction:
                    current_transaction["IMDLoop"] = []
                current_transaction["IMDLoop"].append({"IMD": parse_imd_segment(parts)})
            elif segment_name == "QTY":
                if "QTYLoop" not in current_transaction:
                    current_transaction["QTYLoop"] = []
                current_transaction["QTYLoop"].append({"QTY": parse_qty_segment(parts)})
            elif segment_name == "MOA":
                if "MOALoop" not in current_transaction:
                    current_transaction["MOALoop"] = []
                current_transaction["MOALoop"].append({"MOA": parse_moa_segment(parts)})
            elif segment_name == "PRI":
                if "PRILoop" not in current_transaction:
                    current_transaction["PRILoop"] = []
                current_transaction["PRILoop"].append({"PRI": parse_pri_segment(parts)})
            elif segment_name == "PAC":
                if "PACLoop" not in current_transaction:
                    current_transaction["PACLoop"] = []
                current_transaction["PACLoop"].append({"PAC": parse_pac_segment(parts)})
            elif segment_name == "PCI":
                if "PCILoop" not in current_transaction:
                    current_transaction["PCILoop"] = []
                current_transaction["PCILoop"].append({"PCI": parse_pci_segment(parts)})
            elif segment_name == "TAX":
                if "TAXLoop" not in current_transaction:
                    current_transaction["TAXLoop"] = []
                current_transaction["TAXLoop"].append({"TAX": parse_tax_segment(parts)})
            elif segment_name == "UNS":
                current_transaction["UNS"] = parse_uns_segment(parts)
            elif segment_name == "CNT":
                if "CNT" not in current_transaction:
                    current_transaction["CNT"] = []
                current_transaction["CNT"].append(parse_cnt_segment(parts))
            elif segment_name == "UNT":
                current_transaction["UNT"] = parse_unt_segment(parts)
                current_group["Transactions"].append(current_transaction)
                current_transaction = None
            elif segment_name == "UNZ":
                parsed_data["UNZ"] = parse_unz_segment(parts)
                parsed_data["Groups"].append(current_group)
                current_group = {"Transactions": []}
            else:
                logger.warning(f"Segmento não reconhecido: {segment_name}")

        except Exception as e:
            logger.error(f"Erro ao processar segmento {segment_name}: {str(e)}")

    if current_transaction:
        current_group["Transactions"].append(current_transaction)
    if current_group["Transactions"]:
        parsed_data["Groups"].append(current_group)

    return parsed_data

def parse_unb_segment(parts):
    required_length = 12  # Número mínimo de elementos obrigatórios no segmento UNB

    if len(parts) < required_length:
        raise ValueError("Segmento UNB incompleto")

    unb_dict = {
        "SYNTAXIDENTIFIER_1": {
            "SyntaxIdentifier_1": parts[1].split(":")[0].strip() if len(parts) > 1 else "",
            "SyntaxVersionNumber_2": parts[1].split(":")[1].strip() if len(parts) > 1 else ""
        },
        "INTERCHANGESENDER_2": {
            "InterchangeSenderIdentification_1": parts[2].split(":")[0].strip() if len(parts) > 2 else "",
            "IdentificationCodeQualifier_2": parts[2].split(":")[1].strip() if len(parts) > 2 else "",
            "InterchangeSenderInternalIdentification_3": parts[2].split(":")[2].strip() if len(parts) > 2 else ""
        },
        "INTERCHANGERECIPIENT_3": {
            "InterchangeRecipientIdentification_1": parts[3].split(":")[0].strip() if len(parts) > 3 else "",
            "IdentificationCodeQualifier_2": parts[3].split(":")[1].strip() if len(parts) > 3 else "",
            "InterchangeRecipientInternalIdentification_3": parts[3].split(":")[2].strip() if len(parts) > 3 else ""
        },
        "DATEANDTIMEOFPREPARATION_4": {
            "Date_1": parts[4].split(":")[0].strip() if len(parts) > 4 else "",
            "Time_2": parts[4].split(":")[1].strip() if len(parts) > 4 else ""
        },
        "InterchangeControlReference_5": parts[5].strip() if len(parts) > 5 else "",
        "ApplicationReference_7": parts[7].strip() if len(parts) > 7 else "",
        "AcknowledgementRequest_9": parts[9].strip() if len(parts) > 9 else "",
        "TestIndicator_11": parts[11].strip().rstrip("'") if len(parts) > 11 else ""
    }

    return unb_dict


def parse_unh_segment(parts):
    if not parts:
        raise ValueError("Segmento UNH vazio")

    if len(parts) < 2:
        raise ValueError("Segmento UNH incompleto")

    message_reference = parts[1]
    message_type_version = parts[2] if len(parts) > 2 else ""

    unh_dict = {
        "MessageReferenceNumber_01": message_reference,
        "MessageIdentifier_02": {
            "MessageType_01": "",
            "MessageVersionNumber_02": "",
            "MessageReleaseNumber_03": "",
            "ControllingAgencyCoded_04": ""
        }
    }

    if message_type_version:
        type_version_parts = message_type_version.split(":")
        if len(type_version_parts) > 0:
            unh_dict["MessageIdentifier_02"]["MessageType_01"] = type_version_parts[0].strip()
        if len(type_version_parts) > 1:
            unh_dict["MessageIdentifier_02"]["MessageVersionNumber_02"] = type_version_parts[1].strip()
        if len(type_version_parts) > 2:
            unh_dict["MessageIdentifier_02"]["MessageReleaseNumber_03"] = type_version_parts[2].strip()
        if len(type_version_parts) > 3:
            unh_dict["MessageIdentifier_02"]["ControllingAgencyCoded_04"] = type_version_parts[3].strip()

    return unh_dict


def parse_bgm_segment(parts):
    if not parts:
        raise ValueError("Segmento BGM vazio")

    if len(parts) < 4:
        raise ValueError("Segmento BGM incompleto")

    bgm_dict = {
        "DOCUMENTMESSAGENAME_01": {
            "Documentmessagenamecoded_01": parts[1].strip()
        },
        "Documentmessagenumber_02": parts[2].strip(),
        "Messagefunctioncoded_03": parts[3].strip() if len(parts) > 3 else ""
    }

    return bgm_dict

def parse_dtm_segment(parts):
    if not parts:
        raise ValueError("Segmento DTM vazio")

    if len(parts) < 2:
        raise ValueError("Segmento DTM incompleto")

    dtm_subparts = parts[1].split(":")
    if len(dtm_subparts) < 3:
        raise ValueError("Segmento DTM incompleto")

    dtm_dict = {
        "DATETIMEPERIOD_01": {
            "Datetimeperiodqualifier_01": dtm_subparts[0].strip(),
            "Datetimeperiod_02": dtm_subparts[1].strip(),
            "Datetimeperiodformatqualifier_03": dtm_subparts[2].strip()
        }
    }

    return dtm_dict


def parse_pai_segment(parts):
    if not parts:
        raise ValueError("Segmento PAI vazio")

    if len(parts) < 2:
        raise ValueError("Segmento PAI incompleto")

    # Vamos capturar apenas a parte após "::" se existir
    payment_means_coded = parts[1].split("::")[-1].strip().rstrip("'")

    pai_dict = {
        "PAI": {
            "PAYMENTINSTRUCTIONDETAILS_01": {
                "Paymentmeanscoded_03": payment_means_coded
            }
        }
    }

    return pai_dict

def parse_ftx_segment(parts):
    if not parts:
        raise ValueError("Segmento FTX vazio")

    if len(parts) < 3:
        raise ValueError("Segmento FTX incompleto")

    ftx_dict = {
        "TextSubjectQualifier_01": parts[1].strip(),
        "FreeText_02": parts[2].strip()
    }

    if len(parts) > 3:
        ftx_dict["TextReference_03"] = {
            "FreeTextCoded_01": parts[3].strip(),
            "CodeListResponsibleAgencyCoded_03": parts[4].strip() if len(parts) > 4 else ""
        }

    return ftx_dict


def parse_nad_segment(parts):
    if not parts:
        raise ValueError("Segmento NAD vazio")

    if len(parts) < 2:
        raise ValueError("Segmento NAD incompleto")

    nad_dict = {
        "PartyFunctionCodeQualifier_01": parts[1].strip(),
        "PartyIdentificationDetails_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return nad_dict


def parse_cux_segment(parts):
    if not parts:
        raise ValueError("Segmento CUX vazio")

    if len(parts) < 2:
        raise ValueError("Segmento CUX incompleto")

    cux_dict = {
        "CurrenciesQualifier_01": parts[1].strip(),
        "CurrencyDetails_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return cux_dict


def parse_tdt_segment(parts):
    if not parts:
        raise ValueError("Segmento TDT vazio")

    if len(parts) < 2:
        raise ValueError("Segmento TDT incompleto")

    tdt_dict = {
        "TransportStageQualifier_01": parts[1].strip(),
        "TransportMeansIdentificationName_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return tdt_dict


def parse_tod_segment(parts):
    if not parts:
        raise ValueError("Segmento TOD vazio")

    if len(parts) < 2:
        raise ValueError("Segmento TOD incompleto")

    tod_dict = {
        "TimeModeQualifier_01": parts[1].strip(),
        "Time_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return tod_dict


def parse_lin_segment(parts):
    if not parts:
        raise ValueError("Segmento LIN vazio")

    if len(parts) < 2:
        raise ValueError("Segmento LIN incompleto")

    lin_dict = {
        "LineItemIdentifier_01": parts[1].strip(),
        "ActionRequestNotification_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return lin_dict


def parse_pia_segment(parts):
    if not parts:
        raise ValueError("Segmento PIA vazio")

    if len(parts) < 2:
        raise ValueError("Segmento PIA incompleto")

    pia_dict = {
        "ProductIdentifierCode_01": parts[1].strip(),
        "ItemNumberIdentification_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return pia_dict


def parse_imd_segment(parts):
    if not parts:
        raise ValueError("Segmento IMD vazio")

    if len(parts) < 2:
        raise ValueError("Segmento IMD incompleto")

    imd_dict = {
        "ItemDescriptionType_01": parts[1].strip(),
        "CodeListIdentificationCode_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return imd_dict


def parse_qty_segment(parts):
    if not parts:
        raise ValueError("Segmento QTY vazio")

    if len(parts) < 2:
        raise ValueError("Segmento QTY incompleto")

    qty_dict = {
        "QuantityDetailsQualifier_01": parts[1].strip(),
        "Quantity_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return qty_dict


def parse_moa_segment(parts):
    if not parts:
        raise ValueError("Segmento MOA vazio")

    if len(parts) < 2:
        raise ValueError("Segmento MOA incompleto")

    moa_dict = {
        "MonetaryAmountTypeQualifier_01": parts[1].strip(),
        "MonetaryAmount_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return moa_dict


def parse_pri_segment(parts):
    if not parts:
        raise ValueError("Segmento PRI vazio")

    if len(parts) < 2:
        raise ValueError("Segmento PRI incompleto")

    pri_dict = {
        "PriceDetailsQualifier_01": parts[1].strip(),
        "Price_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return pri_dict


def parse_rff_segment(parts):
    if not parts:
        raise ValueError("Segmento RFF vazio")

    if len(parts) < 2:
        raise ValueError("Segmento RFF incompleto")

    rff_dict = {
        "ReferenceQualifier_01": parts[1].strip(),
        "ReferenceNumber_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return rff_dict


def parse_pac_segment(parts):
    if not parts:
        raise ValueError("Segmento PAC vazio")

    if len(parts) < 2:
        raise ValueError("Segmento PAC incompleto")

    pac_dict = {
        "NumberOfPackages_01": parts[1].strip(),
        "PackageTypeDescriptionCode_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return pac_dict


def parse_pci_segment(parts):
    if not parts:
        raise ValueError("Segmento PCI vazio")

    if len(parts) < 2:
        raise ValueError("Segmento PCI incompleto")

    pci_dict = {
        "PackageItemNumber_01": parts[1].strip(),
        "PackageItemNumberTypeCodeQualifier_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return pci_dict


def parse_loc_segment(parts):
    if not parts:
        raise ValueError("Segmento LOC vazio")

    if len(parts) < 2:
        raise ValueError("Segmento LOC incompleto")

    loc_dict = {
        "PlaceLocationIdentification_01": parts[1].strip(),
        "LocationFunctionCodeQualifier_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return loc_dict


def parse_tax_segment(parts):
    if not parts:
        raise ValueError("Segmento TAX vazio")

    if len(parts) < 2:
        raise ValueError("Segmento TAX incompleto")

    tax_dict = {
        "DutyTaxFeeAccountDetail_01": parts[1].strip(),
        "DutyTaxFeeAssessmentDetails_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return tax_dict


def parse_uns_segment(parts):
    if not parts:
        raise ValueError("Segmento UNS vazio")

    if len(parts) < 2:
        raise ValueError("Segmento UNS incompleto")

    uns_dict = {
        "SectionControl_01": parts[1].strip(),
        "ControlValue_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return uns_dict


def parse_cnt_segment(parts):
    if not parts:
        raise ValueError("Segmento CNT vazio")

    if len(parts) < 2:
        raise ValueError("Segmento CNT incompleto")

    cnt_dict = {
        "ControlQualifier_01": parts[1].strip(),
        "ControlValue_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return cnt_dict


def parse_com_segment(parts):
    if not parts:
        raise ValueError("Segmento COM vazio")

    if len(parts) < 2:
        raise ValueError("Segmento COM incompleto")

    com_dict = {
        "CommunicationContactFunctionCode_01": parts[1].strip(),
        "CommunicationContactDetails_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return com_dict



def parse_cta_segment(parts):
    if not parts:
        raise ValueError("Segmento CTA vazio")

    if len(parts) < 2:
        raise ValueError("Segmento CTA incompleto")

    cta_dict = {
        "ContactFunctionCodeQualifier_01": parts[1].strip(),
        "DepartmentOrEmployeeDetails_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return cta_dict


def parse_unt_segment(parts):
    if not parts:
        raise ValueError("Segmento UNT vazio")

    if len(parts) < 2:
        raise ValueError("Segmento UNT incompleto")

    unt_dict = {
        "NumberOfSegmentsInMessage_01": parts[1].strip(),
        "MessageReferenceNumber_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return unt_dict


def parse_unz_segment(parts):
    if not parts:
        raise ValueError("Segmento UNZ vazio")

    if len(parts) < 2:
        raise ValueError("Segmento UNZ incompleto")

    unz_dict = {
        "InterchangeControlCount_01": parts[1].strip(),
        "InterchangeControlReference_02": parts[2].strip() if len(parts) > 2 else ""
    }

    return unz_dict




