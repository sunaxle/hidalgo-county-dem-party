with open('elected_officials.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:578] + lines[976:]

with open('elected_officials.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed HTML bounds.")
