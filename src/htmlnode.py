class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 


    def __repr__(self):
        return f"Tag={self.tag!r} Value={self.value!r} Children={self.children!r} Props={self.props!r}"

    def set_prop(self, key, value):
        self.props[key] = value

    def to_html(self):
        raise NotImplementedError("This is a placeholder for the child classes")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNodes MUST have a value")
        if self.tag is None:
            return self.value
        if self.tag in ["img", "br"]:
            return f"<{self.tag}{self.props_to_html()} />"
        if self.tag == "text":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNodes MUST have a tag")
        if not self.children:
            raise ValueError("ParentNodes MUST have children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"