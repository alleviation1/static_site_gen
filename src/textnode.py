from enum import Enum

class TextType(Enum):
    TEXT = "text",
    BOLD = "bold",
    ITALIC = "italic",
    CODE = 'code',
    LINK = 'link',
    IMAGE = 'image'

class TextNode:

    def __init__(self, text, text_type, url=None):
        self. text = text
        if not text_type in TextType:
            self.text_type = TextType.TEXT
            
        self. text_type = text_type
        self.url = url

    def __eq__(self, other_node):
            if not self.text == other_node.text:
                return False
            if not self.text_type == other_node.text_type:
                return False
            if not self.url == other_node.url:
                return False

            return True

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'