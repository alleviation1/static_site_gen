from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode

valid_delimiters = [None, "**", "__", "`"]

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag='em', value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag='code', value=text_node.text, props=None)
        case TextType.LINK:
            return LeafNode(tag='a', value=text_node.text, props={"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode(tag='img', value="", props={"src": f"{text_node.url}", "alt": f"{text_node.text}"} if text_node.url else None)
        case _:
            raise Exception("Invalid Text Type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not delimiter in valid_delimiters:
        raise Exception("Invalid delimiter")
    if not old_nodes:
        return []
    if not text_type in TextType:
        raise Exception("Invalid text type")

    new_nodes = []
    for old_node in old_nodes:
        delim_count = old_node.text.count(delimiter)

        sub_nodes = []
        if delim_count == 1:
            raise Exception("Invalid syntax, single delimiter")
        if delim_count >= 2 and text_type is not None:
            sub_node_texts = old_node.text.split(delimiter, maxsplit=2)
            sub_nodes.append(TextNode(sub_node_texts[0], TextType.TEXT))
            sub_nodes.append(TextNode(sub_node_texts[1], text_type))
            sub_nodes.append(TextNode(sub_node_texts[2], TextType.TEXT))

            new_nodes.extend(split_nodes_delimiter(sub_nodes, delimiter, text_type))

        else:
            new_nodes.append(old_node)

    return new_nodes