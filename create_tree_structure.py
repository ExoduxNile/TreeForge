import os
import argparse

def parse_tree_file(file_path):
    """Parse the tree diagram from a text file and return a list of (path, is_dir) tuples."""
    structure = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_path = []
    
    for line in lines:
        line = line.rstrip()
        if not line or line.isspace():
            continue
            
        # Count leading characters to determine indentation level
        indent = len(line) - len(line.lstrip('│├└ ─'))
        line = line.lstrip('│├└ ─')
        
        # Adjust current_path to match indentation level
        while len(current_path) > indent // 4:
            current_path.pop()
            
        # Extract name, removing any comments starting with '#'
        name = line.strip().split('#')[0].strip()
        if not name:  # Skip if name is empty after removing comment
            continue
            
        # Determine if it's a directory
        is_dir = name.endswith('/')
        if is_dir:
            name = name[:-1]  # Remove trailing slash
            
        # Build the full path
        full_path = os.path.join(*current_path, name)
        current_path.append(name)
        
        # Store the path and whether it's a directory
        structure.append((full_path, is_dir))
        
        # If it's not a directory, remove the last component for the next iteration
        if not is_dir:
            current_path.pop()
            
    return structure

def create_structure(structure, output_dir):
    """Create directories and files in the output directory based on the parsed structure."""
    for path, is_dir in structure:
        full_path = os.path.join(output_dir, path)
        if is_dir:
            os.makedirs(full_path, exist_ok=True)
        else:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create an empty file
            with open(full_path, 'a'):
                pass

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create directory and file structure from a tree diagram.")
    parser.add_argument('tree_file', help="Path to the text file containing the tree diagram")
    parser.add_argument('output_dir', help="Directory where the structure should be created")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.isfile(args.tree_file):
        print(f"Error: {args.tree_file} does not exist or is not a file.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Parse the tree file and create the structure
    try:
        structure = parse_tree_file(args.tree_file)
        create_structure(structure, args.output_dir)
        print(f"Successfully created structure in {args.output_dir}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
