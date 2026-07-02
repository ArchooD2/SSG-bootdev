import os
import tempfile
import unittest

from generate_page import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_strips_whitespace(self):
        markdown = "#    Tolkien Fan Club   "
        self.assertEqual(
            extract_title(markdown),
            "Tolkien Fan Club",
        )

    def test_extract_title_from_document(self):
        markdown = """Some text before the heading

# Main Title

## Smaller Heading
"""

        self.assertEqual(
            extract_title(markdown),
            "Main Title",
        )

    def test_ignores_h2(self):
        markdown = """## Not the title

# Actual Title
"""

        self.assertEqual(
            extract_title(markdown),
            "Actual Title",
        )

    def test_missing_title(self):
        markdown = """## Only an h2

This is a paragraph.
"""

        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_hash_without_space_is_not_title(self):
        with self.assertRaises(ValueError):
            extract_title("#Not a valid heading")


class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            markdown_path = os.path.join(
                temp_directory,
                "content",
                "index.md",
            )
            template_path = os.path.join(
                temp_directory,
                "template.html",
            )
            destination_path = os.path.join(
                temp_directory,
                "public",
                "index.html",
            )

            os.makedirs(os.path.dirname(markdown_path))

            with open(
                markdown_path,
                "w",
                encoding="utf-8",
            ) as markdown_file:
                markdown_file.write(
                    "# Test Page\n\n"
                    "This is **bold** text."
                )

            with open(
                template_path,
                "w",
                encoding="utf-8",
            ) as template_file:
                template_file.write(
                    "<html>"
                    "<head><title>{{ Title }}</title></head>"
                    "<body>{{ Content }}</body>"
                    "</html>"
                )

            generate_page(
                markdown_path,
                template_path,
                destination_path,
            )

            with open(
                destination_path,
                "r",
                encoding="utf-8",
            ) as output_file:
                generated_html = output_file.read()

            self.assertEqual(
                generated_html,
                (
                    "<html>"
                    "<head><title>Test Page</title></head>"
                    "<body>"
                    "<div>"
                    "<h1>Test Page</h1>"
                    "<p>This is <b>bold</b> text.</p>"
                    "</div>"
                    "</body>"
                    "</html>"
                ),
            )

    def test_generate_page_creates_directories(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            markdown_path = os.path.join(
                temp_directory,
                "page.md",
            )
            template_path = os.path.join(
                temp_directory,
                "template.html",
            )
            destination_path = os.path.join(
                temp_directory,
                "nested",
                "public",
                "index.html",
            )

            with open(
                markdown_path,
                "w",
                encoding="utf-8",
            ) as markdown_file:
                markdown_file.write("# Page")

            with open(
                template_path,
                "w",
                encoding="utf-8",
            ) as template_file:
                template_file.write(
                    "<title>{{ Title }}</title>"
                    "{{ Content }}"
                )

            generate_page(
                markdown_path,
                template_path,
                destination_path,
            )

            self.assertTrue(
                os.path.isfile(destination_path)
            )


if __name__ == "__main__":
    unittest.main()