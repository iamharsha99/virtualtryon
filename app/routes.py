from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from video_processing import load_shirt_images, stream_video_feed

bp = Blueprint('routes', __name__)

# Load shirt images
shirt_images = load_shirt_images()

@bp.route('/', methods=['GET', 'POST'])
def index():
    global shirt_images
    shirt_files = [os.path.basename(img) for img in os.listdir('static/uploads') if img.endswith('.png')]
    
    # Retrieve and validate selected shirt index from session
    selected_shirt_index = session.get('shirt_index', 0)
    if selected_shirt_index < 0 or selected_shirt_index >= len(shirt_files):
        selected_shirt_index = 0

    # Get the selected shirt based on the validated index
    selected_shirt = shirt_files[selected_shirt_index] if shirt_files else None

    if request.method == 'POST':
        shirt_index = request.form.get('shirt')
        if shirt_index.isdigit():
            shirt_index = int(shirt_index)
            if 0 <= shirt_index < len(shirt_files):
                session['shirt_index'] = shirt_index
            else:
                session['shirt_index'] = 0  # Default to 0 if out of range
        return redirect(url_for('routes.index'))

    return render_template('index.html', shirts=shirt_files, selected_shirt_index=selected_shirt_index)

@bp.route('/upload_shirt', methods=['POST'])
def upload_shirt():
    global shirt_images
    file = request.files.get('file')
    if file and file.filename.endswith('.png'):
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)
        # Reload shirt images
        shirt_images = load_shirt_images()
    return redirect(url_for('routes.index'))

@bp.route('/stream_video_feed')
def stream_video_feed_route():
    shirt_index = request.args.get('shirt_index', default=0, type=int)
    return stream_video_feed(shirt_index)
