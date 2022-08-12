import boto3
from typing import Any, Dict


class Object:
    def __init__(self, bucket: str, key: str) -> None:
        self.client = boto3.client('s3')
        self.key = key
        self.bucket = bucket

    def head(self) -> Dict[str, Any]:
        return self.client.head_object(
            Bucket=self.bucket,
            Key=self.key
        )

    def get(self, Range: str = '0-') -> Dict[str, Any]:
        return self.client.get_object(
            Bucket=self.bucket,
            Key=self.key,
            Range=f'bytes={Range}'
        )
