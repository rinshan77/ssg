import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()