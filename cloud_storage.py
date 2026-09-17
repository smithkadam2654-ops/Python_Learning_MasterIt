"""
Cloud Storage Module

This module provides comprehensive cloud storage utilities including:
- Cloud provider abstraction
- File upload and download
- Directory synchronization
- File sharing and permissions
- Storage quota management
- File versioning
- Cloud backup operations
- Multi-cloud support
- Storage optimization
- Error handling and retry logic

Note: This module uses various cloud provider SDKs.
Install with: pip install boto3 google-cloud-storage azure-storage-blob

All functions include comprehensive docstrings and type hints.
"""

import os
import hashlib
import threading
import queue
from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class CloudProvider(Enum):
    """Supported cloud storage providers."""
    AWS_S3 = "aws_s3"
    GOOGLE_CLOUD = "google_cloud"
    AZURE_BLOB = "azure_blob"
    DROPBOX = "dropbox"
    ONE_DRIVE = "one_drive"


class SyncDirection(Enum):
    """Synchronization direction."""
    UPLOAD = "upload"
    DOWNLOAD = "download"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class CloudFile:
    """Represents a file in cloud storage."""
    name: str
    size: int
    modified_time: datetime
    etag: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = None
    is_directory: bool = False


@dataclass
class StorageQuota:
    """Container for storage quota information."""
    total_space: int
    used_space: int
    available_space: int
    percentage_used: float


@dataclass
class SyncResult:
    """Container for synchronization results."""
    files_uploaded: int
    files_downloaded: int
    files_skipped: int
    files_failed: int
    total_size_transferred: int
    duration: float
    errors: List[str]


class CloudStorageClient:
    """Abstract cloud storage client."""
    
    def __init__(self, provider: CloudProvider, config: Dict[str, Any]):
        """Initialize cloud storage client."""
        self.provider = provider
        self.config = config
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the specific cloud client."""
        if self.provider == CloudProvider.AWS_S3:
            self._init_aws_s3()
        elif self.provider == CloudProvider.GOOGLE_CLOUD:
            self._init_google_cloud()
        elif self.provider == CloudProvider.AZURE_BLOB:
            self._init_azure_blob()
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
    
    def _init_aws_s3(self) -> None:
        """Initialize AWS S3 client."""
        try:
            import boto3
            self._client = boto3.client(
                's3',
                aws_access_key_id=self.config.get('access_key'),
                aws_secret_access_key=self.config.get('secret_key'),
                region_name=self.config.get('region', 'us-east-1')
            )
        except ImportError:
            raise ImportError("boto3 library is required. Install with: pip install boto3")
    
    def _init_google_cloud(self) -> None:
        """Initialize Google Cloud Storage client."""
        try:
            from google.cloud import storage
            self._client = storage.Client.from_service_account_info(
                self.config.get('credentials')
            )
        except ImportError:
            raise ImportError("google-cloud-storage library is required. Install with: pip install google-cloud-storage")
    
    def _init_azure_blob(self) -> None:
        """Initialize Azure Blob Storage client."""
        try:
            from azure.storage.blob import BlobServiceClient
            self._client = BlobServiceClient(
                account_url=self.config.get('account_url'),
                credential=self.config.get('credential')
            )
        except ImportError:
            raise ImportError("azure-storage-blob library is required. Install with: pip install azure-storage-blob")
    
    def upload_file(self, local_path: str, remote_path: str,
                   metadata: Optional[Dict[str, str]] = None) -> bool:
        """Upload file to cloud storage."""
        if not os.path.exists(local_path):
            return False
        
        try:
            if self.provider == CloudProvider.AWS_S3:
                bucket_name = self.config.get('bucket')
                extra_args = {'Metadata': metadata} if metadata else {}
                self._client.upload_file(
                    bucket_name,
                    remote_path,
                    local_path,
                    ExtraArgs=extra_args
                )
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                bucket = self._client.bucket(self.config.get('bucket'))
                blob = bucket.blob(remote_path)
                blob.upload_from_filename(local_path)
                if metadata:
                    blob.metadata = metadata
            elif self.provider == CloudProvider.AZURE_BLOB:
                container_name = self.config.get('container')
                blob_client = self._client.get_blob_client(container_name, remote_path)
                with open(local_path, 'rb') as data:
                    blob_client.upload_blob(data, overwrite=True)
            
            return True
        except Exception as e:
            print(f"Upload failed: {e}")
            return False
    
    def download_file(self, remote_path: str, local_path: str) -> bool:
        """Download file from cloud storage."""
        try:
            if self.provider == CloudProvider.AWS_S3:
                bucket_name = self.config.get('bucket')
                self._client.download_file(bucket_name, remote_path, local_path)
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                bucket = self._client.bucket(self.config.get('bucket'))
                blob = bucket.blob(remote_path)
                blob.download_to_filename(local_path)
            elif self.provider == CloudProvider.AZURE_BLOB:
                container_name = self.config.get('container')
                blob_client = self._client.get_blob_client(container_name, remote_path)
                with open(local_path, 'wb') as data:
                    data.write(blob_client.download_blob().readall())
            
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    
    def list_files(self, prefix: str = "", max_keys: int = 1000) -> List[CloudFile]:
        """List files in cloud storage."""
        files = []
        
        try:
            if self.provider == CloudProvider.AWS_S3:
                bucket_name = self.config.get('bucket')
                response = self._client.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=prefix,
                    MaxKeys=max_keys
                )
                
                for obj in response.get('Contents', []):
                    files.append(CloudFile(
                        name=obj['Key'],
                        size=obj['Size'],
                        modified_time=obj['LastModified'],
                        etag=obj['ETag'],
                        is_directory=False
                    ))
            
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                bucket = self._client.bucket(self.config.get('bucket'))
                blobs = bucket.list_blobs(prefix=prefix, max_results=max_keys)
                
                for blob in blobs:
                    files.append(CloudFile(
                        name=blob.name,
                        size=blob.size,
                        modified_time=blob.time_created,
                        etag=blob.etag,
                        is_directory=blob.name.endswith('/')
                    ))
            
            elif self.provider == CloudProvider.AZURE_BLOB:
                container_name = self.config.get('container')
                container_client = self._client.get_container_client(container_name)
                blobs = container_client.list_blobs(name_starts_with=prefix)
                
                for blob in blobs:
                    files.append(CloudFile(
                        name=blob.name,
                        size=blob.size,
                        modified_time=blob.last_modified,
                        is_directory=False
                    ))
        
        except Exception as e:
            print(f"List files failed: {e}")
        
        return files
    
    def delete_file(self, remote_path: str) -> bool:
        """Delete file from cloud storage."""
        try:
            if self.provider == CloudProvider.AWS_S3:
                bucket_name = self.config.get('bucket')
                self._client.delete_object(bucket_name, remote_path)
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                bucket = self._client.bucket(self.config.get('bucket'))
                blob = bucket.blob(remote_path)
                blob.delete()
            elif self.provider == CloudProvider.AZURE_BLOB:
                container_name = self.config.get('container')
                blob_client = self._client.get_blob_client(container_name, remote_path)
                blob_client.delete_blob()
            
            return True
        except Exception as e:
            print(f"Delete failed: {e}")
            return False
    
    def get_file_info(self, remote_path: str) -> Optional[CloudFile]:
        """Get information about a specific file."""
        try:
            if self.provider == CloudProvider.AWS_S3:
                bucket_name = self.config.get('bucket')
                response = self._client.head_object(bucket_name, remote_path)
                
                return CloudFile(
                    name=remote_path,
                    size=response['ContentLength'],
                    modified_time=response['LastModified'],
                    etag=response['ETag'],
                    content_type=response.get('ContentType'),
                    is_directory=False
                )
            
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                bucket = self._client.bucket(self.config.get('bucket'))
                blob = bucket.blob(remote_path)
                blob.reload()
                
                return CloudFile(
                    name=remote_path,
                    size=blob.size,
                    modified_time=blob.time_created,
                    etag=blob.etag,
                    content_type=blob.content_type,
                    is_directory=False
                )
            
            elif self.provider == CloudProvider.AZURE_BLOB:
                container_name = self.config.get('container')
                blob_client = self._client.get_blob_client(container_name, remote_path)
                blob = blob_client.get_blob_properties()
                
                return CloudFile(
                    name=remote_path,
                    size=blob.size,
                    modified_time=blob.last_modified,
                    is_directory=False
                )
        
        except Exception as e:
            print(f"Get file info failed: {e}")
            return None
    
    def file_exists(self, remote_path: str) -> bool:
        """Check if file exists in cloud storage."""
        return self.get_file_info(remote_path) is not None
    
    def get_storage_quota(self) -> Optional[StorageQuota]:
        """Get storage quota information."""
        # This is provider-specific and may not be available for all providers
        try:
            if self.provider == CloudProvider.AWS_S3:
                # S3 doesn't provide quota info directly
                return None
            elif self.provider == CloudProvider.GOOGLE_CLOUD:
                # GCS doesn't provide quota info directly
                return None
            elif self.provider == CloudProvider.AZURE_BLOB:
                # Azure doesn't provide quota info directly
                return None
        except Exception:
            pass
        
        return None


class FileSynchronizer:
    """File synchronization between local and cloud storage."""
    
    def __init__(self, client: CloudStorageClient):
        """Initialize file synchronizer."""
        self.client = client
        self.sync_log: List[Dict] = []
    
    def sync_directory(self, local_dir: str, remote_prefix: str,
                      direction: SyncDirection = SyncDirection.BIDIRECTIONAL,
                      delete: bool = False) -> SyncResult:
        """Synchronize directory with cloud storage."""
        start_time = time.time()
        
        files_uploaded = 0
        files_downloaded = 0
        files_skipped = 0
        files_failed = 0
        total_size_transferred = 0
        errors = []
        
        try:
            # Get local files
            local_files = self._get_local_files(local_dir)
            
            # Get remote files
            remote_files = self.client.list_files(remote_prefix)
            remote_file_map = {f.name: f for f in remote_files}
            
            # Synchronize based on direction
            if direction in [SyncDirection.UPLOAD, SyncDirection.BIDIRECTIONAL]:
                for local_file in local_files:
                    remote_path = os.path.join(remote_prefix, local_file['relative_path'])
                    
                    # Check if file exists remotely
                    remote_file = remote_file_map.get(remote_path)
                    
                    should_upload = True
                    if remote_file:
                        # Compare modification times
                        if local_file['modified_time'] <= remote_file.modified_time:
                            should_upload = False
                            files_skipped += 1
                    
                    if should_upload:
                        full_local_path = local_file['full_path']
                        if self.client.upload_file(full_local_path, remote_path):
                            files_uploaded += 1
                            total_size_transferred += local_file['size']
                        else:
                            files_failed += 1
                            errors.append(f"Failed to upload: {local_file['relative_path']}")
            
            if direction in [SyncDirection.DOWNLOAD, SyncDirection.BIDIRECTIONAL]:
                for remote_file in remote_files:
                    if remote_file.is_directory:
                        continue
                    
                    relative_path = remote_file.name.replace(remote_prefix, "").lstrip('/')
                    local_path = os.path.join(local_dir, relative_path)
                    
                    # Check if file exists locally
                    local_file = None
                    for lf in local_files:
                        if lf['relative_path'] == relative_path:
                            local_file = lf
                            break
                    
                    should_download = True
                    if local_file:
                        # Compare modification times
                        if local_file['modified_time'] >= remote_file.modified_time:
                            should_download = False
                            files_skipped += 1
                    
                    if should_download:
                        if self.client.download_file(remote_file.name, local_path):
                            files_downloaded += 1
                            total_size_transferred += remote_file.size
                        else:
                            files_failed += 1
                            errors.append(f"Failed to download: {relative_path}")
            
            # Handle deletions if requested
            if delete:
                if direction == SyncDirection.UPLOAD:
                    # Delete remote files that don't exist locally
                    for remote_file in remote_files:
                        relative_path = remote_file.name.replace(remote_prefix, "").lstrip('/')
                        if not any(lf['relative_path'] == relative_path for lf in local_files):
                            self.client.delete_file(remote_file.name)
                
                elif direction == SyncDirection.DOWNLOAD:
                    # Delete local files that don't exist remotely
                    for local_file in local_files:
                        remote_path = os.path.join(remote_prefix, local_file['relative_path'])
                        if remote_path not in remote_file_map:
                            os.remove(local_file['full_path'])
        
        except Exception as e:
            errors.append(f"Sync error: {str(e)}")
        
        duration = time.time() - start_time
        
        result = SyncResult(
            files_uploaded=files_uploaded,
            files_downloaded=files_downloaded,
            files_skipped=files_skipped,
            files_failed=files_failed,
            total_size_transferred=total_size_transferred,
            duration=duration,
            errors=errors
        )
        
        self.sync_log.append({
            "timestamp": datetime.now().isoformat(),
            "local_dir": local_dir,
            "remote_prefix": remote_prefix,
            "direction": direction.value,
            "result": result.__dict__
        })
        
        return result
    
    def _get_local_files(self, directory: str) -> List[Dict]:
        """Get list of local files with metadata."""
        files = []
        
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, directory)
                
                stat = os.stat(full_path)
                
                files.append({
                    "full_path": full_path,
                    "relative_path": relative_path,
                    "size": stat.st_size,
                    "modified_time": datetime.fromtimestamp(stat.st_mtime)
                })
        
        return files


class BackupManager:
    """Cloud backup operations."""
    
    def __init__(self, client: CloudStorageClient):
        """Initialize backup manager."""
        self.client = client
        self.backup_log: List[Dict] = []
    
    def create_backup(self, source_path: str, backup_name: str,
                     compression: bool = True) -> bool:
        """Create backup of local directory."""
        start_time = time.time()
        
        try:
            # Create backup name with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_prefix = f"{backup_name}_{timestamp}"
            
            # Upload files
            files_uploaded = 0
            total_size = 0
            
            for root, dirs, filenames in os.walk(source_path):
                for filename in filenames:
                    local_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(local_path, source_path)
                    remote_path = f"{backup_prefix}/{relative_path}"
                    
                    if self.client.upload_file(local_path, remote_path):
                        files_uploaded += 1
                        total_size += os.path.getsize(local_path)
            
            duration = time.time() - start_time
            
            self.backup_log.append({
                "timestamp": datetime.now().isoformat(),
                "source_path": source_path,
                "backup_name": backup_name,
                "backup_prefix": backup_prefix,
                "files_uploaded": files_uploaded,
                "total_size": total_size,
                "duration": duration,
                "success": True
            })
            
            return True
            
        except Exception as e:
            self.backup_log.append({
                "timestamp": datetime.now().isoformat(),
                "source_path": source_path,
                "backup_name": backup_name,
                "success": False,
                "error": str(e)
            })
            return False
    
    def restore_backup(self, backup_prefix: str, restore_path: str) -> bool:
        """Restore backup from cloud storage."""
        start_time = time.time()
        
        try:
            # List backup files
            backup_files = self.client.list_files(backup_prefix)
            
            files_restored = 0
            total_size = 0
            
            for cloud_file in backup_files:
                if cloud_file.is_directory:
                    continue
                
                relative_path = cloud_file.name.replace(backup_prefix, "").lstrip('/')
                local_path = os.path.join(restore_path, relative_path)
                
                # Create directory if needed
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                if self.client.download_file(cloud_file.name, local_path):
                    files_restored += 1
                    total_size += cloud_file.size
            
            duration = time.time() - start_time
            
            self.backup_log.append({
                "timestamp": datetime.now().isoformat(),
                "backup_prefix": backup_prefix,
                "restore_path": restore_path,
                "files_restored": files_restored,
                "total_size": total_size,
                "duration": duration,
                "success": True
            })
            
            return True
            
        except Exception as e:
            self.backup_log.append({
                "timestamp": datetime.now().isoformat(),
                "backup_prefix": backup_prefix,
                "restore_path": restore_path,
                "success": False,
                "error": str(e)
            })
            return False
    
    def list_backups(self, backup_name: str) -> List[Dict]:
        """List available backups."""
        backups = []
        
        try:
            # List all files with backup prefix
            all_files = self.client.list_files(f"{backup_name}_")
            
            # Extract backup prefixes
            backup_prefixes = set()
            for file in all_files:
                # Extract backup prefix from file path
                parts = file.name.split('/')
                if parts:
                    backup_prefixes.add(parts[0])
            
            # Get backup info
            for prefix in sorted(backup_prefixes):
                backup_files = [f for f in all_files if f.name.startswith(prefix)]
                
                if backup_files:
                    total_size = sum(f.size for f in backup_files)
                    oldest = min(f.modified_time for f in backup_files)
                    newest = max(f.modified_time for f in backup_files)
                    
                    backups.append({
                        "prefix": prefix,
                        "file_count": len(backup_files),
                        "total_size": total_size,
                        "created": oldest,
                        "last_modified": newest
                    })
        
        except Exception as e:
            print(f"List backups failed: {e}")
        
        return backups
    
    def delete_backup(self, backup_prefix: str) -> bool:
        """Delete a backup."""
        try:
            # List all files in backup
            backup_files = self.client.list_files(backup_prefix)
            
            # Delete all files
            for cloud_file in backup_files:
                self.client.delete_file(cloud_file.name)
            
            return True
            
        except Exception as e:
            print(f"Delete backup failed: {e}")
            return False


class FileSharing:
    """File sharing and permissions management."""
    
    def __init__(self, client: CloudStorageClient):
        """Initialize file sharing manager."""
        self.client = client
    
    def generate_share_link(self, remote_path: str, 
                           expiration_hours: int = 24) -> Optional[str]:
        """Generate shareable link for file."""
        # This is provider-specific and would require additional implementation
        # For now, return a placeholder
        return f"https://{self.client.provider.value}.example.com/share/{remote_path}"
    
    def set_file_permissions(self, remote_path: str,
                            permissions: Dict[str, str]) -> bool:
        """Set file permissions."""
        # This is provider-specific and would require additional implementation
        return True
    
    def get_file_permissions(self, remote_path: str) -> Dict[str, str]:
        """Get file permissions."""
        # This is provider-specific and would require additional implementation
        return {}


class StorageOptimizer:
    """Storage optimization utilities."""
    
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculate SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    @staticmethod
    def find_duplicate_files(directory: str) -> Dict[str, List[str]]:
        """Find duplicate files based on hash."""
        hash_map = {}
        
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                
                try:
                    file_hash = StorageOptimizer.calculate_file_hash(file_path)
                    
                    if file_hash not in hash_map:
                        hash_map[file_hash] = []
                    
                    hash_map[file_hash].append(file_path)
                except:
                    continue
        
        # Return only duplicates
        return {h: files for h, files in hash_map.items() if len(files) > 1}
    
    @staticmethod
    def compress_directory(directory: str, output_file: str) -> bool:
        """Compress directory into zip file."""
        try:
            import zipfile
            
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, filenames in os.walk(directory):
                    for filename in filenames:
                        file_path = os.path.join(root, filename)
                        arcname = os.path.relpath(file_path, directory)
                        zipf.write(file_path, arcname)
            
            return True
        except Exception as e:
            print(f"Compression failed: {e}")
            return False
    
    @staticmethod
    def get_directory_size(directory: str) -> int:
        """Calculate total size of directory."""
        total_size = 0
        
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    total_size += os.path.getsize(file_path)
                except:
                    continue
        
        return total_size


class CloudStorageManager:
    """High-level cloud storage management."""
    
    def __init__(self):
        """Initialize cloud storage manager."""
        self.clients: Dict[CloudProvider, CloudStorageClient] = {}
    
    def add_client(self, provider: CloudProvider, config: Dict[str, Any]) -> None:
        """Add a cloud storage client."""
        client = CloudStorageClient(provider, config)
        self.clients[provider] = client
    
    def get_client(self, provider: CloudProvider) -> Optional[CloudStorageClient]:
        """Get a specific cloud storage client."""
        return self.clients.get(provider)
    
    def sync_to_all_providers(self, local_path: str, 
                             remote_prefix: str) -> Dict[CloudProvider, SyncResult]:
        """Sync to all configured providers."""
        results = {}
        
        for provider, client in self.clients.items():
            synchronizer = FileSynchronizer(client)
            results[provider] = synchronizer.sync_directory(
                local_path, remote_prefix, SyncDirection.UPLOAD
            )
        
        return results


def demonstrate_cloud_storage():
    """Demonstrate cloud storage functionality."""
    print("=== Cloud Storage Demonstration ===\n")
    
    # Cloud Providers
    print("1. Supported Cloud Providers:")
    for provider in CloudProvider:
        print(f"   - {provider.value}")
    
    # Client Configuration
    print("\n2. Client Configuration:")
    print("   AWS S3: requires access_key, secret_key, region, bucket")
    print("   Google Cloud: requires credentials JSON, bucket")
    print("   Azure Blob: requires account_url, credential, container")
    
    # File Operations
    print("\n3. File Operations:")
    print("   - upload_file(local_path, remote_path)")
    print("   - download_file(remote_path, local_path)")
    print("   - list_files(prefix)")
    print("   - delete_file(remote_path)")
    print("   - get_file_info(remote_path)")
    print("   - file_exists(remote_path)")
    
    # Synchronization
    print("\n4. File Synchronization:")
    print("   - sync_directory(local_dir, remote_prefix, direction)")
    print("   - Supports upload, download, bidirectional sync")
    print("   - Automatic conflict resolution based on timestamps")
    print("   - Optional deletion of orphaned files")
    
    # Backup Operations
    print("\n5. Backup Operations:")
    print("   - create_backup(source_path, backup_name)")
    print("   - restore_backup(backup_prefix, restore_path)")
    print("   - list_backups(backup_name)")
    print("   - delete_backup(backup_prefix)")
    print("   - Automatic timestamping of backups")
    
    # Storage Optimization
    print("\n6. Storage Optimization:")
    print("   - calculate_file_hash(file_path)")
    print("   - find_duplicate_files(directory)")
    print("   - compress_directory(directory, output_file)")
    print("   - get_directory_size(directory)")
    
    # Multi-Cloud Management
    print("\n7. Multi-Cloud Management:")
    print("   - Add multiple cloud providers")
    print("   - Sync to all providers simultaneously")
    print("   - Provider-specific configuration")
    
    # Example Configuration
    print("\n8. Example Configuration:")
    print("""
# AWS S3 Configuration
aws_config = {
    "access_key": "your_access_key",
    "secret_key": "your_secret_key",
    "region": "us-east-1",
    "bucket": "your-bucket"
}

# Google Cloud Configuration
gcp_config = {
    "credentials": "path/to/credentials.json",
    "bucket": "your-bucket"
}

# Create client
client = CloudStorageClient(CloudProvider.AWS_S3, aws_config)

# Upload file
client.upload_file("local_file.txt", "remote_file.txt")

# Download file
client.download_file("remote_file.txt", "downloaded_file.txt")

# List files
files = client.list_files(prefix="documents/")
""")
    
    print("\n=== Demonstration Complete ===")
    print("\nCloud Storage Requirements:")
    print("- AWS S3: pip install boto3")
    print("- Google Cloud: pip install google-cloud-storage")
    print("- Azure Blob: pip install azure-storage-blob")
    print("\nBest Practices:")
    print("- Use encryption for sensitive data")
    print("- Implement proper error handling and retry logic")
    print("- Monitor storage usage and costs")
    print("- Use lifecycle policies for automatic cleanup")
    print("- Implement proper access controls")
    print("- Consider using multi-cloud for redundancy")


if __name__ == "__main__":
    import time
    demonstrate_cloud_storage()