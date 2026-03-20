import csv

try:
    with open('data/mock_volunteers.csv', 'r') as f:
        content = f.read()
        
    lines = [x for x in content.splitlines() if x.strip()]
    print(f"Total Lines: {len(lines)}")
    if len(lines) > 1:
        headers = [x.strip() for x in lines[0].split(',')]
        print(f"Headers: {headers}")
        
    data = []
    
    for row in lines[1:]:
        row_values = []
        in_quotes = False
        curr_val = ""
        
        for char in row:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                row_values.append(curr_val.strip())
                curr_val = ""
            else:
                curr_val += char
                
        row_values.append(curr_val.strip())
        
        obj = {}
        for idx, h in enumerate(headers):
            if idx < len(row_values):
                obj[h] = row_values[idx]
        data.append(obj)

    chairs = [d for d in data if d.get("Role", "") in ["Precinct Chair", "Block Captain"]]
    print(f"Parsed {len(data)} rows successfully!")
    print(f"Found {len(chairs)} chairs/captains.")
    if chairs:
        print(f"Example: {chairs[0]['First Name']} {chairs[0]['Last Name']} ({chairs[0]['Role']} Pct {chairs[0]['Precinct Number']})")
        
except Exception as e:
    print(f"Error: {e}")
