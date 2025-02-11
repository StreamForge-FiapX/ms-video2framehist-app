class VideoStatus:
    def __init__(self, file_name: str, status: str, upload_timestamp: str, s3_object_key: str):
        self.file_name = file_name
        self.status = status
        self.upload_timestamp = upload_timestamp
        self.s3_object_key = s3_object_key

    def to_dict(self):
        return {
            'FileName': self.file_name,
            'Status': self.status,
            'UploadTimestamp': self.upload_timestamp,
            'S3ObjectKey': self.s3_object_key
        }
