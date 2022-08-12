import json
import operator
import os
import subprocess
from .s3.object import Object as S3Object
from .s3.object_iterator import ObjectIterator as S3ObjectIterator
from typing import Any, Dict


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    bucket, object = operator.itemgetter('bucket', 'object')(
        event['Records'][0]['s3']
    )

    s3_object_iterator = S3ObjectIterator(
        S3Object(bucket['name'], object['key'])
    )

    output = subprocess.Popen(
        [str(os.getenv('EXIFTOOL_BIN')), '-json', '-fast', '-'],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # BrokenPipeError is expected on larger files as exiftool
    # will broke pipe with `fast` flag
    if output.stdin is not None:
        try:
            for chunk in iter(s3_object_iterator):
                output.stdin.write(chunk)
        except BrokenPipeError as exception:
            print(exception)

    # Wait for process termination
    stdout, stderr = output.communicate()

    return json.loads(
        stdout.decode()
    )[0]
