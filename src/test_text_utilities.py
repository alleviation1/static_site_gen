import unittest

from text_utilities import (text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, markdown_to_blocks,
 split_nodes_image, split_nodes_link, text_to_textnodes, block_to_block_type, BlockType, markdown_to_html_node
)
from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode

class TestTextUtilities(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italics(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props['href'], "https://www.google.com")

    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], "https://www.google.com")
        self.assertEqual(html_node.props['alt'], "This is an image text node")

    def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_delimiter_text(self):
        node = TextNode("This is text with text type", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text with text type")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_delimiter_with_invalid_delimiter(self):
        node = TextNode("This is text with text type", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "g", TextType.TEXT)
        self.assertListEqual(new_nodes, [node])

    def test_split_delimiter_with_invalid_text_type(self):
        node = TextNode("This is text with text type", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], None, TextType.IMAGE)

    def test_split_delimiter_without_nodes(self):
        self.assertEqual(split_nodes_delimiter([], None, TextType.TEXT), [])

    def test_split_delimiter_with_uneven_delimiters(self):
        node = TextNode("This is text with text type with **uneven bold delimiters", TextType.BOLD)
        with self.assertRaises(Exception):
            self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(result[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_extract_markdown_images_without_image_syntax(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(result[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))

    def test_extract_markdown_links_without_link_syntax(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = """




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    def test_markdown_to_blocks_multiple_new_line_chars(self):
        md = """
\n\n\nsome text

\n\n\n more text  
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "some text",
                "more text",
            ]
        )

    def test_markdown_to_blocks_leading_empty_space(self):
        md = """
            some text

            more text  
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "some text",
                "more text",
            ]
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("""##### some heading"""), BlockType.HEADING)
        self.assertEqual(block_to_block_type("""``` some code ```"""), BlockType.CODE)
        self.assertEqual(block_to_block_type("""> a quote"""), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("""- some unordered list"""), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("""1. some ordered list"""), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("""a regular paragraph"""), BlockType.PARAGRAPH)

    def test_block_to_block_type_multiple_lined_quotes_and_lists(self):
        self.assertEqual(block_to_block_type("""
> some quote
> using more than
> one line
"""
        ), BlockType.QUOTE)

        self.assertEqual(block_to_block_type("""
- some unordered list
- with multiple
- lines of items
"""
        ), BlockType.UNORDERED_LIST)

        self.assertEqual(block_to_block_type("""
1. some ordered list
2. with multiple
3. lines of items
"""
        ), BlockType.ORDERED_LIST)


    def test_block_to_block_type_multiple_lined_quotes_and_lists_fails_bad_syntax(self):
        with self.assertRaises(Exception) as cm:
            block_to_block_type("""
> some quote
> using more than
one line
"""
            )
            self.assertEqual(cm.exception.args[0], "Detected invalid quote syntax")

        with self.assertRaises(Exception) as cm:
            block_to_block_type("""
- some unordered list
- with multiple
lines of items
"""
        )
        self.assertEqual(cm.exception.args[0], "Detected invalid unordered list syntax")

        with self.assertRaises(Exception) as cm:
            block_to_block_type("""
1. some ordered list
2. with multiple
lines of items
"""
        )
        self.assertEqual(cm.exception.args[0], "Detected invalid ordered list syntax")


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )