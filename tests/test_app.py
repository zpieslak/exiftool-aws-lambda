import unittest
from hamcrest import anything, assert_that, has_entries, instance_of
from app.exiftool.app import handler
from tests.config import Config as TestConfig


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.config = TestConfig()
        self.config.patcher.environment()
        self.addCleanup(self.config.patcher.stop())

    def test_handler_succeeded_binary(self) -> None:
        self.event = self.config.event('s3_put_binary.json')

        with self.config.use_cassette('app_succeeded_binary.yml'):
            result = handler(self.event, None)

            assert_that(
                result, has_entries({
                    'SourceFile': '-',
                    'ExifToolVersion': instance_of(float),
                    'FileSize': '0 bytes',
                    'FileModifyDate': anything(),
                    'FileAccessDate': anything(),
                    'FileInodeChangeDate': anything(),
                    'FilePermissions': 'prw-------',
                    'Error': 'Unknown file type'
                })
            )

    def test_handler_succeeded_pdf(self) -> None:
        self.event = self.config.event('s3_put_pdf.json')

        with self.config.use_cassette('app_succeeded_pdf.yml'):
            result = handler(self.event, None)

            assert_that(
                result, has_entries({
                    'SourceFile': '-',
                    'ExifToolVersion': instance_of(float),
                    'FileSize': '0 bytes',
                    'FileModifyDate': anything(),
                    'FileAccessDate': anything(),
                    'FileInodeChangeDate': anything(),
                    'FilePermissions': 'prw-------',
                    'FileType': 'PDF',
                    'FileTypeExtension': 'pdf',
                    'MIMEType': 'application/pdf',
                    'PDFVersion': 1.4,
                    'Linearized': 'No',
                    'PageCount': 1,
                    'XMPToolkit': 'XMP toolkit 2.9.1-13, framework 1.6',
                    'Producer': 'GPL Ghostscript 9.56.1',
                    'ModifyDate': '2022:05:31 15:10:30+02:00',
                    'CreateDate': '2022:05:31 15:10:30+02:00',
                    'CreatorTool': 'GNU Enscript 1.6.6',
                    'DocumentID': 'uuid:9881c87a-18ff-11f8-0000-8aa3554e5edc',
                    'Format': 'application/pdf',
                    'Title': 'Enscript Output',
                    'Creator': '',
                    'Author': ''
                })
            )

    def test_handler_succeeded_avi(self) -> None:
        self.event = self.config.event('s3_put_avi.json')

        with self.config.use_cassette('app_succeeded_avi.yml'):
            result = handler(self.event, None)

            assert_that(
                result, has_entries({
                    'SourceFile': '-',
                    'ExifToolVersion': instance_of(float),
                    'FileSize': '0 bytes',
                    'FileModifyDate': anything(),
                    'FileAccessDate': anything(),
                    'FileInodeChangeDate': anything(),
                    'FilePermissions': 'prw-------',
                    'FileType': 'AVI',
                    'FileTypeExtension': 'avi',
                    'MIMEType': 'video/x-msvideo',
                    'FrameRate': 30,
                    'MaxDataRate': '24.41 kB/s',
                    'FrameCount': 18000,
                    'StreamCount': 1,
                    'StreamType': 'Video',
                    'VideoCodec': 'FMP4',
                    'VideoFrameRate': 30,
                    'VideoFrameCount': 18000,
                    'Quality': 'Default',
                    'SampleSize': 'Variable',
                    'BMPVersion': 'Windows V3',
                    'ImageWidth': 1920,
                    'ImageHeight': 1080,
                    'Planes': 1,
                    'BitDepth': 24,
                    'Compression': 'FMP4',
                    'ImageLength': 6220800,
                    'PixelsPerMeterX': 0,
                    'PixelsPerMeterY': 0,
                    'NumColors': 'Use BitDepth',
                    'NumImportantColors': 'All',
                    'Software': 'Lavf59.16.100',
                    'ImageSize': '1920x1080',
                    'Megapixels': 2.1,
                    'Duration': '0:10:00'
                })
            )
