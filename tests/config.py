from __future__ import annotations
import os
import unittest.mock
import vcr
import json
from types import TracebackType
from typing import Any, AnyStr, Callable, Dict, Optional


class Config:
    def __init__(self) -> None:
        self.patcher = self.Patcher()
        self.fixtures_path = os.path.join(
            os.path.dirname(__file__), 'fixtures'
        )

    def use_cassette(self, name: str) -> vcr.cassette.CassetteContextDecorator:
        return vcr.VCR(
            cassette_library_dir=os.path.join(self.fixtures_path, 'cassettes'),
            match_on=['host', 'method'],
            decode_compressed_response=True,
            filter_headers=['authorization']
        ).use_cassette(name)

    def event(self, path: str) -> Dict[str, Any]:
        with open(os.path.join(self.fixtures_path, 'events', path)) as f:
            return json.load(f)

    class Patcher:
        def environment(self) -> os._Environ[AnyStr]:
            return unittest.mock.patch.dict(
                os.environ,
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    'AWS_SECRET_ACCESS_KEY': 'secret_access_key',
                    'AWS_DEFAULT_REGION': 'us-east-2',
                    'EXIFTOOL_BIN': '/opt/bin/exiftool'
                },
                clear=True
            ).start()

        def stop(self) -> Callable[[], None]:
            return unittest.mock.patch.stopall

    def __enter__(self) -> Config:
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        pass
