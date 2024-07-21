class TextNode():
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
        return (
            self.value == other.value and
            self.text_type == other.text_type and
            self.url == other.url
        )
    def __repr__(self):
        return f"TextNode({self.value}, {self.text_type}, {self.url})"
    

def text_node_to_html_node(text_node):
    from htmlnode import LeafNode

    if text_node.text_type == TextNode.text_type_text:
        return LeafNode(value=text_node.value)
    elif text_node.text_type == TextNode.text_type_bold:
        return LeafNode(tag="b", value=text_node.value)
    elif text_node.text_type == TextNode.text_type_italic:
        return LeafNode(tag="i", value=text_node.value)
    elif text_node.text_type == TextNode.text_type_code:
        return LeafNode(tag="code", value=text_node.value)
    elif text_node.text_type == TextNode.text_type_link:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode(tag="a", value=text_node.value, props={"href": text_node.url})
    elif text_node.text_type == TextNode.text_type_image:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.value})
    else:
        raise ValueError(f"Unknown text type for {text.node.text_type}")
    
