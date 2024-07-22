def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block).strip())

    return [block for block in blocks if block]


def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0].strip()

    if first_line.startswith("#"):
        count_hashes = 0
        for char in first_line:
            if char == "#":
                count_hashes += 1
            else:
                break
        if 1 <= count_hashes <= 6 and first_line[count_hashes] == " ":
            return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    if all(line.strip().startswith(">") for line in lines):
        return "quote"

    if all(
        line.strip().startswith(("*", "-")) and line.strip()[1] == " " for line in lines
    ):
        return "unordered_list"

    try:
        if all(
            line.strip().split(" ", 1)[0].rstrip(".").isdigit()
            and int(line.strip().split(" ", 1)[0].rstrip(".")) == i + 1
            for i, line in enumerate(lines)
        ):
            return "ordered_list"
    except (IndexError, ValueError):
        pass

    return "paragraph"

def create_html_node(block, block_type):
    if block_type.startswith('heading'):
        count_hashes = block.count('#', 0, block.index(' '))
        return HTMLNode(f'h{count_hashes}', [HTMLNode('text', [block.strip('# ').strip()])])
    elif block_type == 'code':
        code_content = block.strip('```')
        code_node = HTMLNode('code', [HTMLNode('text', [code_content])])
        return HTMLNode('pre', [code_node])
    elif block_type == 'quote':
        quote_content = block.strip('> ')
        return HTMLNode('blockquote', text_to_children(quote_content))
    elif block_type == 'unordered_list':
        items = block.split('\n')
        list_items = [
            HTMLNode('li', text_to_children(item.strip('*- '))) for item in items if item.strip()
        ]
        return HTMLNode('ul', list_items)
    elif block_type == 'ordered_list':
        items = block.split('\n')
        list_items = [
            HTMLNode('li', text_to_children(item.split(' ', 1)[1])) for item in items if item.strip()
        ]
        return HTMLNode('ol', list_items)
    elif block_type == 'paragraph':
        return HTMLNode('p', text_to_children(block))
    return HTMLNode('p', text_to_children(block))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = create_html_node(block, block_type)
        html_children.append(html_node)

    parent_node = HTMLNode('div', html_children)
    return parent_node
    