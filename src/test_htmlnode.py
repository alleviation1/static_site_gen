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
        self.assertEqual(node_props_text, ' href="https://www.google.com" target="_blank"')
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_values(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_tagless(self):
        node = LeafNode(None, "A leaf node", None)
        self.assertEqual(node.to_html(), "A leaf node")

    def test_leaf_to_html_with_props(self):
        node = LeafNode('a', 'google', {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">google</a>')


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

    def test_no_children_raises_value_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "span child")
        child_node2 = LeafNode("p", "paragraph child")
        child_node3 = LeafNode("a", "google", {"href": "https://www.google.com", "target": "_blank"})
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<div><span>span child</span><p>paragraph child</p><a href="https://www.google.com" target="_blank">google</a></div>')

    def test_to_html_with_nested_parent_nodes(self):
        child_node = LeafNode("p", "child node")
        nested_parent = ParentNode("div", [child_node], {"class": "nested"})
        parent_node = ParentNode("div", [nested_parent])
        self.assertEqual(parent_node.to_html(), '<div><div class="nested"><p>child node</p></div></div>')