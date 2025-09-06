import os
from typing import Dict, List

class Config:
    """Configuration class for Orato application"""
    
    # Supported languages
    LANGUAGES = {
        'en': {'name': 'English', 'code': 'en-US'},
        'ar': {'name': 'Arabic', 'code': 'ar-SA'},
        'hi': {'name': 'Hindi', 'code': 'hi-IN'},
        'fr': {'name': 'French', 'code': 'fr-FR'},
        'ps': {'name': 'Pashto', 'code': 'ps-AF'},
        'prs': {'name': 'Dari', 'code': 'prs-AF'},
        'es': {'name': 'Spanish', 'code': 'es-ES'},
        'de': {'name': 'German', 'code': 'de-DE'},
        'it': {'name': 'Italian', 'code': 'it-IT'},
        'pt': {'name': 'Portuguese', 'code': 'pt-BR'},
        'ru': {'name': 'Russian', 'code': 'ru-RU'},
        'ja': {'name': 'Japanese', 'code': 'ja-JP'},
        'ko': {'name': 'Korean', 'code': 'ko-KR'},
        'zh': {'name': 'Chinese', 'code': 'zh-CN'}
    }
    
    # Azure regions
    AZURE_REGIONS = [
        'eastus', 'eastus2', 'southcentralus', 'westus2', 'westus3',
        'australiaeast', 'southeastasia', 'northeurope', 'swedencentral',
        'uksouth', 'westeurope', 'centralus', 'southafricanorth',
        'centralindia', 'eastasia', 'japaneast', 'japanwest',
        'koreacentral', 'canadacentral', 'francecentral', 'germanywestcentral',
        'italynorth', 'norwayeast', 'polandcentral', 'switzerlandnorth',
        'uaenorth', 'brazilsouth', 'centralusstage', 'eastusstage',
        'eastus2stage', 'northcentralusstage', 'southcentralusstage',
        'westusstage', 'westus2stage', 'asia', 'asiapacific', 'australia',
        'brazil', 'canada', 'europe', 'global', 'india', 'japan', 'uk'
    ]
    
    # File upload settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'm4a', 'ogg', 'flac', 'json'}
    
    # Application settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    @classmethod
    def get_language_name(cls, code: str) -> str:
        """Get language name by code"""
        return cls.LANGUAGES.get(code, {}).get('name', 'Unknown')
    
    @classmethod
    def get_language_code(cls, code: str) -> str:
        """Get Azure language code by language code"""
        return cls.LANGUAGES.get(code, {}).get('code', 'en-US')
    
    @classmethod
    def get_supported_languages(cls) -> List[Dict]:
        """Get list of supported languages"""
        return [
            {'code': code, 'name': info['name'], 'azure_code': info['code']}
            for code, info in cls.LANGUAGES.items()
        ]

