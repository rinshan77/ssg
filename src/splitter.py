from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, provided_text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        parts = node.value.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("Unmatched delimiter detected!")

        for i, part in enumerate(parts):
            if part == "" and i % 2 == 1:
                raise ValueError("Empty text node detected!")
            text_type = provided_text_type if i % 2 == 1 else "text"
            new_nodes.append(TextNode(part, text_type))

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
