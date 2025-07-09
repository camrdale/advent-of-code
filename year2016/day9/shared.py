import re


MARKER = re.compile(r'\(([0-9]*)x([0-9]*)\)')


def decompressed_length(text: str, recursive: bool = False) -> int:
    start = 0
    length = 0
    while marker := MARKER.search(text, start):
        length += marker.start() - start
        section_length = int(marker.group(1))
        section_repeats = int(marker.group(2))
        start = marker.end() + section_length
        if recursive:
            section = text[marker.end():marker.end()+section_length]
            section_length = decompressed_length(section, recursive=recursive)
        length += section_length * section_repeats
    
    length += len(text) - start

    return length
