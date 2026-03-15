import os
import shutil
from flask import Flask, request, jsonify, send_file
import random

app = Flask(__name__)

#princess = 'rapunzel' 
#princess = 'snow_white' 
princess = 'aurora' 

# CONFIGURATION
SOURCE_FOLDER =  princess # Change to your current folder
KEEP_FOLDER = princess + '/selected'
REJECT_FOLDER = princess + '/rejected'
TARGET_COUNT = 200

# Ensure folders exist
for folder in [KEEP_FOLDER, REJECT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_image_list():
    """Get list of remaining images in source."""
    if not os.path.exists(SOURCE_FOLDER):
        return []
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('.')]
    return files

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/image')
def get_image():
    files = get_image_list()
    if not files:
        return jsonify({'status': 'done', 'message': 'No more images!'})
    
    # Pick a random image to avoid bias from order
    filename = random.choice(files)
    return jsonify({'status': 'ok', 'filename': filename, 'count_remaining': len(files)})

@app.route('/action', methods=['POST'])
def action():
    data = request.json
    filename = data.get('filename')
    decision = data.get('decision') # 'keep' or 'skip'
    
    src = os.path.join(SOURCE_FOLDER, filename)
    
    if not os.path.exists(src):
        return jsonify({'error': 'File not found'}), 404

    if decision == 'keep':
        dst = os.path.join(KEEP_FOLDER, filename)
        # Optional: Rename to ensure uniqueness if needed, but keeping name is usually fine
        shutil.move(src, dst)
    elif decision == 'skip':
        dst = os.path.join(REJECT_FOLDER, filename)
        shutil.move(src, dst)
        
    return jsonify({'status': 'success'})

@app.route('/serve_image')
def serve_image():
    filename = request.args.get('filename')
    path = os.path.join(SOURCE_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path)
    return "Image not found", 404

if __name__ == '__main__':
    print(f"--- SORTER STARTED ---")
    print(f"Source: {SOURCE_FOLDER}")
    print(f"Target Keep: {KEEP_FOLDER} (Max {TARGET_COUNT})")
    print("Open the 'Forwarded Address' in your browser to start sorting.")
    app.run(host='0.0.0.0', port=5000)