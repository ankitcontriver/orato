from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from services.azure_service import AzureService
from services.elevenlabs_service import ElevenLabsService
from services.batch_service import BatchService
from services.file_service import FileService
from utils.config import Config

app = Flask(__name__)
CORS(app)

# Initialize services
azure_service = AzureService()
elevenlabs_service = ElevenLabsService()
batch_service = BatchService()
file_service = FileService()

# Create necessary directories
file_service.create_directories()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        provider = data.get('provider', 'azure')
        language = data.get('language', 'en')
        voice_name = data.get('voice_name')
        api_key = data.get('api_key')
        region = data.get('region', 'eastus')
        
        if not text or not api_key:
            return jsonify({'error': 'Text and API key are required'}), 400
        
        if provider == 'azure':
            result = azure_service.text_to_speech(text, language, voice_name, api_key, region)
        elif provider == 'elevenlabs':
            result = elevenlabs_service.text_to_speech(text, voice_name, api_key)
        else:
            return jsonify({'error': 'Invalid provider'}), 400
        
        if result['success']:
            return jsonify({
                'success': True,
                'filename': result['filename'],
                'download_url': f'/download/{result["filename"]}'
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        provider = request.form.get('provider', 'azure')
        language = request.form.get('language', 'en')
        api_key = request.form.get('api_key')
        region = request.form.get('region', 'eastus')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        # Save uploaded file
        filepath = file_service.save_uploaded_file(file, 'stt')
        
        if provider == 'azure':
            result = azure_service.speech_to_text(filepath, language, api_key, region)
        else:
            return jsonify({'error': 'Only Azure supports STT'}), 400
        
        # Clean up uploaded file
        file_service.cleanup_file(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'text': result['text']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch', methods=['POST'])
def batch_process():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        provider = request.form.get('provider', 'azure')
        language = request.form.get('language', 'en')
        api_key = request.form.get('api_key')
        region = request.form.get('region', 'eastus')
        process_type = request.form.get('type', 'tts')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        result = batch_service.process_batch(file, provider, language, api_key, region, process_type)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voices', methods=['GET'])
def get_voices():
    provider = request.args.get('provider', 'azure')
    language = request.args.get('language', 'en')
    
    if provider == 'azure':
        voices = azure_service.get_available_voices(language)
    elif provider == 'elevenlabs':
        voices = elevenlabs_service.get_available_voices()
    else:
        return jsonify({'error': 'Invalid provider'}), 400
    
    return jsonify({'voices': voices})

@app.route('/download/<filename>')
def download_file(filename):
    filepath = file_service.get_download_path(filename)
    if filepath and os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)