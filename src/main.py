import os
import shutil

from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode
from text_utilities import (text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks,
markdown_to_html_node
)

def main():
    copy_files_recursive("static", "public")

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
    

main()
