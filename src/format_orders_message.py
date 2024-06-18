from Api.Modules import parse_edi_message


def format_orders_message(parsed_data):
    orders_message = {
        "UNB": parsed_data.get("UNB", {}),
        "Groups": []
    }

    groups = parsed_data.get("Groups", [])
    for group in groups:
        transactions = group.get("Transactions", [])
        formatted_transactions = []
        for transaction in transactions:
            formatted_transaction = {
                "UNH": transaction.get("UNH", {}),
                "BGM": transaction.get("BGM", {}),
                "DTM": transaction.get("DTM", []),
                # Adicionar outros segmentos conforme necessário
            }
            if "NADLoop" in transaction:
                formatted_transaction["NADLoop"] = transaction["NADLoop"]
            formatted_transactions.append(formatted_transaction)

        orders_message["Groups"].append({"Transactions": formatted_transactions})

    return orders_message

# Exemplo de uso para parsear a mensagem EDI e formatar para retorno
edi_content = """UNB+UNOB:1+SENDER1:14:ZZUK+RECEIVER1:1:ZZUK+071101:1701+131++ORDERS++1++1'
UNH+000000101+ORDERS:D:96A:UN'
BGM+220+128576+9'
DTM+137:20020830:102'
PAI+::42'
FTX+ZZZ+1+001::91'
RFF+CT:652744'
DTM+171:20020825:102'
NAD+BY+5412345000013::9'
RFF+VA:87765432'
CTA+OC+:P FORGET'
COM+0044715632478:TE'
NAD+SU+4012345500004::9'
RFF+VA:56225432'
CUX+2:GBP:9+3:EUR:4+1.67'
DTM+134:2002080120020831:718'
TDT+20++30+31'
TOD+3++CIF:23:9'
LOC+1+BE-BRU'
LIN+1++4000862141404:SRS'
PIA+1+ABC1234:IN'
IMD+C++TU::9'
QTY+21:48'
MOA+203:699.84'
PRI+AAA:14.58:CT:AAE:1:KGM'
RFF+PL:AUG93RNG04'
DTM+171:20020801:102'
PAC+2+:51+CS'
PCI+14'
LOC+7+3312345502000::9'
QTY+11:24'
DTM+2:20020915:102'
LOC+7+3312345501003::9'
QTY+11:24'
DTM+2:20020913:102'
TAX+7+VAT+++:::17.5+S'
UNS+S'
CNT+2:1'
UNT+38+000000101'
UNZ+1+131'"""

parsed_data = parse_edi_message(edi_content)
formatted_message = format_orders_message(parsed_data)
print(formatted_message)
