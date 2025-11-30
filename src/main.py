from textnode import TextNode, TextType
from htmlnode import HtmlNode

def main():
    # node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    # print(node)

    child_node = HtmlNode('p', "some inner text", None, None)
    node_props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    node = HtmlNode(tag='a', value=None, children=None, props=node_props)
    node_repr = print(node)

main()