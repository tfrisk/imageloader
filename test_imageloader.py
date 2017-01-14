import unittest
from imageloader import imageLoader

class imageloader_test(unittest.TestCase):
    def test_config_case1(self):
        loader = imageLoader(['-u', 'http://www.google.com', '-d'])
        self.assertEqual(loader.args.url, 'http://www.google.com')
        self.assertEqual(loader.DEBUG_MODE, True)
        self.assertEqual(loader.args.dir, 'saved-images')

    def test_config_case1(self):
        loader = imageLoader(['-u', 'http://www.google.com', '-D', 'dldir'])
        self.assertEqual(loader.args.url, 'http://www.google.com')
        self.assertEqual(loader.DEBUG_MODE, False)
        self.assertEqual(loader.args.dir, 'dldir')

    def test_downloadRawUrl_ok(self):
        """Get OK response from proper url"""
        loader = imageLoader(['-u', 'http://www.google.com'])
        response, status = loader.getUrlResponse("http://www.google.com/")
        self.assertEqual(status, 200)

    def test_getUrlResponse_notfound(self):
        """Get error response from incorrect url"""
        loader = imageLoader(['-u', 'http://www.google.com'])
        response, status = loader.getUrlResponse("http://www.google.com/this-does-not-exist.xml")
        self.assertEqual(status, 404)

    def test_findKeyOrEmpty(self):
        """Test dictionary key wrapper"""
        val = imageLoader.findKeyOrEmpty({"a":1, "b":2}, "a")
        self.assertEqual(val,1)
        val = imageLoader.findKeyOrEmpty({"a":1, "b":2}, "c")
        self.assertEqual(val,'')
        val = imageLoader.findKeyOrEmpty({}, "a")
        self.assertEqual(val,'')

    def test_formProposedUrl(self):
        """Test url forming"""
        loader = imageLoader(['-u', 'http://www.google.com'])
        url1 = imageLoader.formProposedUrl(loader, "//google.com/media/test.png", "append")
        self.assertEqual(url1, "http://google.com/media/test.png")
        url2 = imageLoader.formProposedUrl(loader, "/media/test.png", "combine")
        self.assertEqual(url2, "http://www.google.com//media/test.png")

if __name__ == '__main__':
    unittest.main()
