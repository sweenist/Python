from data_process import DataProcess
import os, sys
import unittest
from unittest.mock import Mock, patch

class TestDataProcess(unittest.TestCase):
    def setUp(self):
        self.no_filename = DataProcess()
        self.non_existent_filename = DataProcess("some arbitrary string")
        self.empty_file = DataProcess("test\\test_empty_data.txt")
        self.real_data_file = DataProcess("test\\test_data.txt")

        self.no_filename.process = Mock(return_value=None)
        self.non_existent_filename.process = Mock(return_value=None)
        self.empty_file.process = Mock(return_value=None)
        self.real_data_file.process = Mock(return_value=None)
    
    def test_initialize(self):
        self.assertTrue(self.no_filename.filename is not None)
        self.assertFalse(os.path.exists(self.non_existent_filename.filename))
        self.assertTrue(os.path.exists(self.empty_file.filename))
        self.assertTrue(os.path.exists(self.real_data_file.filename))

        self.assertFalse(self.non_existent_filename.process.called)
        self.assertFalse(self.no_filename.process.called)
        self.assertTrue(self.empty_file.process.called)
        self.assertTrue(self.real_data_file.process.called)

    def test_process(self):
        self.no_filename.process()
        self.assertTrue(self.no_filename.data == {})

        self.non_existent_filename.process()
        self.assertTrue(self.non_existent_filename.data == {})

        self.empty_file.process()
        self.assertTrue(self.empty_file.data == {})

        self.real_data_file.process()
        self.assertFalse(self.real_data_file.data == {})

if __name__=="__main__":
    unittest.main()
