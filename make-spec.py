import os
import time
import re
from bs4 import BeautifulSoup

def convert_html_to_md(html_file, md_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Remove unwanted elements
    for tag in soup(['header', 'footer', 'script', 'style', 'head', 'nav']):
        tag.decompose()

    # Find the main container
    container = soup.find('div', class_='container') or soup.body
    
    md_output = []

    # Iterate through meaningful elements
    for element in container.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'li', 'pre', 'code', 'table', 'tr', 'td', 'th']):
        if element.name == 'h1':
            md_output.append(f"\n# {element.get_text().strip()}\n")
        elif element.name == 'h2':
            md_output.append(f"\n## {element.get_text().strip()}\n")
        elif element.name == 'h3':
            md_output.append(f"\n### {element.get_text().strip()}\n")
        elif element.name == 'p':
            md_output.append(f"\n{element.get_text().strip()}\n")
        elif element.name == 'li':
            md_output.append(f"- {element.get_text().strip()}")
        elif element.name == 'pre':
            md_output.append(f"\n```\n{element.get_text().strip()}\n```\n")
        # Basic table support
        elif element.name == 'table':
            md_output.append("\n| Table |")
            md_output.append("| --- |")
            for row in element.find_all('tr'):
                cols = [col.get_text().strip() for col in row.find_all(['td', 'th'])]
                if cols:
                    md_output.append(f"| {' | '.join(cols)} |")
            md_output.append("\n")

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_output))

def main():
    if not os.path.exists('spec'):
        os.makedirs('spec')
    
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    for html_file in files:
        md_file = os.path.join('spec', html_file.replace('.html', '.md'))
        print(f"Converting {html_file} to {md_file}...")
        convert_html_to_md(html_file, md_file)
        time.sleep(5) 

if __name__ == '__main__':
    main()
