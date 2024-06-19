import xml.etree.ElementTree as ET

def convert_edi_to_xml(edi_segments):
    # Cria um elemento raiz para o XML
    root = ET.Element("ORDERS")

    for segment in edi_segments:
        # Divide o segmento EDI em seus componentes
        parts = segment.split("+")
        segment_name = parts[0]
        segment_data = parts[1:]

        # Cria um elemento para cada segmento EDI
        segment_element = ET.SubElement(root, segment_name)
        segment_element.text = "+".join(segment_data)

    # Cria uma árvore XML a partir do elemento raiz
    tree = ET.ElementTree(root)

    # Converte a árvore XML para uma string
    xml_str = ET.tostring(root, encoding="unicode", method="xml")

    return xml_str

# Dados EDI fornecidos
edi_data = """UNB+UNOB:1+SENDER1:14:ZZUK+RECEIVER1:1:ZZUK+071101:1701+131++ORDERS++1++1'
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

# Transforma os dados EDI em uma lista de segmentos
edi_segments = edi_data.split("\n")

# Converte os segmentos EDI para XML
xml_output = convert_edi_to_xml(edi_segments)

# Imprime o XML resultante
print(xml_output)
