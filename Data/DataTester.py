import pickle
import time

start_time = time.time()

with open('trie_data.pkl', 'rb') as input:
    trie_loaded = pickle.load(input)

end_time = time.time()

print(end_time-start_time)


print(len(trie_loaded.search("")))
print(trie_loaded.search(""))