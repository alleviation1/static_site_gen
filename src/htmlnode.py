class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise(NotImplementedError)

    def props_to_html(self):
        result = f''
        if self.props == None:
            return result

        for prop, prop_value in self.props.items():
            result += f' {prop}="{prop_value}"'

        return result

    
    def __repr__(self):
        return f"tag: '{self.tag}', value: {self.value}, children: {self.children}, props: {self.props}"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    
    def to_html(self):
        if not self.value:
            raise(ValueError)

        if not self.tag:
            return f"{self.value}"

        prop_string = f''
        if self.props:
            for prop, prop_value in self.props.items():
                prop_string += f' {prop}="{prop_value}"'

        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, props: {self.props}"


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if not self.tag:
            raise(ValueError)

        if not self.children:
            raise(ValueError(f"Parent has no children"))

        children_string = ""
        for child in self.children:
            children_string += child.to_html()

        prop_string = f''
        if self.props:
            for prop, prop_value in self.props.items():
                prop_string += f' {prop}="{prop_value}"'


        return f"<{self.tag}{prop_string}>{children_string}</{self.tag}>"


    def __repr__(self):
        return f"tag: {self.tag}, children: {self.children}, props: {self.props}"
        