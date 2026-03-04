import json
import os

import vcr


my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/headquarters/vcr_cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode='once',
    filter_headers=[('authorization', None)],
    decode_compressed_response=True,
)


def load_fixture(name: str) -> dict:
    """Load a JSON fixture file from mock_fixtures/."""
    fixtures_dir = os.path.join(os.path.dirname(__file__), "mock_fixtures")
    with open(os.path.join(fixtures_dir, name), encoding="utf-8") as fh:
        return json.load(fh)
