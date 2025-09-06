import os
import uuid
from werkzeug.utils import secure_filename
from typing import Optional

class FileService:
    def __init__(self):
        self.upload_dir = 'uploads'
        self.download_dir = 'downloads'
        self.allowed_extensions = {'wav', 'mp3', 'mp4', 'm4a', 'ogg', 'flac'}

    def create_directories(self):
        """Create necessary directories"""
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.download_dir, exist_ok=True)
        os.makedirs('static', exist_ok=True)
        os.makedirs('templates', exist_ok=True)

    def save_uploaded_file(self, file, prefix: str = 'file') -> str:
        """Save uploaded file and return filepath"""
        filename = secure_filename(file.filename)
        unique_filename = f"{prefix}_{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(self.upload_dir, unique_filename)
        file.save(filepath)
        return filepath

    def get_download_path(self, filename: str) -> Optional[str]:
        """Get full path for download file"""
        filepath = os.path.join(self.download_dir, filename)
        if os.path.exists(filepath):
            return filepath
        return None

    def cleanup_file(self, filepath: str):
        """Clean up temporary file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error cleaning up file {filepath}: {e}")

    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(filepath)
        except Exception:
            return 0

    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up files older than specified hours"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for directory in [self.upload_dir, self.download_dir]:
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > max_age_seconds:
                            os.remove(filepath)
            except Exception as e:
                print(f"Error cleaning up directory {directory}: {e}")

