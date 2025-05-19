#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import sys

def parse_tree_file(file_path):
    """Parse the tree diagram from a text file and return a list of paths with type."""
    structure = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.isspace():
                continue
                
            # Remove any tree diagram characters and leading/trailing whitespace
            line = line.lstrip('│├└─ ')
            
            # Skip lines that are just tree structure characters
            if not line or all(c in '│├└─ ' for c in line):
                continue
                
            # Extract the path, removing comments
            path = line.split('#')[0].strip()
            if not path:
                continue
                
            # Determine if it's a directory
            is_dir = path.endswith('/')
            if is_dir:
                path = path[:-1]  # Remove trailing slash
                
            structure.append((path, is_dir))
            
    return structure

def create_structure(structure, output_dir):
    """Create directories and files in the output directory."""
    # First create all directories
    for path, is_dir in structure:
        if is_dir:
            full_path = os.path.join(output_dir, path)
            try:
                os.makedirs(full_path, exist_ok=True)
                print(f"Created directory: {full_path}")
            except OSError as e:
                print(f"Error creating directory {full_path}: {e}", file=sys.stderr)
    
    # Then create all files
    for path, is_dir in structure:
        if not is_dir:
            full_path = os.path.join(output_dir, path)
            try:
                # Ensure parent directory exists
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                # Create empty file
                with open(full_path, 'a'):
                    pass
                print(f"Created file: {full_path}")
            except OSError as e:
                print(f"Error creating file {full_path}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Create directory and file structure from a tree diagram.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        'tree_file',
        help="Path to the text file containing the tree diagram"
    )
    parser.add_argument(
        'output_dir',
        help="Directory where the structure should be created"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.isfile(args.tree_file):
        print(f"Error: Input file '{args.tree_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Convert output_dir to absolute path
    output_dir = os.path.abspath(args.output_dir)
    
    # Parse the tree file
    try:
        structure = parse_tree_file(args.tree_file)
    except Exception as e:
        print(f"Error parsing tree file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Create the structure
    try:
        os.makedirs(output_dir, exist_ok=True)
        create_structure(structure, output_dir)
        print(f"\nSuccessfully created structure in: {output_dir}")
    except Exception as e:
        print(f"Error creating structure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
