from pathlib import Path
from typing import Optional, Set, List
from dataclasses import dataclass

words = [
    line.strip().upper()
    for line in Path(Path(__file__).parent.resolve(), 'svnweb_words.txt').open().readlines()
    if not any(c.isupper() for c in line)
]

letters = [
    'RZE',
    'KTO',
    'UIW',
    'SHB',
]

side_map = {
    c: i
    for i, side in enumerate(letters)
    for c in side
}

def is_valid(word: str) -> bool:
    if not all(c in side_map for c in word):
        return False
    
    prev_side: Optional[int] = None

    for c in word:
        side = side_map[c]
        if side == prev_side:
            return False
        prev_side = side
    
    return True

@dataclass
class Word:
    word: str

    @property
    def start(self) -> str:
        return self.word[0]

    @property
    def end(self) -> str:
        return self.word[-1]

    @property
    def unique(self) -> Set[str]:
        return set(self.word)
    

valids: List[Word] = [
    Word(word)
    for word in words
    if is_valid(word)
]

start_map = {}
for word in valids:
    start_map.setdefault('', []).append(word)
    start_map.setdefault(word.start, []).append(word)

def explore(start: str, remaining: Set[str], visited: List[str], best_length: int) -> List[Word]:
    if len(visited) >= best_length:
        return []
    
    paths = []
    for word in sorted(start_map[start], key=lambda word: len(remaining - word.unique)):
        if word.word in visited:
            continue

        if len(remaining - word.unique) == len(remaining) and word.start == word.end:
            continue

        if len(remaining - word.unique) == 0:
            print(f'{" ".join(visited + [word.word])}\n')
            return [word]

        path: List[Word] = explore(word.end, remaining - word.unique, visited + [word.word], best_length=best_length)
        if not path:
            continue

        paths.append([word] + path)
        best_length = min(best_length, min(map(len, paths)))
    
    if not paths:
        return []
    
    return min(paths, key=len)

print(explore('', set(''.join(letters)), [], best_length=10))
