import unittest

from text_utilities import text_node_to_html_node, split_nodes_delimiter
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
        self.assertEqual(html_node.tag, 'em')
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
        node = TextNode("This is text with an __italic__ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
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
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "g", TextType.TEXT)

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