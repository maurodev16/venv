import os

from fastapi import logger

from Api.Modules.parse_segments import *

def read_edifact_file(file_path):
   with open(file_path, 'r') as file:
        lines = file.readlines()

   for line in lines:
        parts = line.strip().split('+')
        segment_name = parts[0]

        if segment_name == "UNH":
            parsed_segment = parse_unh_segment(parts)
        elif segment_name == "BGM":
            parsed_segment = parse_bgm_segment(parts)
        elif segment_name == "DTM":
            parsed_segment = parse_dtm_segment(parts)
        else:
            # Handle other segment types here if needed
            parsed_segment = {"SegmentName": segment_name, "SegmentData": parts[1:]}

        print(f"Parsed Segment ({segment_name}): {parsed_segment}")