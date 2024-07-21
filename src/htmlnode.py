class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None): 
        self.tag = tag              #String representing tag name e.g. p, a, h1
        self.value = value          #String representing value of tag e.g. text inside paragraph
        self.children = children    #List of HTMLNode objects, representing the children of this node
        self.props = props if props is not None else {}         #Dictionary representing attributes of the tag, e.g. (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("This is a placeholder for the child classes")
    
    def props_to_html(self):
        string = ""
        for key, value in self.props.items():
            string += f' {key}="{value}"'
        return string


    def __repr__(self):
        return f"Tag={self.tag!r} Value={self.value!r} Children={self.children!r} Props={self.props!r}"

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

        