from htmlnode import HTMLNode, LeafNode, ParentNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:

    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    def __init__(self, value, text_type, url=None):
        self.value = value
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.value == other.value
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.value}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):

    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.value)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.value)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.value)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.value)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.value, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.value})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
