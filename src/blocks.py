def markdown_to_blocks(markdown):
    lines = markdown.split('\n')
    blocks = []
    current_block = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == '':
            if current_block:
                blocks.append('\n'.join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append('\n'.join(current_block).strip())

    return [block for block in blocks if block]

