from __future__ import annotations
from .object import Object as S3Object


class ObjectIterator:
    def __init__(self, s3_object: S3Object) -> None:
        self.s3_object = s3_object
        self.chunk_size = 8388608  # 8 MB
        self.max_last_byte_pos = self.s3_object.head()['ContentLength'] - 1
        self.first_byte_pos = 0
        self.last_byte_pos = -1

    def __iter__(self) -> ObjectIterator:
        return self

    def __next__(self) -> bytes:
        # Stop iteration when reached to the end of file
        if self.last_byte_pos >= self.max_last_byte_pos:
            raise StopIteration

        # Set first and last byte position
        # Byte range needs to be shift by -1
        self.first_byte_pos = self.last_byte_pos + 1
        self.last_byte_pos += self.chunk_size

        # Verify last byte position to avoid InvalidRange error
        if self.last_byte_pos > self.max_last_byte_pos:
            self.last_byte_pos = self.max_last_byte_pos

        return self.s3_object.get(
            f'{self.first_byte_pos}-{self.last_byte_pos}'
        )['Body'].read()
