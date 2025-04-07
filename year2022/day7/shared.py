import re
from typing import NamedTuple


CD = re.compile(r'\$ cd (.*)')
LS = re.compile(r'\$ ls')
FILE_SIZE = re.compile(r'([0-9]*) (.*)')
DIR_NAME = re.compile(r'dir (.*)')


class File(NamedTuple):
    name: str
    size: int


class Directory:
    def __init__(self, name: str, parent: 'Directory | None'):
        self.name = name
        self.parent = parent
        self.files: dict[str, File] = {}
        self.directories: dict[str, Directory] = {}
        self._size: int | None = None

    def path(self) -> str:
        if self.parent is not None:
            return self.parent.path() + '/' + self.name
        return self.name
    
    def size(self) -> int:
        if self._size is None:
            self._size = sum(file.size for file in self.files.values()) + sum(directory.size() for directory in self.directories.values())
        return self._size
    

def parse_directory_tree(input: list[str]) -> Directory:
    assert input[0] == '$ cd /'
    root = Directory('', None)
    current_location = root
    i = 1
    while i < len(input):
        if match := CD.match(input[i]):
            name = match.group(1)
            if name == '..':
                if current_location.parent is None:
                    raise ValueError(f'Cannot go to parent of directory: {current_location}')
                current_location = current_location.parent
            elif name in current_location.directories:
                current_location = current_location.directories[name]
            else:
                new_dir = Directory(name, current_location)
                current_location.directories[name] = new_dir
                current_location = new_dir
            i += 1
        elif match := LS.match(input[i]):
            i += 1
            while i < len(input) and not input[i].startswith('$'):
                if match := FILE_SIZE.match(input[i]):
                    name = match.group(2)
                    size = int(match.group(1))
                    if name in current_location.files:
                        if size != current_location.files[name].size:
                            raise ValueError(f'Found file {name} with two different sizes: {size} != {current_location.files[name].size}')
                    else:
                        current_location.files[name] = File(name, size)
                elif match := DIR_NAME.match(input[i]):
                    name = match.group(1)
                    if name not in current_location.directories:
                        current_location.directories[name] = Directory(name, current_location)
                else:
                    raise ValueError(f'Failed to parse directory list: {input[i]}')
                i += 1
        else:
            raise ValueError(f'Failed to parse command line: {input[i]}')
    return root
