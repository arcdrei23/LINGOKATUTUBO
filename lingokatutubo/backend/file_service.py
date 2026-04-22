"""
File service for handling uploaded documents
"""

import os
import tempfile
import uuid
from pathlib import Path
from typing import Optional, Tuple
from models import FileType


class FileService:
    """Manages file uploads, temporary storage, and cleanup"""
    
    def __init__(self, upload_dir: Optional[str] = None):
        """
        Initialize file service
        
        Args:
            upload_dir: Directory for temporary uploads. Defaults to /tmp/bagobo-uploads/
        """
        self.upload_dir = upload_dir or os.path.join(tempfile.gettempdir(), "bagobo-uploads")
        self.jobs_dir = os.path.join(self.upload_dir, "jobs")
        
        # Create directories
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.jobs_dir, exist_ok=True)
    
    async def save_upload(self, file_content: bytes, original_filename: str, job_id: str) -> str:
        """
        Save uploaded file with job ID
        
        Args:
            file_content: The file bytes
            original_filename: Original filename from upload
            job_id: Unique job identifier
        
        Returns:
            Path to saved file
        """
        job_dir = os.path.join(self.jobs_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # Sanitize filename and save
        safe_name = Path(original_filename).stem + Path(original_filename).suffix
        file_path = os.path.join(job_dir, f"input_{safe_name}")
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return file_path
    
    def get_job_dir(self, job_id: str) -> str:
        """Get the working directory for a job"""
        return os.path.join(self.jobs_dir, job_id)
    
    def get_output_path(self, job_id: str, filename: str) -> str:
        """Get path for output file in job directory"""
        job_dir = self.get_job_dir(job_id)
        os.makedirs(job_dir, exist_ok=True)
        return os.path.join(job_dir, filename)
    
    def cleanup_job(self, job_id: str):
        """Remove all files for a job (optional - call after download)"""
        job_dir = self.get_job_dir(job_id)
        if os.path.exists(job_dir):
            import shutil
            shutil.rmtree(job_dir)
    
    @staticmethod
    def get_file_type(filename: str) -> Optional[FileType]:
        """Detect file type from extension"""
        ext = Path(filename).suffix.lower()
        ext_map = {
            '.pdf': FileType.PDF,
            '.docx': FileType.DOCX,
            '.jpg': FileType.JPG,
            '.jpeg': FileType.JPG,
            '.png': FileType.PNG,
        }
        return ext_map.get(ext)
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        if self.file_exists(file_path):
            return os.path.getsize(file_path)
        return 0


# Global instance
_file_service = None


def get_file_service() -> FileService:
    """Get or create the global file service instance"""
    global _file_service
    if _file_service is None:
        _file_service = FileService()
    return _file_service

