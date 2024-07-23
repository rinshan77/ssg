class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def props_to_html(self):
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string

    def __repr__(self):
        return f"Tag={self.tag!r} Value={self.value!r} Children={self.children!r} Props={self.props!r}"

    def set_prop(self, key, value):
        self.props[key] = value

    def equals(self, other):
        if not isinstance(other, HTMLNode):
            return False
        if self.tag != other.tag:
            return False
        if self.props != other.props:
            return False
        if len(self.children) != len(other.children):
            return False
        for child, other_child in zip(self.children, other.children):
            if not child.equals(other_child):
                return False
        return True

    def to_html(self):
        raise NotImplementedError("This is a placeholder for the child classes")


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, [], props)

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("LeafNodes MUST have a value")
        if self.tag is None:
            return self.value
        if self.tag in ["img", "br"]:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.tag == "text":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, value=None, children=None, props=None):
        if children is None:
            children = []
        super().__init__(tag, value, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNodes MUST have a tag")
        if not self.children:
            raise ValueError("ParentNodes MUST have children")

        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
