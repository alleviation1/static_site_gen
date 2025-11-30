import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_params_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text, node2.text)
        self.assertEqual(node.text_type, node2.text_type)
        self.assertEqual(node.url, node2.url)


    def test_params_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.LINK, url="https://www.boot.dev")
        self.assertNotEqual(node.text, node2.text)
        self.assertNotEqual(node.text_type, node2.text_type)
        self.assertNotEqual(node.url, node2.url)

    def test_undef_text_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("some node text", TextType.NONEXISTENT)

    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.LINK, url="https://www.boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()


