import pickle
import csv
import sys

from Data.Trie import Trie

trie = Trie()

# Lesen der ersten 100 Einträge aus der CSV-Datei und Einfügen in den Trie
with open('wikipedia_titles.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    sys.setrecursionlimit(500000)  # Setzen Sie einen höheren Wert
    for i, row in enumerate(reader):
        if i >= 500000:
            break
        trie.insert(row[0])
        print(i)

with open('trie_data.pkl', 'wb') as output:
    pickle.dump(trie, output, pickle.HIGHEST_PROTOCOL)


