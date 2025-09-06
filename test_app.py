from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import requests
import uuid
import tempfile
import json
import subprocess
import zipfile
import shutil

app = Flask(__name__)
CORS(app)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('downloads', exist_ok=True)

def convert_audio_to_wav(input_path, output_path=None):
    """Convert any audio format to WAV format for Azure STT compatibility using ffmpeg"""
    try:
        # Generate output path if not provided
        if not output_path:
            output_path = input_path.replace('.wav', '_converted.wav')
        
        # Use ffmpeg to convert to WAV format with Azure STT compatible settings
        # Azure STT works best with: 16kHz, 16-bit, mono
        cmd = [
            'ffmpeg', '-i', input_path,
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',      # mono
            '-sample_fmt', 's16',  # 16-bit
            '-y',            # overwrite output file
            output_path
        ]
        
        # Run ffmpeg command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Audio converted successfully: {input_path} -> {output_path}")
            return output_path
        else:
            print(f"FFmpeg conversion error: {result.stderr}")
            # If conversion fails, return original path
            return input_path
        
    except Exception as e:
        print(f"Audio conversion error: {e}")
        # If conversion fails, return original path
        return input_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stt')
def stt():
    return render_template('stt.html')

@app.route('/tts')
def tts():
    return render_template('tts.html')

@app.route('/batch')
def batch():
    return render_template('batch.html')

# Separate pages for each functionality

@app.route('/debug')
def debug():
    return send_file('debug.html')

@app.route('/test-stt')
def test_stt():
    return send_file('test_stt.html')

@app.route('/test-complete')
def test_complete():
    return send_file('test_complete.html')

@app.route('/test-stt-simple')
def test_stt_simple():
    return send_file('test_stt_simple.html')

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        provider = data.get('provider', 'azure')
        language = data.get('language', 'en-US')
        voice_name = data.get('voice_name')
        api_key = data.get('api_key')
        region = data.get('region', 'eastus')
        
        if not text or not api_key:
            return jsonify({'error': 'Text and API key are required'}), 400
        
        # Generate unique filename
        filename = f"tts_{uuid.uuid4().hex}.wav"
        filepath = os.path.join('downloads', filename)
        
        if provider == 'azure':
            result = azure_tts_rest(text, language, voice_name, api_key, region, filepath)
        elif provider == 'elevenlabs':
            result = elevenlabs_tts(text, voice_name, api_key, filepath)
        else:
            return jsonify({'error': 'Invalid provider'}), 400
        
        if result['success']:
            return jsonify({
                'success': True,
                'filename': filename,
                'download_url': f'/download/{filename}'
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def azure_tts_rest(text, language, voice_name, api_key, region, output_path):
    """Use Azure REST API instead of SDK"""
    try:
        url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
        
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm'
        }
        
        # Use provided voice or default
        if not voice_name:
            voice_name = "en-US-AriaNeural"
        
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'>
            <voice name='{voice_name}'>
                {text}
            </voice>
        </speak>
        """
        
        response = requests.post(url, headers=headers, data=ssml)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return {'success': True}
        else:
            return {'success': False, 'error': f'Azure API error: {response.status_code} - {response.text}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def elevenlabs_tts(text, voice_name, api_key, output_path):
    """ElevenLabs TTS using REST API"""
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech"
        
        if not voice_name:
            voice_name = "21m00Tcm4TlvDq8ikWAM"  # Default voice
        
        headers = {
            'Accept': 'audio/wav',
            'Content-Type': 'application/json',
            'xi-api-key': api_key
        }
        
        data = {
            'text': text,
            'model_id': 'eleven_monolingual_v1',
            'voice_settings': {
                'stability': 0.5,
                'similarity_boost': 0.5
            }
        }
        
        response = requests.post(f"{url}/{voice_name}", json=data, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return {'success': True}
        else:
            return {'success': False, 'error': f'ElevenLabs API error: {response.status_code} - {response.text}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        language = request.form.get('language', 'en-US')
        api_key = request.form.get('api_key')
        region = request.form.get('region', 'eastus')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        # Save uploaded file
        filename = f"stt_{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Validate the file was saved properly
        if not os.path.exists(filepath):
            return jsonify({'error': 'Failed to save audio file'}), 500
            
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            return jsonify({'error': 'Audio file is empty'}), 400
            
        print(f"Processing audio file: {filename}, size: {file_size} bytes")
        
        # Use Azure REST API for STT
        result = azure_stt_rest(filepath, language, api_key, region)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'text': result['text']
            })
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def azure_stt_rest(audio_path, language, api_key, region):
    """Use Azure REST API for Speech to Text"""
    try:
        # Convert audio to WAV format for Azure STT compatibility
        converted_audio_path = convert_audio_to_wav(audio_path)
        
        url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1"
        
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Accept': 'application/json'
        }
        
        params = {
            'language': language,
            'format': 'detailed'
        }
        
        # Read the converted audio file as binary
        with open(converted_audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            
        print(f"Audio data size: {len(audio_data)} bytes")
        print(f"Using converted audio file: {converted_audio_path}")
        
        # Check for potential encoding issues in the first 1000 bytes
        try:
            sample_data = audio_data[:1000]
            sample_data.decode('utf-8')
            print("Audio data appears to be valid binary")
        except UnicodeDecodeError as e:
            print(f"Potential encoding issue in audio data: {e}")
            # Try to clean the data - replace ellipsis character with dots
            audio_data = audio_data.replace(b'\xe2\x80\xa6', b'...')  # UTF-8 encoded ellipsis
        
        # Make the request with the binary data
        try:
            response = requests.post(url, headers=headers, params=params, data=audio_data)
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error: {e}")
            return {'success': False, 'error': f"Audio file encoding error: {str(e)}"}
        except Exception as e:
            print(f"Request error: {e}")
            return {'success': False, 'error': f"Request failed: {str(e)}"}
        
        print(f"Azure STT response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Azure STT result: {result}")
            if result.get('RecognitionStatus') == 'Success':
                return {'success': True, 'text': result.get('DisplayText', '')}
            else:
                return {'success': False, 'error': f'Recognition failed: {result.get("RecognitionStatus")}'}
        else:
            print(f"Azure STT error response: {response.text}")
            return {'success': False, 'error': f'Azure API error: {response.status_code} - {response.text}'}
            
    except Exception as e:
        print(f"Azure STT exception: {e}")
        return {'success': False, 'error': str(e)}

@app.route('/api/batch', methods=['POST'])
def batch_processing():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        batch_type = request.form.get('batch_type', 'tts')
        language = request.form.get('language', 'en-US')
        voice = request.form.get('voice', 'en-US-AvaNeural')
        elevenlabs_voice = request.form.get('elevenlabs_voice', '')
        provider = request.form.get('provider', 'azure')
        api_key = request.form.get('api_key')
        region = request.form.get('region', 'eastus')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        # Save uploaded file
        filename = f"batch_{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        print(f"Processing batch file: {filename}, type: {batch_type}, provider: {provider}")
        
        if batch_type == 'tts':
            result = process_tts_batch(filepath, language, voice, elevenlabs_voice, provider, api_key, region)
        else:
            result = process_stt_batch(filepath, language, provider, api_key, region)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if result['success']:
            return jsonify({
                'success': True,
                'processed_count': result.get('processed_count', 0),
                'download_url': result.get('download_url'),
                'message': result.get('message', 'Batch processing completed successfully')
            })
        else:
            return jsonify({'error': result.get('error', 'Batch processing failed')}), 500
            
    except Exception as e:
        print(f"Batch processing error: {e}")
        return jsonify({'error': str(e)}), 500

def process_tts_batch(filepath, language, voice, elevenlabs_voice, provider, api_key, region):
    """Process TTS batch from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return {'success': False, 'error': 'JSON file must contain an array of objects'}
        
        results = []
        processed_count = 0
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                continue
                
            for filename, text in item.items():
                try:
                    # Generate TTS for this text
                    output_filename = f"batch_tts_{i}_{filename.replace('.wav', '')}.wav"
                    output_path = os.path.join('downloads', output_filename)
                    
                    if provider == 'azure':
                        tts_result = azure_tts_rest(text, language, voice, api_key, region, output_path)
                    else:  # elevenlabs
                        tts_result = elevenlabs_tts(text, elevenlabs_voice, api_key, output_path)
                    
                    if tts_result['success']:
                        results.append({
                            'original_file': filename,
                            'generated_file': output_filename,
                            'text': text,
                            'status': 'success'
                        })
                        processed_count += 1
                    else:
                        results.append({
                            'original_file': filename,
                            'text': text,
                            'status': 'failed',
                            'error': tts_result.get('error', 'Unknown error')
                        })
                        
                except Exception as e:
                    results.append({
                        'original_file': filename,
                        'text': text,
                        'status': 'failed',
                        'error': str(e)
                    })
        
        # Create a ZIP file with results and generated audio files
        zip_filename = f"batch_results_{uuid.uuid4().hex}.zip"
        zip_path = os.path.join('downloads', zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add results JSON file
            results_json = json.dumps(results, indent=2)
            zipf.writestr('results.json', results_json)
            
            # Add generated audio files
            for result in results:
                if result.get('status') == 'success' and 'generated_file' in result:
                    audio_file_path = os.path.join('downloads', result['generated_file'])
                    if os.path.exists(audio_file_path):
                        zipf.write(audio_file_path, result['generated_file'])
        
        return {
            'success': True,
            'processed_count': processed_count,
            'download_url': f'/download/{zip_filename}',
            'message': f'Processed {processed_count} files successfully. Download includes results.json and generated audio files.'
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_stt_batch(filepath, language, provider, api_key, region):
    """Process STT batch from audio files"""
    try:
        # For STT batch, we expect a zip file with audio files
        import zipfile
        import tempfile
        
        results = []
        processed_count = 0
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Process each audio file
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.wav', '.mp3', '.m4a', '.flac')):
                        try:
                            audio_path = os.path.join(root, file)
                            
                            if provider == 'azure':
                                stt_result = azure_stt_rest(audio_path, language, api_key, region)
                            else:  # elevenlabs - use Azure STT for now since ElevenLabs doesn't have STT
                                stt_result = azure_stt_rest(audio_path, language, api_key, region)
                            
                            if stt_result['success']:
                                results.append({
                                    'original_file': file,
                                    'text': stt_result['text'],
                                    'status': 'success'
                                })
                                processed_count += 1
                            else:
                                results.append({
                                    'original_file': file,
                                    'status': 'failed',
                                    'error': stt_result.get('error', 'Unknown error')
                                })
                                
                        except Exception as e:
                            results.append({
                                'original_file': file,
                                'status': 'failed',
                                'error': str(e)
                            })
        
        # Create a ZIP file with results
        zip_filename = f"batch_stt_results_{uuid.uuid4().hex}.zip"
        zip_path = os.path.join('downloads', zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add results JSON file
            results_json = json.dumps(results, indent=2)
            zipf.writestr('results.json', results_json)
        
        return {
            'success': True,
            'processed_count': processed_count,
            'download_url': f'/download/{zip_filename}',
            'message': f'Processed {processed_count} audio files successfully. Download includes results.json with transcriptions.'
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join('downloads', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
