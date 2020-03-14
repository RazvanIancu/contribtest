import unittest
import generate
import json
import filecmp
class Test(unittest.TestCase):

    '''
        Testing if we can read properly data and content from the .rst
    '''
    def test_read_file_data(self):
        data, content = generate.read_file("test/source/contact.rst")
        
        self.assertEqual(data, json.loads('{"title": "Contact us!", "layout": "base.html"}'))
        self.assertEqual(content, "Write an email to contact@example.com.")

    '''
        Testing the whole program with files given
    '''
    def test_generate_site(self):
        generate.generate_site('test/source/', 'output')
        
        self.assertTrue(filecmp.cmp('test/expected_output2/contact.html', 'output/contact.html'));
        self.assertTrue(filecmp.cmp('test/expected_output2/index.html', 'output/index.html'));

if __name__ == '__main__':
    unittest.main()