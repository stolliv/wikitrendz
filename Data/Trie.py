from Data.TrieNode import TrieNode


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, prefix, limit=10):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._find_words_from_node(node, prefix,limit)

    def _find_words_from_node(self, node, prefix, limit):
        words = []
        if len(words) < limit:
            if node.is_end_of_word:
                words.append(prefix)
            for char, next_node in node.children.items():
                words.extend(self._find_words_from_node(next_node, prefix + char, limit))
                if len(words) >= limit:
                    break
        return words[:limit]
