import unittest
from htmlnode import HTMLNode
from blocks import markdown_to_blocks, block_to_block_type
from blocktohtml import (
    markdown_to_html_node,
    text_to_children,
    create_html_node,
    convert_bold_text,
    convert_italic_text,
    convert_link_text,
)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading 1"
        expected_html = HTMLNode(
            "div", [HTMLNode("h1", [HTMLNode("text", ["Heading 1"])])]
        )
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected_html)

    def test_link(self):
        markdown = "[Example](http://example.com)"
        expected_html = HTMLNode(
            "div",
            [
                HTMLNode(
                    "a",
                    [HTMLNode("text", ["Example"])],
                    props={"href": "http://example.com"},
                )
            ],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_paragraph_with_bold_and_italic(self):
        markdown = "This is **bold** and *italic* text."
        expected_html = HTMLNode(
            "div",
            [
                HTMLNode(
                    "p",
                    [
                        HTMLNode("text", ["This is "]),
                        HTMLNode("strong", [HTMLNode("text", ["bold"])]),
                        HTMLNode("text", [" and "]),
                        HTMLNode("em", [HTMLNode("text", ["italic"])]),
                        HTMLNode("text", [" text."]),
                    ],
                )
            ],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        expected_html = HTMLNode(
            "div",
            [
                HTMLNode(
                    "ul",
                    [
                        HTMLNode("li", [HTMLNode("text", ["Item 1"])]),
                        HTMLNode("li", [HTMLNode("text", ["Item 2"])]),
                        HTMLNode("li", [HTMLNode("text", ["Item 3"])]),
                    ],
                )
            ],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_ordered_list(self):
        markdown = "1. First Item\n2. Second Item\n3. Third Item"
        expected_html = HTMLNode(
            "div",
            [
                HTMLNode(
                    "ol",
                    [
                        HTMLNode("li", [HTMLNode("text", ["First Item"])]),
                        HTMLNode("li", [HTMLNode("text", ["Second Item"])]),
                        HTMLNode("li", [HTMLNode("text", ["Third Item"])]),
                    ],
                )
            ],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_blockquote(self):
        markdown = "> This is a quote."
        expected_html = HTMLNode(
            "div", [HTMLNode("blockquote", [HTMLNode("text", ["This is a quote."])])]
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_code_block(self):
        markdown = "```\ncode block\n```"
        expected_html = HTMLNode(
            "div",
            [HTMLNode("pre", [HTMLNode("code", [HTMLNode("text", ["code block"])])])],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))

    def test_mixed_content(self):
        markdown = "# Heading\nParagraph with **bold** and *italic* text.\n- List item"
        expected_html = HTMLNode(
            "div",
            [
                HTMLNode("h1", [HTMLNode("text", ["Heading"])]),
                HTMLNode(
                    "p",
                    [
                        HTMLNode("text", ["Paragraph with "]),
                        HTMLNode("strong", [HTMLNode("text", ["bold"])]),
                        HTMLNode("text", [" and "]),
                        HTMLNode("em", [HTMLNode("text", ["italic"])]),
                        HTMLNode("text", [" text."]),
                    ],
                ),
                HTMLNode("ul", [HTMLNode("li", [HTMLNode("text", ["List item"])])]),
            ],
        )
        result = markdown_to_html_node(markdown)
        self.assertTrue(result.equals(expected_html))


if __name__ == "__main__":
    unittest.main()
