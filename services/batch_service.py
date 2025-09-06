import json
import os
from typing import Dict, List
from services.azure_service import AzureService
from services.elevenlabs_service import ElevenLabsService
from services.file_service import FileService

class BatchService:
    def __init__(self):
        self.azure_service = AzureService()
        self.elevenlabs_service = ElevenLabsService()
        self.file_service = FileService()

    def process_batch(self, file, provider: str, language: str, api_key: str, 
                     region: str, process_type: str) -> Dict:
        """Process batch file for TTS or STT"""
        try:
            # Read and parse JSON file
            content = file.read().decode('utf-8')
            data = json.loads(content)
            
            if not isinstance(data, dict):
                return {'success': False, 'error': 'Invalid JSON format. Expected object with key-value pairs.'}
            
            results = []
            errors = []
            
            for key, value in data.items():
                try:
                    if process_type == 'tts':
                        result = self._process_tts_batch_item(key, value, provider, language, api_key, region)
                    else:
                        result = self._process_stt_batch_item(key, value, provider, language, api_key, region)
                    
                    if result['success']:
                        results.append(result)
                    else:
                        errors.append({'key': key, 'error': result['error']})
                        
                except Exception as e:
                    errors.append({'key': key, 'error': str(e)})
            
            return {
                'success': True,
                'results': results,
                'errors': errors,
                'total_processed': len(results),
                'total_errors': len(errors)
            }
            
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f'Invalid JSON format: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _process_tts_batch_item(self, key: str, text: str, provider: str, 
                               language: str, api_key: str, region: str) -> Dict:
        """Process a single TTS batch item"""
        try:
            if provider == 'azure':
                result = self.azure_service.text_to_speech(text, language, None, api_key, region)
            elif provider == 'elevenlabs':
                result = self.elevenlabs_service.text_to_speech(text, None, api_key)
            else:
                return {'success': False, 'error': 'Invalid provider'}
            
            if result['success']:
                return {
                    'success': True,
                    'original_key': key,
                    'text': text,
                    'filename': result['filename'],
                    'download_url': f'/download/{result["filename"]}'
                }
            else:
                return {'success': False, 'error': result['error']}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _process_stt_batch_item(self, key: str, audio_path: str, provider: str, 
                               language: str, api_key: str, region: str) -> Dict:
        """Process a single STT batch item"""
        try:
            # For STT batch processing, we would need the actual audio files
            # This is a placeholder implementation
            return {
                'success': False,
                'error': 'STT batch processing requires audio files. Please use individual STT processing.'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_batch_template(self, process_type: str) -> Dict:
        """Create a template for batch processing"""
        if process_type == 'tts':
            template = {
                "1.wav": "Hello, this is a sample text for TTS conversion.",
                "2.wav": "This is another sample text in a different language.",
                "3.wav": "You can add as many entries as you want."
            }
        else:
            template = {
                "audio1.wav": "path/to/audio1.wav",
                "audio2.wav": "path/to/audio2.wav",
                "audio3.wav": "path/to/audio3.wav"
            }
        
        return {
            'success': True,
            'template': template,
            'instructions': f'For {process_type.upper()}: Replace the values with your {process_type} data'
        }

