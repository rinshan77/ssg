import unittest
from textnode import TextNode
from splitter import split_nodes_delimiter

import unittest


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(result, expected)

    def test_no_split(self):
        node = TextNode("This is plain text with no special code block", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [node]
        self.assertEqual(result, expected)

    def test_multiple_splits(self):
        node = TextNode("`code1` and `code2` are two code blocks", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("", "text"),
            TextNode("code1", "code"),
            TextNode(" and ", "text"),
            TextNode("code2", "code"),
            TextNode(" are two code blocks", "text"),
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is `unmatched code block", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", "code")

    def test_empty_text_node(self):
        node = TextNode("", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [TextNode("", "text")]
        self.assertEqual(result, expected)
        self.assertEqual(result, expected)

    def test_delimiter_at_edges(self):
        node = TextNode("`code at start` and `code at end`", "text")
        result = split_nodes_delimiter([node], "`", "code")
        expected = [
            TextNode("", "text"),
            TextNode("code at start", "code"),
            TextNode(" and ", "text"),
            TextNode("code at end", "code"),
            TextNode("", "text"),
        ]
        self.assertEqual(result, expected)

    def test_nested_delimiters(self):
        old_nodes = [TextNode("This is `code with `nested`` delimiters", "text")]
        delimiter = "`"

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, "code")

    def test_different_text_types(self):
        node1 = TextNode("`code block`", "text")
        node2 = TextNode("This is a bold text", "bold")
        result = split_nodes_delimiter([node1, node2], "`", "code")
        expected = [
            TextNode("", "text"),
            TextNode("code block", "code"),
            TextNode("", "text"),
            node2,
        ]
        self.assertEqual(result, expected)

    def test_complex_mixed_content(self):
        node1 = TextNode("This is `mixed` with `code`", "text")
        node2 = TextNode("and some `bold text`", "bold")
        result = split_nodes_delimiter([node1, node2], "`", "code")
        expected = [
            TextNode("This is ", "text"),
            TextNode("mixed", "code"),
            TextNode(" with ", "text"),
            TextNode("code", "code"),
            TextNode("", "text"),
            node2,
        ]
        self.assertEqual(result, expected)

    def test_only_delimiters(self):
        node = TextNode("``", "text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", "code")


if __name__ == "__main__":
    unittest.main()
