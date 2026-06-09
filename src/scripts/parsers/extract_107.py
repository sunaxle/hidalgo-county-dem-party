import sys
import xml.etree.ElementTree as ET


def parse_xml_spreadsheet(file_path):
    print(f"Parsing {file_path}")
    namespace = {"s": "urn:schemas-microsoft-com:office:spreadsheet"}

    context = ET.iterparse(file_path, events=("start", "end"))

    current_sheet_name = ""
    current_row_data = []

    # We want to keep track of the header row (row 1 or 2 of the sheet)
    header_row = []
    row_count = 0

    for event, elem in context:
        # Get local tag name without namespace
        tag = elem.tag.split("}")[-1]

        if event == "start" and tag == "Worksheet":
            current_sheet_name = elem.attrib.get(
                "{urn:schemas-microsoft-com:office:spreadsheet}Name", "Unknown"
            )
            row_count = 0
            header_row = []

        elif event == "start" and tag == "Row":
            current_row_data = []
            row_count += 1

        elif event == "end" and tag == "Cell":
            # Find the Data element inside the Cell
            data_elem = elem.find("s:Data", namespace)
            if data_elem is not None and data_elem.text is not None:
                current_row_data.append(data_elem.text.strip())
            else:
                current_row_data.append("")

        elif event == "end" and tag == "Row":
            if row_count <= 2 and not header_row and any(current_row_data):
                header_row = current_row_data

            # If the row has "107" in it, print it
            if "107" in current_row_data or "0107" in current_row_data:
                print(f"[{current_sheet_name}] Header: {header_row}")
                print(f"[{current_sheet_name}] Data:   {current_row_data}")

            elem.clear()  # Free memory

    print("Done parsing.\n")


parse_xml_spreadsheet("precinct_107_data_upload/detail.xls")
parse_xml_spreadsheet("precinct_107_data_upload/detail 2.xls")
