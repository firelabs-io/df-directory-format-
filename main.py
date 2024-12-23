import os
import shutil

def faddf(file, folder, current_dir):
    dot = {
        '.png': 'image/png', 
        '.jpg': 'image/jpg',
        '.jpeg': 'image/jpeg',
        '.bmp': 'image/bmp',
        '.txt': 'document/text',
        '.md': 'document/markdown',
        '.bin': 'binary/linux',
        '.exe': 'binary/windows'
    }
    
    matched = False
    for ext, label in dot.items():
        if ext in file.lower():
            category, subcategory = label.split('/')
            if category not in folder:
                folder[category] = {}
            if subcategory not in folder[category]:
                folder[category][subcategory] = []
            folder[category][subcategory].append(file)
            matched = True
            break
    
    # If no match was found and the file has an extension
    if not matched:
        ext = os.path.splitext(file)[1].lower()
        if ext:  # Only add if it has an extension
            category = ext[1:]  # Remove the dot
            if category not in folder:
                folder[category] = []
            folder[category].append(file)
    
    # Move the file to the appropriate directory (except for the script itself)
    if file != os.path.basename(__file__):  # Ensure the running script is not moved
        move_file(file, folder, current_dir)

def move_file(file, folder, current_dir):
    # Find the category path to move the file into
    file_path = os.path.join(current_dir, file)
    
    # For unmatched extension, move to category based on extension
    ext = os.path.splitext(file)[1].lower()
    category = ext[1:] if ext else None

    # Check where to move the file
    if category:
        target_dir = os.path.join(current_dir, category)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.move(file_path, os.path.join(target_dir, file))

if __name__ == '__main__':
    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
    folder = {}

    for file in files:
        faddf(file, folder, current_dir)

    # Printing the updated structure
    def print_tree(d, indent=0):
        for key, value in d.items():
            print(' ' * indent + key + '/')
            if isinstance(value, dict):
                print_tree(value, indent + 4)
            elif isinstance(value, list):
                for item in value:
                    print(' ' * (indent + 4) + item)

    print_tree(folder)
