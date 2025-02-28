import pytest
from fitspy.apps.pyside.main_model import MainModel

@pytest.fixture
def mock_qsettings(mocker):
    """Mock QSettings to avoid writing to actual registry during tests"""
    mock_settings = mocker.patch('fitspy.apps.pyside.main_model.QSettings')

    settings_instance = mocker.MagicMock()
    settings_instance.values = {}
    
    def value_side_effect(key, default=None, type=None):
        return settings_instance.values.get(key, default)
    
    def setValue_side_effect(key, value):
        settings_instance.values[key] = value
    
    def contains_side_effect(key):
        return key in settings_instance.values
    
    settings_instance.value.side_effect = value_side_effect
    settings_instance.setValue.side_effect = setValue_side_effect
    settings_instance.contains.side_effect = contains_side_effect
    
    mock_settings.return_value = settings_instance
    yield settings_instance

@pytest.fixture
def mock_defaults(mocker):
    """Mock DEFAULTS dictionary"""
    mock_defaults = mocker.patch('fitspy.apps.pyside.main_model.DEFAULTS')
    mock_defaults.return_value = {
        'theme': 'light',
        'peaks_cmap': 'viridis',
        'map_cmap': 'plasma',
        'dx0': 0.1,
        'dfwhm': 0.2,
        'nested': {
            'setting1': 'value1',
            'setting2': True
        }
    }
    yield mock_defaults.return_value

def test_initialization(mock_qsettings):
    """Test proper initialization of MainModel"""
    model = MainModel()
    assert isinstance(model, MainModel)
    assert model.settings == mock_qsettings

def test_check_version(mock_qsettings, mocker):
    """Test version checking and setting migration"""
    # Set initial version to older version
    old_version = '2025.1'
    expected_version = '2025.2'
    mock_qsettings.values['version'] = old_version
    
    mocker.patch('fitspy.apps.pyside.main_model.VERSION', expected_version)
    MainModel()

    mock_qsettings.setValue.assert_any_call('version', expected_version)
    mock_qsettings.sync.assert_called_once()
    assert mock_qsettings.values['version'] == expected_version

def test_settings_key_migration(mock_qsettings, mocker):
    """Test version checking with key mapping migration"""
    mock_qsettings.values['old_key'] = 'test_value'
    
    key_mapping = {
        "new_key": ["old_key"],
    }
    
    mocker.patch('fitspy.apps.pyside.main_model.SETTINGS_KEY_MIGRATIONS', key_mapping)
    MainModel()
    
    assert 'new_key' in mock_qsettings.values
    assert mock_qsettings.values['new_key'] == 'test_value'
    
    mock_qsettings.remove.assert_called_with('old_key')

def test_settings_value_migration(mock_qsettings, mocker):
    """Test version checking with value mapping migration"""
    mock_qsettings.values['click_mode'] = 'highlight'
    
    value_mapping = {
        "click_mode": {"highlight": "new_value"}
    }
    
    mocker.patch('fitspy.apps.pyside.main_model.SETTINGS_VALUE_MIGRATIONS', value_mapping)
    MainModel()
    assert mock_qsettings.values['click_mode'] == 'new_value'
