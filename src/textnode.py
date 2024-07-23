from htmlnode import HTMLNode, LeafNode, ParentNode

class TextNode:
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    def __init__(self, value, text_type=None, url=None):
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
    if text_node.text_type == TextNode.text_type_text:
        return LeafNode("text", text_node.value)
    elif text_node.text_type == TextNode.text_type_bold:
        return LeafNode("strong", text_node.value)
    elif text_node.text_type == TextNode.text_type_italic:
        return LeafNode("em", text_node.value)
    elif text_node.text_type == TextNode.text_type_code:
        return LeafNode("code", text_node.value)
    elif text_node.text_type == TextNode.text_type_link:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("a", text_node.value, {"href": text_node.url})
    elif text_node.text_type == TextNode.text_type_image:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.value})
    else:
        raise ValueError(f"Unknown text type for {text_node.text_type}")
