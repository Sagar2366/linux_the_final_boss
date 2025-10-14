#!/usr/bin/env python3
import re
import os
import glob

def extract_headings(content):
    """Extract headings from markdown content."""
    headings = []
    for line in content.split('\n'):
        if line.startswith('#'):
            # Count the number of # to determine heading level
            level = len(re.match(r'^#+', line).group())
            # Extract heading text
            text = line.lstrip('#').strip()
            # Create anchor link
            anchor = text.lower().replace(' ', '-').replace(':', '').replace('?', '').replace('(', '').replace(')', '').replace('/', '').replace(',', '')
            headings.append((level, text, anchor))
    return headings

def create_toc(headings):
    """Create table of contents from headings."""
    toc = ["## Table of Contents\n"]
    for level, text, anchor in headings:
        # Add indentation based on heading level
        indent = "  " * (level - 1)
        # Create TOC entry with link
        toc.append(f"{indent}- [{text}](#{anchor})")
    return "\n".join(toc)

def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if TOC already exists
    if "## Table of Contents" in content:
        return False
    
    # Extract headings and create TOC
    headings = extract_headings(content)
    toc = create_toc(headings)
    
    # Find the position after the first heading
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and not line.startswith('##'):
            insert_pos = i + 1
            break
    
    # Insert TOC after the first heading
    new_content = '\n'.join(lines[:insert_pos]) + '\n\n' + toc + '\n\n' + '\n'.join(lines[insert_pos:])
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    """Main function to process all markdown files."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pattern = os.path.join(base_dir, 'Day_*', '*.md')
    
    files_processed = 0
    for filepath in glob.glob(pattern):
        if process_file(filepath):
            print(f"Added TOC to {filepath}")
            files_processed += 1
    
    print(f"\nTotal files processed: {files_processed}")

if __name__ == "__main__":
    main()
