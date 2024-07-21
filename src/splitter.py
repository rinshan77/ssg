from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        parts = node.value.split(delimiter)

        # Check for unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError("Unmatched delimiter detected!")

        for i, part in enumerate(parts):
            if part == "" and i % 2 == 1:
                raise ValueError("Empty text node detected!")
            text_type = "code" if i % 2 == 1 else "text"
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
            # Append the text before the image, if it's not empty
            if before:
                new_nodes.append(TextNode(before, node.text_type))
            # Append the image as a new TextNode
            new_nodes.append(TextNode(alt_text, "text_type_image", url))
            # Continue with the text after the image
            current_text = after

        # Append any remaining text after the last image, if it's not empty
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
            new_nodes.append(TextNode(link_text, "text_type_link", url))
            current_text = after

        if current_text:
            new_nodes.append(TextNode(current_text, node.text_type))
    return new_nodes

# Example usage for split_nodes_link

text_with_links = (
    "This is text with a link [to boot dev](https://www.boot.dev) "
    "and [to youtube](https://www.youtube.com/@bootdotdev)"
)
node_with_links = TextNode(text_with_links, "text_type_text")

# Initial node list
old_nodes = [node_with_links]

# Using the split_nodes_link function
new_nodes = split_nodes_link(old_nodes)

# Printing the result
print(new_nodes)

# Example usage for split_nodes_image

text_with_images = (
    "This is text with an image ![example1](http://example.com/image1.png)"
    " and another image ![example2](http://example.com/image2.png)"
)
node_with_images = TextNode(text_with_images, "text_type_text")

# Initial node list
old_nodes = [node_with_images]

# Using the split_nodes_image function
new_nodes = split_nodes_image(old_nodes)

# Printing the result
print(new_nodes)

