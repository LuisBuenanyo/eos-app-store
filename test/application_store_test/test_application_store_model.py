import unittest
from mock import Mock
from application_store.application_store_model import ApplicationStoreModel,\
    Category
import tempfile
import shutil
import os
from sets import ImmutableSet
from application_store.application_store_errors import ApplicationStoreWrappedException


class ApplicationStoreModelTestCase(unittest.TestCase):
    
    def setUp(self):
        self._app_store_dir = tempfile.mkdtemp()
        self._test_object = ApplicationStoreModel(self._app_store_dir)

    def tearDown(self):
        # Remove the temporary directories
        shutil.rmtree(self._app_store_dir)
        
    def test_when_there_is_no_directory_categories_wraps_the_exception(self):
        self.assertRaises(ApplicationStoreWrappedException, ApplicationStoreModel('NonExistantDir').get_categories)

    def test_get_categories_returns_an_empty_list_when_there_are_no_files(self):
        self.assertEquals(ImmutableSet([]), self._test_object.get_categories())

    def test_get_categories_returns_an_empty_list_when_there_are_no_categories(self):
        self._make_file(self._app_store_dir, 'app1.desktop', '[Desktop Entry]\nType=Application\nName=app1\nExec=foo')        
        self._make_file(self._app_store_dir, 'app2.desktop', '[Desktop Entry]\nType=Application\nName=app2\nExec=bar')        
        self.assertEquals(ImmutableSet([]), self._test_object.get_categories())

    def test_get_categories_returns_single_category_from_single_file(self):
        self._make_file(self._app_store_dir, 'app1.desktop', '[Desktop Entry]\nCategories=Audio\nType=Application\nName=app1\nExec=foo')        
        self.assertEquals(ImmutableSet([Category('Audio')]), self._test_object.get_categories())

    def test_two_files_with_same_category(self):
        self._make_file(self._app_store_dir, 'app1.desktop', '[Desktop Entry]\nCategories=Audio\nType=Application\nName=app1\nExec=foo')        
        self._make_file(self._app_store_dir, 'app2.desktop', '[Desktop Entry]\nCategories=Audio\nType=Application\nName=app2\nExec=bar')        
        self.assertEquals(ImmutableSet([Category('Audio')]), self._test_object.get_categories())
    
    def test_two_files_with_different_categories(self):
        self._make_file(self._app_store_dir, 'app1.desktop', '[Desktop Entry]\nCategories=Audio\nType=Application\nName=app1\nExec=foo')        
        self._make_file(self._app_store_dir, 'app2.desktop', '[Desktop Entry]\nCategories=Games\nType=Application\nName=app2\nExec=bar')        
        self.assertEquals(ImmutableSet([Category('Audio'), Category('Games')]), self._test_object.get_categories())
    
    def test_file_with_multiple_categories(self):
        self._make_file(self._app_store_dir, 'app1.desktop', '[Desktop Entry]\nCategories=Audio;Games\nType=Application\nName=app1\nExec=foo')        
        self.assertEquals(ImmutableSet([Category('Audio'), Category('Games')]), self._test_object.get_categories())
    
    def _make_file(self, dirname, filename, content = 'Testing'):
        f = open(os.path.join(dirname, filename), 'w')
        f.write(content)
        f.close()
