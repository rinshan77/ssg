from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("a", "b", "c", "d")
        print(node)

    def test_repr(self):
        node = HTMLNode(
            "a", "This is text", ["child1", "child2"], {"href": "link", "style": "cool"}
        )
        repr_str = node.__repr__()
        expected_str = "Tag='a' Value='This is text' Children=['child1', 'child2'] Props={'href': 'link', 'style': 'cool'}"
        self.assertEqual(repr_str, expected_str)

    def test_props_to_html(self):
        node = HTMLNode(
            "a", "This is text", ["child1", "child2"], {"href": "link", "style": "cool"}
        )
        node2 = HTMLNode(
            props={"href": "link", "style": "cool", "attri": "whatever", "key": "value"}
        )
        print(node.props_to_html())
        print(node2.props_to_html())


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode("img", "Yooo!", {"src": "https://www.google.com"})
        print(node.to_html())
        print(node2.to_html())
        print(node3.to_html())


class TestParentNode(unittest.TestCase):
    def test_parent_node_with_children(self):
        leaf1 = LeafNode(tag="span", value="Child 1", props={"class": "text-bold"})
        leaf2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[leaf1, leaf2], props={"id": "parent"})

        expected_html = '<div id="parent"><span class="text-bold">Child 1</span><span>Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_parent_node_without_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(
                tag=None, children=[LeafNode(tag="span", value="Child")]
            ).to_html()
        self.assertEqual(str(context.exception), "ParentNodes MUST have a tag")

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag="div", children=[]).to_html()
        self.assertEqual(str(context.exception), "ParentNodes MUST have children")

    def test_recursive_parent_node(self):
        leaf1 = LeafNode(tag="span", value="Child 1", props={"class": "text-bold"})
        leaf2 = LeafNode(tag="span", value="Child 2")
        inner_parent = ParentNode(tag="section", children=[leaf1, leaf2])
        outer_parent = ParentNode(
            tag="div", children=[inner_parent], props={"id": "outer-parent"}
        )

        expected_html = '<div id="outer-parent"><section><span class="text-bold">Child 1</span><span>Child 2</span></section></div>'
        self.assertEqual(outer_parent.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
