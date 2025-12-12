import re

from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HtmlNode

valid_delimiters = [None, "**", "_", "`"]

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "ordered_list",

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        case TextType.BOLD:
            return LeafNode(tag='b', value=text_node.text, props=None)
        case TextType.ITALIC:
            return LeafNode(tag='i', value=text_node.text)
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
        return old_nodes
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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    html = []
    lines = markdown.split("\n\n")

    for line in lines:
        line = line.strip()
        if line:
            html.append(line)

    return html

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if not line:
            lines.remove(line)

    if lines[0].find("# ") != -1:
        return BlockType.HEADING

    elif (len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")) or lines[0].count("```") > 1:
        return BlockType.CODE

    elif lines[0].startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                raise Exception("Detected invalid quote syntax")
        return BlockType.QUOTE

    elif lines[0].startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                raise Exception("Detected invalid unordered list syntax")
        return BlockType.UNORDERED_LIST

    elif lines[0].startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                raise Exception("Detected invalid ordered list syntax")
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    html_nodes = []
    markdown_blocks = markdown_to_blocks(markdown)

    for block in markdown_blocks:
        html_children = []
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:
            children = text_to_textnodes(block)
            for child in children:
                child.text = child.text.replace("\n", " ")
                html_children.append(text_node_to_html_node(child))
        else:
            block = block.replace("```", "")
            lines = block.splitlines()
            new_lines = [line for line in lines if line.strip()]
            block = "\n".join(new_lines)
            block += "\n"
            child = TextNode(block, TextType.TEXT)
            html_children.append(text_node_to_html_node(child))



        match(block_type):
            case BlockType.HEADING:
                html_nodes.append(HtmlNode("header", None, html_children))
            case BlockType.CODE:
                html_nodes.append(HtmlNode("code", None, html_children))
            case BlockType.QUOTE:
                html_nodes.append(HtmlNode("q", None, html_children))
            case BlockType.UNORDERED_LIST: 
                html_nodes.append(HtmlNode("ul", None, html_children))
            case BlockType.ORDERED_LIST:
                html_nodes.append(HtmlNode("ol", None, html_children))
            case BlockType.PARAGRAPH:
                html_nodes.append(HtmlNode("p", None, html_children))
            case _:
                raise Exception("Error converting block type")
            
    return ParentNode("div", html_nodes)
# "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>
    # <p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
