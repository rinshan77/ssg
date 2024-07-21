from textnode import TextNode


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
