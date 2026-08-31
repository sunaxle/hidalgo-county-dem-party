import os, glob

replacements = [
    ("+1-956-672-7274", "+1-956-212-0476"),
    ("(956) 672-7274", "(956) 212-0476"),
    ("956-672-7274", "956-212-0476"),
    ("9566727274", "9562120476"),
    ("(956) 672 7274", "(956) 212 0476"),
    ("956.672.7274", "956.212.0476"),
]

modified_files = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv", "__pycache__", ".gstack", "Elections_Data", "2026_Election_Data")]
    for file in files:
        if file.endswith((".html", ".js", ".json", ".md", ".txt", ".css", ".offline")):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                
                new_content = content
                for old_val, new_val in replacements:
                    new_content = new_content.replace(old_val, new_val)
                
                if new_content != content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    modified_files.append(filepath)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"Modified {len(modified_files)} files:")
for f in modified_files:
    print(f" - {f}")

