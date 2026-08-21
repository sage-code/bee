import os
import re
import time

def process_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        
        # Rule 1: Replace "** " with "-- "
        # We only match if it's the start of the line or indented.
        # We use re.sub to preserve indentation.
        if re.match(r'^\s*\*\*\s', line):
            line = re.sub(r'(\s*)\*\*\s', r'\1-- ', line)
        
        # Rule 2: Replace "# " with "-- " 
        # Requirement: Not if # is inside quotes (a simple heuristic for code files)
        # We check if the line contains a quote before the #.
        # This is a basic heuristic for "#" comments vs strings.
        if re.match(r'^\s*#\s', line):
            # Check for potential string quotes on the line
            if not re.search(r'["\'].*#.*["\']', line):
                line = re.sub(r'(\s*)#\s', r'\1-- ', line)
        
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    # Mandatory pause
    time.sleep(1)

def main():
    root_dir = 'C:\\Users\\eluci\\sage-code\\bee'
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.bee'):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == '__main__':
    main()
