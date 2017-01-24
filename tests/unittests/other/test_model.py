import os
import tempfile
import unittest

from dpl.core.config import Config

temp_dir = tempfile.TemporaryDirectory()
temp_dir_path = temp_dir.name


class TestModelInit(unittest.TestCase):
    def test_invalid_path_type(self):
        with self.assertRaisesRegex(ValueError, "config dir must be a string*"):
            Config(None)

    def test_path_is_not_dir(self):
        temp_file = tempfile.NamedTemporaryFile(dir=temp_dir_path)
        temp_file_path = temp_file.name

        with self.assertRaisesRegex(ValueError, "specified path is not a directory"):
            Config(temp_file_path)

    def test_nonexistent_path(self):
        non_existent_path = "{0}/nonexistent".format(temp_dir_path)

        with self.assertRaisesRegex(ValueError, "specified path does not exist"):
            Config(non_existent_path)

    def test_normal_init(self):
        obj = Config("{0}/configs".format(os.getcwd()))
        obj.read_configs()

if __name__ == '__main__':
    unittest.main()
