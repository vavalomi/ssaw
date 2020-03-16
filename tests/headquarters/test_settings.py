from . import my_vcr


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

