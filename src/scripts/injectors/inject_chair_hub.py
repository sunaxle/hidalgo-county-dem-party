import glob
import os

directory = "."
files_modified = 0

for filepath in glob.glob(os.path.join(directory, "*.html")):
    with open(filepath) as f:
        lines = f.readlines()

    new_lines = []
    modified = False

    for i, line in enumerate(lines):
        if '<a href="precinct_chairs.html">Precinct Chairs</a>' in line:
            # Check if we already added it
            if i > 0 and "chair_onboarding.html" in lines[i - 1]:
                new_lines.append(line)
                continue

            indent = line[: len(line) - len(line.lstrip())]
            new_lines.append(
                f'{indent}<a href="chair_onboarding.html" style="color: #fcd34d; font-weight: 800;">Chair Hub 🧭</a>\n'
            )
            new_lines.append(line)
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(filepath, "w") as f:
            f.writelines(new_lines)
        print(f"✅ Injected Chair Hub into {os.path.basename(filepath)}")
        files_modified += 1

print(f"\nOperation Complete. Modified {files_modified} files.")
