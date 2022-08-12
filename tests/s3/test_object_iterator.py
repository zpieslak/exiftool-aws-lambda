import unittest
from hamcrest import assert_that, instance_of, equal_to, raises, calling
from app.exiftool.s3.object import Object
from app.exiftool.s3.object_iterator import ObjectIterator
from tests.config import Config as TestConfig


class TestS3ObjectIterator(unittest.TestCase):
    def setUp(self) -> None:
        self.config = TestConfig()
        self.config.patcher.environment()
        self.addCleanup(self.config.patcher.stop())

    def test_next_success(self) -> None:
        with self.config.use_cassette('s3_object_iterator_succeeded_pdf.yml'):
            object_iterator = ObjectIterator(
                Object('test-bucket', 'test/test.pdf')
            )

            assert_that(
                object_iterator.__next__(),
                instance_of(bytes)
            )
            assert_that(object_iterator.first_byte_pos, equal_to(0))
            assert_that(object_iterator.last_byte_pos, equal_to(5300))

    def test_next_failure(self) -> None:
        with self.config.use_cassette('s3_object_iterator_succeeded_pdf.yml'):
            object_iterator = ObjectIterator(
                Object('test-bucket', 'test/test.pdf')
            )
            object_iterator.__next__()

            assert_that(
                calling(object_iterator.__next__),
                raises(StopIteration)
            )  # type: ignore
