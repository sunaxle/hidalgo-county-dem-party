import re
import sys
from datetime import datetime


def update_data(count, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    js_path = "js/voter_reg_data.js"

    with open(js_path) as f:
        content = f.read()

    # Find the array of data
    pattern = r"(const\s+voterRegistrationData\s*=\s*\[)(.*?)(\];)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        start_tag = match.group(1)
        data_block = match.group(2).rstrip()
        end_tag = match.group(3)

        # Remove the last comma if there is one
        if data_block.endswith(","):
            data_block = data_block[:-1]

        # Append the new data point
        new_data_point = f",\n  {{ date: '{date_str}', count: {count} }}\n"

        new_content = (
            content[: match.start()]
            + start_tag
            + data_block
            + new_data_point
            + end_tag
            + content[match.end() :]
        )

        with open(js_path, "w") as f:
            f.write(new_content)
        print(f"Successfully added {count} voters on {date_str} to tracking data.")
    else:
        print("Could not find the voterRegistrationData array in js/voter_reg_data.js")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_voter_registration_data.py <count> [YYYY-MM-DD]")
        sys.exit(1)

    count = int(sys.argv[1].replace(",", ""))
    date_str = sys.argv[2] if len(sys.argv) > 2 else None

    update_data(count, date_str)
