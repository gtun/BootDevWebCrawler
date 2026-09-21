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

if __name__ == "__main__":
    unittest.main()