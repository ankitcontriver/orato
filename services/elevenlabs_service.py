import os
import uuid
from elevenlabs import Voice, VoiceSettings, generate, save, voices
from typing import Dict, List, Optional

class ElevenLabsService:
    def __init__(self):
        self.default_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice ID

    def text_to_speech(self, text: str, voice_name: Optional[str], api_key: str) -> Dict:
        """Convert text to speech using ElevenLabs API"""
        try:
            # Set API key
            os.environ['ELEVEN_API_KEY'] = api_key
            
            # Use provided voice or default
            voice_id = voice_name if voice_name else self.default_voice_id
            
            # Generate unique filename
            filename = f"elevenlabs_tts_{uuid.uuid4().hex}.mp3"
            filepath = os.path.join('downloads', filename)
            
            # Generate audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(
                        stability=0.5,
                        similarity_boost=0.5,
                        style=0.0,
                        use_speaker_boost=True
                    )
                )
            )
            
            # Save audio
            save(audio, filepath)
            
            return {'success': True, 'filename': filename}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_available_voices(self) -> List[Dict]:
        """Get available voices from ElevenLabs"""
        try:
            # This would require API key, so we'll return some popular voice IDs
            popular_voices = [
                {
                    'name': '21m00Tcm4TlvDq8ikWAM',
                    'display_name': 'Rachel (Default)',
                    'language': 'en'
                },
                {
                    'name': 'AZnzlk1XvdvUeBnXmlld',
                    'display_name': 'Domi',
                    'language': 'en'
                },
                {
                    'name': 'EXAVITQu4vr4xnSDxMaL',
                    'display_name': 'Bella',
                    'language': 'en'
                },
                {
                    'name': 'ErXwobaYiN019PkySvjV',
                    'display_name': 'Antoni',
                    'language': 'en'
                },
                {
                    'name': 'MF3mGyEYCl7XYWbV9V6O',
                    'display_name': 'Elli',
                    'language': 'en'
                },
                {
                    'name': 'TxGEqnHWrfWFTfGW9XjX',
                    'display_name': 'Josh',
                    'language': 'en'
                },
                {
                    'name': 'VR6AewLTigWG4xSOukaG',
                    'display_name': 'Arnold',
                    'language': 'en'
                },
                {
                    'name': 'pNInz6obpgDQGcFmaJgB',
                    'display_name': 'Adam',
                    'language': 'en'
                },
                {
                    'name': 'yoZ06aMxZJJ28mfd3POQ',
                    'display_name': 'Sam',
                    'language': 'en'
                }
            ]
            
            return popular_voices
            
        except Exception as e:
            return []

    def get_voice_by_id(self, voice_id: str, api_key: str) -> Optional[Dict]:
        """Get voice details by ID"""
        try:
            os.environ['ELEVEN_API_KEY'] = api_key
            voice = voices.get(voice_id)
            
            return {
                'name': voice.voice_id,
                'display_name': voice.name,
                'language': voice.labels.get('language', 'en'),
                'description': voice.labels.get('description', '')
            }
            
        except Exception as e:
            return None

