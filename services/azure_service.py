import azure.cognitiveservices.speech as speechsdk
import os
import uuid
from typing import Dict, List, Optional

class AzureService:
    def __init__(self):
        self.languages = {
            'en': 'en-US',
            'ar': 'ar-SA',
            'hi': 'hi-IN',
            'fr': 'fr-FR',
            'ps': 'ps-AF',  # Pashto
            'prs': 'prs-AF',  # Dari
            'es': 'es-ES',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-BR',
            'ru': 'ru-RU',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'zh': 'zh-CN'
        }
        
        self.voices = {
            'en': 'en-US-AriaNeural',
            'ar': 'ar-SA-ZariyahNeural',
            'hi': 'hi-IN-SwaraNeural',
            'fr': 'fr-FR-DeniseNeural',
            'es': 'es-ES-ElviraNeural',
            'de': 'de-DE-KatjaNeural',
            'it': 'it-IT-ElsaNeural',
            'pt': 'pt-BR-FranciscaNeural',
            'ru': 'ru-RU-SvetlanaNeural',
            'ja': 'ja-JP-NanamiNeural',
            'ko': 'ko-KR-SunHiNeural',
            'zh': 'zh-CN-XiaoxiaoNeural'
        }

    def text_to_speech(self, text: str, language: str, voice_name: Optional[str], 
                      api_key: str, region: str) -> Dict:
        """Convert text to speech using Azure Cognitive Services"""
        try:
            # Configure Azure Speech
            speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
            
            # Set language
            speech_config.speech_synthesis_language = self.languages.get(language, 'en-US')
            
            # Set voice
            if voice_name:
                speech_config.speech_synthesis_voice_name = voice_name
            else:
                speech_config.speech_synthesis_voice_name = self.voices.get(language, 'en-US-AriaNeural')
            
            # Generate unique filename
            filename = f"azure_tts_{uuid.uuid4().hex}.wav"
            filepath = os.path.join('downloads', filename)
            
            # Configure audio output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            
            # Synthesize
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return {'success': True, 'filename': filename}
            else:
                return {'success': False, 'error': f'Synthesis failed: {result.reason}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def speech_to_text(self, audio_path: str, language: str, api_key: str, region: str) -> Dict:
        """Convert speech to text using Azure Cognitive Services"""
        try:
            # Configure Azure Speech
            speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
            speech_config.speech_recognition_language = self.languages.get(language, 'en-US')
            
            # Configure audio input
            audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
            
            # Create recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            
            # Recognize
            result = speech_recognizer.recognize_once_async().get()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {'success': True, 'text': result.text}
            else:
                return {'success': False, 'error': f'Recognition failed: {result.reason}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_available_voices(self, language: str) -> List[Dict]:
        """Get available voices for a specific language"""
        voices = []
        lang_code = self.languages.get(language, 'en-US')
        
        # Add default voice for the language
        if language in self.voices:
            voices.append({
                'name': self.voices[language],
                'display_name': f"Default {language.upper()} Voice",
                'language': lang_code
            })
        
        # Add some additional popular voices
        additional_voices = {
            'en': ['en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-DavisNeural'],
            'ar': ['ar-SA-HamedNeural', 'ar-SA-SalmaNeural'],
            'hi': ['hi-IN-MadhurNeural', 'hi-IN-PrabhatNeural'],
            'fr': ['fr-FR-HenriNeural', 'fr-FR-CelesteNeural'],
            'es': ['es-ES-AlvaroNeural', 'es-ES-LiaNeural'],
            'de': ['de-DE-ConradNeural', 'de-DE-KatjaNeural'],
            'it': ['it-IT-DiegoNeural', 'it-IT-ElsaNeural'],
            'pt': ['pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural'],
            'ru': ['ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural'],
            'ja': ['ja-JP-KeitaNeural', 'ja-JP-NanamiNeural'],
            'ko': ['ko-KR-InJoonNeural', 'ko-KR-SunHiNeural'],
            'zh': ['zh-CN-YunxiNeural', 'zh-CN-XiaoxiaoNeural']
        }
        
        if language in additional_voices:
            for voice in additional_voices[language]:
                voices.append({
                    'name': voice,
                    'display_name': voice.replace('-', ' ').replace('Neural', ''),
                    'language': lang_code
                })
        
        return voices

