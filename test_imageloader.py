import unittest
from imageloader import imageLoader

class imageloader_test(unittest.TestCase):

    def test_downloadRawUrl_ok(self):
        """Get OK response from proper url"""
        response, status = imageLoader.getUrlResponse("http://www.google.com/")
        self.assertEqual(status, 200)

    def test_downloadRawUrl_notfound(self):
        """Get error response from incorrect url"""
        response, status = imageLoader.getUrlResponse("http://www.apsisaudio.com/this-does-not-exist.xml")
        self.assertEqual(status, -1)
        self.assertEqual(response, "ERROR")

    def test_findKeyOrEmpty(self):
        val = imageLoader.findKeyOrEmpty({"a":1, "b":2}, "a")
        self.assertEqual(val,1)
        val = imageLoader.findKeyOrEmpty({"a":1, "b":2}, "c")
        self.assertEqual(val,'')

if __name__ == '__main__':
    unittest.main()
