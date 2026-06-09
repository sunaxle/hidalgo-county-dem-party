import sys
import xml.etree.ElementTree as ET


def parse_xml(file_path, year):
    print(f"--- {year} General Election ({file_path}) ---")
    namespace = {"s": "urn:schemas-microsoft-com:office:spreadsheet"}
    context = ET.iterparse(file_path, events=("start", "end"))

    current_sheet = ""
    row_count = 0
    header = []

    for event, elem in context:
        tag = elem.tag.split("}")[-1]

        if event == "start" and tag == "Worksheet":
            current_sheet = elem.attrib.get(
                "{urn:schemas-microsoft-com:office:spreadsheet}Name", "Unknown"
            )
            row_count = 0
            header = []

        elif event == "start" and tag == "Row":
            current_row = []
            row_count += 1

        elif event == "end" and tag == "Cell":
            data_elem = elem.find("s:Data", namespace)
            if data_elem is not None and data_elem.text is not None:
                current_row.append(data_elem.text.strip())
            else:
                current_row.append("")

        elif event == "end" and tag == "Row":
            if row_count <= 2 and not header and any(current_row):
                header = current_row

            if current_row and (current_row[0] == "107" or current_row[0] == "0107"):
                if "Registered Voters" in current_sheet:
                    print(f"Sheet: {current_sheet}")
                    print(f"  Header: {header}")
                    print(f"  107   : {current_row}")
                elif (
                    "President" in current_sheet
                    or "Governor" in current_sheet
                    or "Senator" in current_sheet
                    or "US Rep" in current_sheet
                    or "U.S. Rep" in current_sheet
                ):
                    print(f"Sheet: {current_sheet}")
                    print(f"  Header: {header}")
                    print(f"  107   : {current_row}")
            elem.clear()


parse_xml("precinct_107_data_upload/detail 2.xls", "2022")
parse_xml("precinct_107_data_upload/detail.xls", "2024")
