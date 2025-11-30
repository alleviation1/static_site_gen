import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_html_node_init(self):
        child_node = HtmlNode('p', "some inner text", None, None)
        node_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HtmlNode(tag='a', value=None, children=child_node, props=node_props)
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, child_node)
        self.assertEqual(node.props, node_props)


    def test_html_init_None(self):
        node = HtmlNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_html_props_to_html(self):
        child_node = HtmlNode('p', "some inner text", None, None)
        node_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HtmlNode(tag='a', value=None, children=child_node, props=node_props)
        node_props_text = node.props_to_html()
        self.assertEqual(node_props_text, ' href: "https://www.google.com" target: "_blank"')
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_values(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props_to_html(), ' href: "https://www.google.com" target: "_blank"')

    def test_leaf_to_html_tagless(self):
        node = LeafNode(None, "A leaf node", None)
        self.assertEqual(node.to_html(), "A leaf node")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )