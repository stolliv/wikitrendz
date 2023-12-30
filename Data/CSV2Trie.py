import pickle
import csv
import sys

from Data.Trie import Trie

trie = Trie()

with open('../wiki_titles.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    sys.setrecursionlimit(4000000)
    for i, row in enumerate(reader):
        if i >= 4000000:
            break
        trie.insert(row[0])
        if i % 10000 == 0:
            print(i)

with open('4000_trie_data.pkl', 'wb') as output:
    pickle.dump(trie, output, pickle.HIGHEST_PROTOCOL)


