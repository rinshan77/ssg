import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a node", "bold")
        node2 = TextNode("This is a node", "italic")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Wah", "normal", "website.web")
        node2 = TextNode("Wah", "normal", "website.web")
        self.assertEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type_text(self):
        text_node = TextNode("some text", TextNode.text_type_text)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(value="some text")
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    def test_text_type_bold(self):
        text_node = TextNode("bold text", TextNode.text_type_bold)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="strong", value="bold text")
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    def test_text_type_italic(self):
        text_node = TextNode("italic text", TextNode.text_type_italic)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="em", value="italic text")
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    def test_text_type_code(self):
        text_node = TextNode("code sample", TextNode.text_type_code)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(tag="code", value="code sample")
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    def test_text_type_link(self):
        text_node = TextNode(
            "click here", TextNode.text_type_link, url="http://example.com"
        )
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(
            tag="a", value="click here", props={"href": "http://example.com"}
        )
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    def test_text_type_image(self):
        text_node = TextNode(
            "image description",
            TextNode.text_type_image,
            url="http://example.com/image.png",
        )
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(
            tag="img",
            value="",
            props={"src": "http://example.com/image.png", "alt": "image description"},
        )
        print(html_node)
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())


if __name__ == "__main__":
    unittest.main()
