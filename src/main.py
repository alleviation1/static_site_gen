import os
import sys
import shutil

from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode
from text_utilities import (text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, text_to_textnodes, markdown_to_blocks,
markdown_to_html_node, extract_title
)

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(basepath)

    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    copy_files_recursive(dir_path_static, dir_path_docs)
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_docs, "index.html"),
        basepath
    )
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)

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

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(os.path.abspath(from_path)):
        raise Exception(f"From path: {os.path.abspath(from_path)} does not exist.")

    if not os.path.exists(os.path.abspath(template_path)):
        raise Exception(f"Template path: {os.path.abspath(template_path)} does not exist.")


    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(os.path.abspath(from_path), 'r', encoding='utf-8') as markdown_file:
            markdown = markdown_file.read()
    except Exception as e:
        print(e)

    try:
        with open(os.path.abspath(template_path), 'r', encoding='utf-8') as template_file:
            template = template_file.read()
    except Exception as e:
        print(e)
    
    title = extract_title(markdown)
    markdown_html = markdown_to_html_node(markdown)
    markdown_html = markdown_html.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", markdown_html)
    tempalte = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    curr_dir = os.path.abspath(".")
    dest_sub_dirs = dest_path.split("/")
    dest_file = dest_sub_dirs[-1]
    dest_sub_dirs = dest_sub_dirs[:-1]
    dest = curr_dir
    
    for sub_path in dest_sub_dirs:
        dest = os.path.join(dest, sub_path)
        if not os.path.exists(dest):
            os.mkdir(dest)

    try:
        with open(os.path.abspath(dest_path), 'w', encoding='utf-8') as html_file:
            html_file.write(template)
    except Exception as e:
            print(e)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for dir in os.listdir(dir_path_content):

        if dir.find(".md") != -1:

            generate_page(
                os.path.join(os.path.join(dir_path_content, dir)),
                template_path,
                os.path.join(os.path.join(dest_dir_path, "index.html")),
                basepath
            )

        elif not os.path.isfile(dir):
            generate_pages_recursive(
                os.path.join(dir_path_content, dir),
                template_path,
                os.path.join(dest_dir_path, dir),
                basepath)
        


main()
