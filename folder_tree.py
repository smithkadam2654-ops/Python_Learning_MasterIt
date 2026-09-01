import os

def print_tree(directory, prefix=""):
    """
    Recursively prints a visual tree of the given directory structure.
    """
    try:
        # Get list of files/folders and sort them
        items = os.listdir(directory)
        items.sort()
    except PermissionError:
        print(f"{prefix}└── [Access Denied]")
        return
        
    # We want to format the last item differently to close the branch visually
    pointers = ["├── "] * (len(items) - 1) + ["└── "] if items else []
    
    for pointer, item in zip(pointers, items):
        # Optional: Skip hidden files and git directories to keep the tree clean
        if item.startswith('.') or item == '__pycache__':
            continue
            
        path = os.path.join(directory, item)
        print(f"{prefix}{pointer}{item}")
        
        # If it's a directory, recurse into it
        if os.path.isdir(path):
            # Extend the prefix for children of this directory
            extension = "│   " if pointer == "├── " else "    "
            print_tree(path, prefix=prefix + extension)

if __name__ == "__main__":
    print("--- 🌳 Directory Tree Visualizer ---")
    folder_path = input("Enter a folder path (or press Enter for current directory): ")
    
    if not folder_path.strip():
        folder_path = os.getcwd()
        
    print(f"\nTree for: {folder_path}\n")
    print(os.path.basename(folder_path) or folder_path)
    print_tree(folder_path)
