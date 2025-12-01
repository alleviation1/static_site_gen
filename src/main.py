from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode

def main():
    node = TextNode('This is some text', TextType.TEXT)
    print(node)

    child_node = HtmlNode('p', "some inner text", None)
    node_props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return HtmlNode(tag=None, value=text_node.text, children=None, props=None)
        case TextType.BOLD:
            return HtmlNode(tag='b', value=text_node.text, props=None)
        case TextType.ITALIC:
            return HtmlNode(tag='em', value=text_node.text)
        case TextType.CODE:
            return HtmlNode(tag='code', value=text_node.text, children=None, props=None)
        case TextType.LINK:
            return HtmlNode(tag='a', value=text_node.text, children=None, props={"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return HtmlNode(tag='img', value="", children=None, props={"src": f"{text_node.url}", "alt": f"{text_node.text}"} if text_node.url else None)
        case _:
            raise Exception("Invalid Text Type")


main()