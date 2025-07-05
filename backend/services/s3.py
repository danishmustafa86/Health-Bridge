"""
AWS S3 Service
Handles file upload, download, and management using boto3
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from datetime import datetime
import uuid

class S3Service:
    """AWS S3 service class for file operations"""
    
    def __init__(self):
        """Initialize S3 service with AWS credentials"""
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "medcare-files")
        
        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS credentials are required")
        
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
        except NoCredentialsError:
            raise ValueError("Invalid AWS credentials")
    
    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        folder: str = ""
    ) -> str:
        """
        Upload file to S3 bucket
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            content_type: MIME type of the file
            folder: S3 folder path (optional)
        
        Returns:
            str: S3 object key/URL
        """
        try:
            # Generate unique filename
            file_extension = filename.split('.')[-1] if '.' in filename else ''
            unique_filename = f"{uuid.uuid4()}.{file_extension}" if file_extension else str(uuid.uuid4())
            
            # Construct S3 key
            s3_key = f"{folder}/{unique_filename}" if folder else unique_filename
            
            # Upload file
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    'original_filename': filename,
                    'upload_date': datetime.now().isoformat()
                }
            )
            
            return s3_key
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="S3 bucket not found"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload file: {str(e)}"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )
    
    async def download_file(self, s3_key: str) -> bytes:
        """
        Download file from S3
        
        Args:
            s3_key: S3 object key
        
        Returns:
            bytes: File content
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return response['Body'].read()
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to download file: {str(e)}"
                )
    
    async def generate_download_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """
        Generate presigned URL for file download
        
        Args:
            s3_key: S3 object key
            expires_in: URL expiration time in seconds (default: 1 hour)
        
        Returns:
            str: Presigned download URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate download URL: {str(e)}"
            )
    
    async def delete_file(self, s3_key: str) -> bool:
        """
        Delete file from S3
        
        Args:
            s3_key: S3 object key
        
        Returns:
            bool: True if successful
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            return True
        
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete file: {str(e)}"
            )
    
    async def list_files(self, folder: str = "", max_keys: int = 100) -> List[Dict[str, Any]]:
        """
        List files in S3 bucket
        
        Args:
            folder: S3 folder path (optional)
            max_keys: Maximum number of files to return
        
        Returns:
            List[Dict]: List of file information
        """
        try:
            kwargs = {
                'Bucket': self.bucket_name,
                'MaxKeys': max_keys
            }
            
            if folder:
                kwargs['Prefix'] = folder
            
            response = self.s3_client.list_objects_v2(**kwargs)
            
            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'].strip('"')
                })
            
            return files
        
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list files: {str(e)}"
            )
    
    async def get_file_metadata(self, s3_key: str) -> Dict[str, Any]:
        """
        Get file metadata from S3
        
        Args:
            s3_key: S3 object key
        
        Returns:
            Dict: File metadata
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            return {
                'size': response['ContentLength'],
                'content_type': response['ContentType'],
                'last_modified': response['LastModified'].isoformat(),
                'etag': response['ETag'].strip('"'),
                'metadata': response.get('Metadata', {})
            }
        
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to get file metadata: {str(e)}"
                )
    
    def is_bucket_accessible(self) -> bool:
        """
        Check if S3 bucket is accessible
        
        Returns:
            bool: True if bucket is accessible
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False