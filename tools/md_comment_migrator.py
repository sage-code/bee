import os
import re
import time

def process_spec_file(filepath):
    print(f"Processing spec file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all code blocks ```...```
    # We use re.DOTALL to match across newlines
    def replace_comments_in_block(match):
        block_content = match.group(1)
        
        # Replace "** " with "-- "
        block_content = re.sub(r'(?m)^\s*\*\*\s', '-- ', block_content)
        
        # Replace "# " with "-- " 
        # Only replace if line starts with # (or whitespace + #)
        # We ensure we don't accidentally match things that aren't comment lines
        block_content = re.sub(r'(?m)^(\s*)#(?!\S)', r'\1-- ', block_content)
        
        return f"```{block_content}```"

    new_content = re.sub(r'```(.*?)```', replace_comments_in_block, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    time.sleep(1)

def main():
    spec_dir = 'C:\\Users\\eluci\\sage-code\\bee\\spec'
    for root, dirs, files in os.walk(spec_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_spec_file(filepath)

if __name__ == '__main__':
    main()
