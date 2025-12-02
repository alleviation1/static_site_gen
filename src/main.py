from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode
from text_utilities import text_node_to_html_node, split_nodes_delimiter

def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)


main()