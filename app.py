from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os
import noisereduce as nr
import librosa
import soundfile as sf

app = Flask(__name__, static_folder='static')
CORS(app)  # Enables CORS

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/upload', methods=['POST'])
def upload_and_process():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    uploaded_file = request.files['audio_file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded audio file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(file_path)

    # Load the audio file
    audio, sample_rate = librosa.load(file_path, sr=None)

    # Perform noise reduction with adjusted parameters for softer reduction
    reduced_noise = nr.reduce_noise(y=audio, sr=sample_rate, n_std_thresh_stationary=1.5, n_std_thresh=1.5)

    # Save the processed audio file
    processed_filename = f'processed_{uploaded_file.filename}'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    sf.write(output_path, reduced_noise, sample_rate)

    # Return success message including the path for download
    return jsonify({
        'message': 'Noise reduction complete!',
        'processed_file': processed_filename
    })

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
