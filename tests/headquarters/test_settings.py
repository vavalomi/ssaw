import vcr

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/headquarters/vcr_cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode='once',
    filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette()
def test_settings_globalnotice(session):
    """Tests an API call to get/set global settings"""

    session.settings.set_globalnotice('aaa')
    r = session.settings.get_globalnotice()
    assert r == 'aaa'

@my_vcr.use_cassette()
def test_settings_globalnotice2(session):
    """Tests an API call to remove global settings"""

    session.settings.remove_globalnotice()
    r = session.settings.get_globalnotice()
    assert r == ''

