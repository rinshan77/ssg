from textnode import TextNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.value.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.value)
        if not images:
            new_nodes.append(node)
            continue
        current_text = node.value
        for alt_text, url in images:
            before, sep, after = current_text.partition(f"![{alt_text}]({url})")
            if before:
                new_nodes.append(TextNode(before, node.text_type))
            new_nodes.append(TextNode(alt_text, "image", url))
            current_text = after

        if current_text:
            new_nodes.append(TextNode(current_text, node.text_type))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.value)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.value
        for link_text, url in links:
            before, sep, after = current_text.partition(f"[{link_text}]({url})")
            if before:
                new_nodes.append(TextNode(before, node.text_type))
            new_nodes.append(TextNode(link_text, "link", url))
            current_text = after

        if current_text:
            new_nodes.append(TextNode(current_text, node.text_type))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")

    return nodes
