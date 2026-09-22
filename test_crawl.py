import unittest
from crawl import *

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
#        input_url = "https://www.boot.dev/blog/path"
#        actual = normalize_url(input_url)
#        expected = "www.boot.dev/blog/path"
#        self.assertEqual(actual, expected)
        test_cases = [
             ("https://www.boot.dev/blog/path/", "www.boot.dev/blog/path"),
            ("https://www.boot.dev/blog/path",  "www.boot.dev/blog/path"),
            ("http://www.boot.dev/blog/path/",  "www.boot.dev/blog/path"),
            ("http://www.boot.dev/blog/path",   "www.boot.dev/blog/path"),
            ("    http://www.boot.dev/blog/path",   "www.boot.dev/blog/path"),
            ("http://www.boot.dev/blog/path/   ",   "www.boot.dev/blog/path")
        ]

        for input_url, expected in test_cases:
            with self.subTest(input_url=input_url):
                actual = normalize_url(input_url)
                self.assertEqual(actual, expected)




    def test_get_heading_from_html(self):
        test_cases = [("""<html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                    <main>
                        <p>Learn to code by building real projects.</p>
                        <p>This is the second paragraph.</p>
                    </main>
                </body>
            </html>""","Welcome to Boot.dev"),
            ("""<html>
                <body>
                    <p>Hello world</p>
                </body>
            </html>""",""),
            ("""<html>
                <body>
                    <h2>Hello world</h2>    
                </body>
            </html>""","Hello world"),
            ("""<html>
                <body>
                    <h1>Hello</h1>
                    <h2>to the world</h2>    
                </body>
            </html>""","Hello"),
            ("""<html>
                <body>
                    <h1>Hello</h1>
                    <h1>Goodbye</h1>    
                </body>
            </html>""","Hello")]

        for html, expected_heading in test_cases:
            with self.subTest(html=html):
                actual_heading = get_heading_from_html(html)
                self.assertEqual(actual_heading, expected_heading)




    def test_get_first_paragraph_from_html(self):
        test_cases = [("""<html>
            <body>
                <h1>Welcome to Boot.dev</h1>
                    <main>
                        <p>Just one paragraph</p>
                    </main>
                </body>
            </html>""","Just one paragraph"),
            ("""<html>
                <body>
                    <p>Two paragraphs, and this is the correct one</p>
                    <p>Two paragraphs, but this is the incorrect one</p>
                </body>
            </html>""","Two paragraphs, and this is the correct one"),
            ("""<html>
                <body>
                    <h2>Hello world</h2>    
                </body>
            </html>""",""),
            ("""<html>
                <body>
                    <p>Outside paragraph.</p>
                    <main>
                        <p>Main paragraph.</p>
                    </main>
                </body>
            </html>""","Main paragraph."),]

        for html, expected_heading in test_cases:
            with self.subTest(html=html):
                actual_heading = get_first_paragraph_from_html(html)
                self.assertEqual(actual_heading, expected_heading)




    def test_get_urls_from_html(self):
        test_cases = [("""<html>
            <body>
                <a href="https://crawler-test.com">Go to Boot.dev</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
            </body>
            </html>""","https://crawler-test.com",["https://crawler-test.com"]),
            ("""<html>
            <body>
                <a href="menu">Go to Boot.dev menu page</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
            </body>
            </html>""","https://crawler-test.com",["https://crawler-test.com/menu"]),
            ("""<html>
            <body>
                <a href="menu">Go to Boot.dev menu page</a>
                <a href="games/">Go to Boot.dev games page</a>
                <a href="/settings">Go to Boot.dev settings page</a>
                <a href="/support/">Go to Boot.dev support page</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
            </body>
            </html>""","https://crawler-test.com",["https://crawler-test.com/menu","https://crawler-test.com/games/","https://crawler-test.com/settings","https://crawler-test.com/support/"])
        ]

        for html, base_url, expected_urls in test_cases:
            with self.subTest(html=html):
                actual_urls = get_urls_from_html(html, base_url)
                self.assertEqual(actual_urls, expected_urls)
                
        with self.assertRaises(ValueError):
            get_urls_from_html("""<html>
            <body>
                <a>Go to Boot.dev menu page</a>
                <a>Go to Boot.dev games page</a>
                <a>Go to Boot.dev settings page</a>
                <a>Go to Boot.dev support page</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
            </body>
            </html>""", "https://crawler-test.com")
                
                
                
                
    def test_get_images_from_html(self):
        test_cases = [("""<html>
            <body>
                <a href="https://crawler-test.com">Go to Boot.dev</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
            </body>
            </html>""","https://crawler-test.com",["https://crawler-test.com/logo.png"]),
            ("""<html>
            <body>
                <a href="menu">Go to Boot.dev menu page</a>
                <img src="/logo.png" alt="Boot.dev Logo" />
                <img src="/images/banner.jpg" alt="Boot.dev Banner" />
            </body>
            </html>""","https://crawler-test.com",["https://crawler-test.com/logo.png","https://crawler-test.com/images/banner.jpg"])
        ]

        for html, base_url, expected_images in test_cases:
            with self.subTest(html=html):
                actual_images = get_images_from_html(html, base_url)
                self.assertEqual(actual_images, expected_images)
                
        with self.assertRaises(ValueError):
            get_images_from_html("<html><body><img alt='Logo'></body></html>", "https://crawler-test.com")



    def test_extract_page_data(self):
        
        test_cases = [
            (
                """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
                </body></html>""",
                "https://crawler-test.com",
                {
                    "url": "https://crawler-test.com",
                    "heading": "Test Title",
                    "first_paragraph": "This is the first paragraph.",
                    "outgoing_links": ["https://crawler-test.com/link1"],
                    "image_urls": ["https://crawler-test.com/image1.jpg"],
                }
            )
        ]
        
        for html, pageurl, expected_data in test_cases:
            with self.subTest(html=html):
                actual_data = extract_page_data(html, pageurl)
                self.assertEqual(actual_data, expected_data)
                
                
                
    def test_placeholder_1(self):
        self.assertTrue(True)

    def test_placeholder_2(self):
        self.assertTrue(True)

    def test_placeholder_3(self):
        self.assertTrue(True)

    def test_placeholder_4(self):
        self.assertTrue(True)

    def test_placeholder_5(self):
        self.assertTrue(True)

    def test_placeholder_6(self):
        self.assertTrue(True)

    def test_placeholder_7(self):
        self.assertTrue(True)

    def test_placeholder_8(self):
        self.assertTrue(True)

    def test_placeholder_9(self):
        self.assertTrue(True)

    def test_placeholder_10(self):
        self.assertTrue(True)

    def test_placeholder_11(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()