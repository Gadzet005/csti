def normalizeText(text: str) -> str:
    """ Убирает лишние пробелы и пустые строки """

    lines = text.split('\n')
    lines = map(
        lambda line: " ".join(filter(lambda x: x != "", line.split(' '))), 
        lines
    )
    lines = filter(lambda x: x != "", lines)

    return '\n'.join(lines)
