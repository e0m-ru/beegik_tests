import unittest
from beegik_tests import MultiKeyDict


class TestMultiKeyDict(unittest.TestCase):
    def setUp(self):
        self.multi_key_dict = MultiKeyDict()

    def test_alias(self):
        self.multi_key_dict.alias('original_key', 'alias_key')
        self.assertEqual(
            self.multi_key_dict._aliases['alias_key'], 'original_key')

    def test_getitem_existing_key(self):
        self.multi_key_dict['key1'] = 'value1'
        self.assertEqual(self.multi_key_dict['key1'], 'value1')

    def test_getitem_alias_key(self):
        self.multi_key_dict['key1'] = 'value1'
        self.multi_key_dict.alias('key1', 'alias_key')
        self.assertEqual(self.multi_key_dict['alias_key'], 'value1')

    def test_getitem_missing_key(self):
        with self.assertRaises(KeyError):
            self.multi_key_dict['missing_key']

    def test_setitem_existing_key(self):
        self.multi_key_dict['key1'] = 'value1'
        self.multi_key_dict['key1'] = 'updated_value'
        self.assertEqual(self.multi_key_dict['key1'], 'updated_value')

    def test_setitem_alias_key(self):
        self.multi_key_dict['key1'] = 'value1'
        self.multi_key_dict.alias('key1', 'alias_key')
        self.multi_key_dict['alias_key'] = 'updated_value'
        self.assertEqual(self.multi_key_dict['key1'], 'updated_value')

    def test_delitem_existing_key(self):
        self.multi_key_dict['key1'] = 'value1'
        del self.multi_key_dict['key1']
        with self.assertRaises(KeyError):
            self.multi_key_dict['key1']

    def test_delitem_alias_key(self):
        self.multi_key_dict['key1'] = 'value1'
        self.multi_key_dict.alias('key1', 'alias_key')
        del self.multi_key_dict['alias_key']
        with self.assertRaises(KeyError):
            self.multi_key_dict['key1']

    def test_delitem_non_existing_key(self):
        with self.assertRaises(KeyError):
            del self.multi_key_dict['non_existing_key']


if __name__ == '__main__':
    unittest.main()
