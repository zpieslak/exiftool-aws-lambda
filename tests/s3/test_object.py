import botocore
import datetime
import unittest
from hamcrest import anything, assert_that, has_entries, instance_of
from app.exiftool.s3.object import Object
from tests.config import Config as TestConfig


class TestS3Object(unittest.TestCase):
    def setUp(self) -> None:
        self.config = TestConfig()
        self.config.patcher.environment()
        self.addCleanup(self.config.patcher.stop())

    def test_head_success_pdf(self) -> None:
        with self.config.use_cassette('s3_object_head_succeeded_pdf.yml'):
            result = Object('test-bucket',
                            'test/test.pdf').head()

            assert_that(
                result, has_entries({
                    'ResponseMetadata': has_entries({
                        'RequestId': anything(),
                        'HostId': anything(),
                        'HTTPStatusCode': 200,
                        'HTTPHeaders': has_entries({
                            'accept-ranges': 'bytes',
                            'content-length': '5301',
                            'content-type': 'application/pdf',
                            'date': anything(),
                            'etag': '"fd866ec96c1a91364b52f54b11827a1c"',
                            'last-modified': 'Tue, 31 May 2022 13:11:02 GMT',
                            'server': 'AmazonS3',
                            'x-amz-expiration': anything(),
                            'x-amz-id-2': anything(),
                            'x-amz-request-id': anything(),
                            'x-amz-server-side-encryption': 'AES256'
                        }),
                        'RetryAttempts': 0
                    }),
                    'AcceptRanges': 'bytes',
                    'Expiration': anything(),
                    'LastModified': instance_of(datetime.datetime),
                    'ContentLength': 5301,
                    'ETag': '"fd866ec96c1a91364b52f54b11827a1c"',
                    'ContentType': 'application/pdf',
                    'ServerSideEncryption': 'AES256',
                    'Metadata': {}
                })
            )

    def test_get_default_range_success_pdf(self) -> None:
        with self.config.use_cassette(
                's3_object_get_default_range_succeeded_pdf.yml'):
            result = Object('test-bucket',
                            'test/test.pdf').get()

            assert_that(
                result, has_entries({
                    'ResponseMetadata': has_entries({
                        'RequestId': anything(),
                        'HostId': anything(),
                        'HTTPStatusCode': 206,
                        'HTTPHeaders': has_entries({
                            'date': anything(),
                            'x-amz-id-2': anything(),
                            'x-amz-server-side-encryption': 'AES256',
                            'content-range': 'bytes 0-5300/5301',
                            'server': 'AmazonS3',
                            'x-amz-request-id': anything(),
                            'x-amz-expiration': anything(),
                            'content-length': '5301',
                            'etag': '"fd866ec96c1a91364b52f54b11827a1c"',
                            'accept-ranges': 'bytes',
                            'last-modified': 'Tue, 31 May 2022 13:11:02 GMT',
                            'content-type': 'application/pdf'
                        }),
                        'RetryAttempts': 0
                    }),
                    'AcceptRanges': 'bytes',
                    'Expiration': anything(),
                    'LastModified': instance_of(datetime.datetime),
                    'ContentLength': 5301,
                    'ETag': '"fd866ec96c1a91364b52f54b11827a1c"',
                    'ContentRange': 'bytes 0-5300/5301',
                    'ContentType': 'application/pdf',
                    'ServerSideEncryption': 'AES256',
                    'Metadata': {},
                    'Body': instance_of(botocore.response.StreamingBody)
                })
            )

    def test_get_partial_range_success_pdf(self) -> None:
        with self.config.use_cassette(
                's3_object_get_partial_range_succeeded_pdf.yml'):
            result = Object('test-bucket',
                            'test/test.pdf').get('0-1023')

            assert_that(
                result, has_entries({
                    'ResponseMetadata': has_entries({
                        'RequestId': anything(),
                        'HostId': anything(),
                        'HTTPStatusCode': 206,
                        'HTTPHeaders': has_entries({
                            'date': anything(),
                            'x-amz-id-2': anything(),
                            'x-amz-server-side-encryption': 'AES256',
                            'content-range': 'bytes 0-1023/5301',
                            'server': 'AmazonS3',
                            'x-amz-request-id': anything(),
                            'x-amz-expiration': anything(),
                            'content-length': '1024',
                            'etag': '"fd866ec96c1a91364b52f54b11827a1c"',
                            'accept-ranges': 'bytes',
                            'last-modified': 'Tue, 31 May 2022 13:11:02 GMT',
                            'content-type': 'application/pdf'
                        }),
                        'RetryAttempts': 0
                    }),
                    'AcceptRanges': 'bytes',
                    'Expiration': anything(),
                    'LastModified': instance_of(datetime.datetime),
                    'ContentLength': 1024,
                    'ETag': '"fd866ec96c1a91364b52f54b11827a1c"',
                    'ContentRange': 'bytes 0-1023/5301',
                    'ContentType': 'application/pdf',
                    'ServerSideEncryption': 'AES256',
                    'Metadata': {},
                    'Body': instance_of(botocore.response.StreamingBody)
                })
            )
