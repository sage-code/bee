import os
import time

files = [
    "features.md",
    "syntax.md",
    "structure.md",
    "types.md",
    "control.md",
    "rules.md",
    "functions.md",
    "objects.md",
    "collections.md",
    "processing.md",
    "concurrency.md",
    "graphics.md",
    "library.md"
]

def add_navigation():
    for i, file in enumerate(files):
        path = os.path.join("spec", file)
        prev_file = files[i - 1] if i > 0 else "index.md"
        next_file = files[i + 1] if i < len(files) - 1 else None
        
        nav = f"\n\n---\n\n[Go back]({prev_file})"
        if next_file:
            nav += f" | [Read next]({next_file})"
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Basic check to avoid double-adding
        if "[Go back]" in content:
            print(f"Skipping {file} (already updated)")
            continue
            
        with open(path, "w", encoding="utf-8") as f:
            f.write(content.rstrip() + nav + "\n")
        
        print(f"Updated {file}")
        time.sleep(50)

add_navigation()
