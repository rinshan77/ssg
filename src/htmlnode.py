class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None): 
        self.tag = tag              #String representing tag name e.g. p, a, h1
        self.value = value          #String representing value of tag e.g. text inside paragraph
        self.children = children    #List of HTMLNode objects, representing the children of this node
        self.props = props          #Dictionary representing attributes of the tag, e.g. (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("This is a placeholder for the child classes")
    
    def props_to_html(self):
        string = ""
        for key, value in self.props.items():
            string += f" {key}={value}"
        return string

    def __repr__(self):
        return f"Tag={self.tag!r} Value={self.value!r} Children={self.children!r} Props={self.props!r}"