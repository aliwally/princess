import os
import sys
from PIL import Image
import imagehash
from pathlib import Path

def get_image_files(folder_path):
    """Recursively gets all image files in the folder."""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}
    image_files = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if Path(file).suffix.lower() in valid_extensions:
                image_files.append(Path(root) / file)
    return image_files

def calculate_hash(image_path):
    """Calculates the perceptual hash of an image."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (handles PNG with transparency, etc.)
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            return imagehash.phash(img)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_and_delete_duplicates(folder_path, threshold=5):
    """
    Finds and deletes duplicate images based on perceptual hash.
    
    Args:
        folder_path (str): Path to the folder containing images.
        threshold (int): Maximum hash difference to consider images as duplicates.
                         Lower = stricter. 0 means identical hash. 5 allows slight compression differences.
    """
    print(f"Scanning folder: {folder_path}")
    image_files = get_image_files(folder_path)
    
    if not image_files:
        print("No images found.")
        return

    hashes = {}
    duplicates_found = 0

    print(f"Found {len(image_files)} images. Calculating hashes...")

    for img_path in image_files:
        img_hash = calculate_hash(img_path)
        
        if img_hash is None:
            continue

        is_duplicate = False
        duplicate_of = None

        # Compare with existing hashes
        for existing_hash, existing_path in hashes.items():
            diff = img_hash - existing_hash
            if diff <= threshold:
                is_duplicate = True
                duplicate_of = existing_path
                break
        
        if is_duplicate:
            print(f"Duplicate found: {img_path}")
            print(f"  -> Matches: {duplicate_of} (Difference: {diff})")
            try:
                os.remove(img_path)
                print(f"  -> Deleted: {img_path}")
                duplicates_found += 1
            except PermissionError:
                print(f"  -> Error: Permission denied to delete {img_path}")
        else:
            hashes[img_hash] = img_path

    print(f"\nProcess finished. {duplicates_found} duplicates deleted.")

if __name__ == "__main__":
    # Usage: python remove_duplicates.py /path/to/folder
    if len(sys.argv) < 2:
        print("Usage: python remove_duplicates.py <folder_path>")
        sys.exit(1)
    
    target_folder = sys.argv[1]
    
    if not os.path.isdir(target_folder):
        print(f"Error: '{target_folder}' is not a valid directory.")
        sys.exit(1)

    # Safety confirmation
    confirm = input(f"WARNING: This will permanently delete files in '{target_folder}'. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        find_and_delete_duplicates(target_folder)
    else:
        print("Operation cancelled.")