from . import my_vcr
from ssaw import SettingsApi

@my_vcr.use_cassette()
def test_settings_globalnotice(session):
    """Tests an API call to get/set global settings"""

    SettingsApi(session).set_globalnotice('aaa')
    r = SettingsApi(session).get_globalnotice()
    assert r == 'aaa'

@my_vcr.use_cassette()
def test_settings_globalnotice2(session):
    """Tests an API call to remove global settings"""

    SettingsApi(session).remove_globalnotice()
    r = SettingsApi(session).get_globalnotice()
    assert r == ''

