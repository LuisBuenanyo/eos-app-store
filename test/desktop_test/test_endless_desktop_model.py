import unittest
from desktop.endless_desktop_model import EndlessDesktopModel
from mock import Mock #@UnresolvedImport
from osapps.app_launcher import AppLauncher
from osapps.app import App
from osapps.app_shortcut import AppShortcut
from osapps.desktop_locale_datastore import DesktopLocaleDatastore
from osapps.app_datastore import AppDatastore
from osapps.launchable_app import LaunchableApp
from osapps.desktop_preferences_datastore import DesktopPreferencesDatastore
from util.feedback_manager import FeedbackManager
from metrics.time_provider import TimeProvider

class DesktopModelTestCase(unittest.TestCase):
    def setUp(self):
        self.available_apps = [
                               App(123, "app 1", "", "", "", False, False, True), 
                               App(234, "app 2", "", "", "", False, False, True), 
                               App(345, "app 3", "", "", "", False, False, True), 
                               App(456, "app 4", "", "", "", False, False, False), 
                               App(567, "app 5", "", "", "", False, False, True), 
                               App(890, "app 6", "", "", "", False, False, True), 
                               ]
        self.available_app_shortcuts = [
                                        AppShortcut(123, "App 1", "", []),
                                        AppShortcut(234, "App 2", "", []),
                                        AppShortcut(345, "App 3", "", [])
                                        ]
        self.mock_desktop_locale_datastore = Mock(DesktopLocaleDatastore)
        self.mock_desktop_locale_datastore.get_all_shortcuts = Mock(return_value=self.available_apps)
        self.mock_app_datastore = Mock(AppDatastore)
        self.app_mock = Mock(LaunchableApp)
        self.app_mock.executable = Mock(return_value="eog")
        self.mock_app_datastore.get_app_by_key = Mock(return_value=self.app_mock)
        self.mock_app_launcher = Mock(AppLauncher)
        self.mock_feedback_manager = Mock(FeedbackManager)
        self.mock_time_provider = Mock(TimeProvider)
        self.mock_desktop_preferences = Mock(DesktopPreferencesDatastore)
        self.testObject = EndlessDesktopModel(self.mock_desktop_locale_datastore,
                                              self.mock_desktop_preferences, 
                                              self.mock_app_datastore, 
                                              self.mock_app_launcher,
                                              self.mock_feedback_manager,
                                              self.mock_time_provider, 
                                              )
    
    def test_initially_shortcut_list_is_retrieved_from_app_util_manager(self):
        self.assertEqual(self.available_apps, self.testObject.get_shortcuts())

    def test_execute_app_with_id_calls_launc_app_on_app_util(self):
        params = []
        self.testObject.execute_app('123', params)
        
        self.mock_app_launcher.launch.assert_called_once_with("eog", params)
        
    def test_execute_app_with_cannot_find_app_no_exception(self):
        self.mock_app_datastore = Mock(AppDatastore)
        self.mock_app_datastore.get_app_by_key = Mock(return_value=None)
        self.testObject = EndlessDesktopModel(self.mock_desktop_locale_datastore, 
                                              self.mock_desktop_preferences, 
                                              self.mock_app_datastore, 
                                              self.mock_app_launcher,
                                              self.mock_feedback_manager,
                                              self.mock_time_provider,
                                              )
        
        params = []
        self.testObject.execute_app('123', params)
        
        self.assertFalse(self.mock_app_launcher.launch.called)
        
    def test_launch_search_launches_browser_with_search_string(self):
        search_string = "foo"
        
        self.testObject.launch_search(search_string)
        
        self.mock_app_launcher.launch_browser.assert_called_once_with(search_string)

    def test_get_background_delegates_to_preferences_datastore(self):
        self.testObject.get_background_pixbuf()
        
        self.mock_desktop_preferences.get_background_pixbuf.assert_called()

    def test_set_background_delegates_to_preferences_datastore(self):
        expected = "/foo/whatever/blah"
        self.testObject.set_background(expected)
        
        self.mock_desktop_preferences.set_background.assert_called_once_with(expected)
        
    def test_get_default_background_delegates_to_preferences_datastore(self):
        self.testObject.get_default_background()
        
        self.mock_desktop_preferences.get_default_background.assert_called()
        
    def test_delete_shortcut_exists(self):
        self.mock_desktop_locale_datastore.get_all_shortcuts = Mock(return_value=self.available_app_shortcuts)
        self.assertEqual(self.testObject.delete_shortcut('App 2'), True, 'Delete shortcut which exists FAILED.')
    
    def test_delete_shortcut_does_not_exist(self):
        self.mock_desktop_locale_datastore.get_all_shortcuts = Mock(return_value=self.available_app_shortcuts)
        self.assertEqual(self.testObject.delete_shortcut('Dummy, non existant App'), False, 'Delete shortcut which does not exist FAILED.')
    
    def test_delete_shortcut_exception_handled(self):
        self.mock_desktop_locale_datastore.get_all_shortcuts = Mock(return_value=self.available_app_shortcuts)
        self.mock_desktop_locale_datastore.set_all_shortcuts = Mock(side_effect=Exception('Booom!'))
        #self.mock_desktop_locale_datastore.set_all_shortcuts()
        self.assertEqual(self.testObject.delete_shortcut('App 2'), False, 'Delete shortcut, exception handled FAILED.')
