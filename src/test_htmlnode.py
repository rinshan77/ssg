from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    
    def test_print(self):
        node = HTMLNode("a", "b", "c", "d")
        print(node)

    def test_repr(self):
        node = HTMLNode("a", "This is text", ["child1", "child2"], {"href": "link", "style": "cool"})
        repr_str = node.__repr__()
        expected_str = "Tag='a' Value='This is text' Children=['child1', 'child2'] Props={'href': 'link', 'style': 'cool'}"
        self.assertEqual(repr_str, expected_str)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is text", ["child1", "child2"], {"href": "link", "style": "cool"})
        node2 = HTMLNode(props={"href": "link", "style": "cool", "attri": "whatever", "key": "value"})
        print(node.props_to_html())
        print(node2.props_to_html())

