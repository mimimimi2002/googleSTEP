import time
import anagramfinder
from importlib.resources import files

test_words = []
with open("random_words.txt" ,'r') as f:
  content = f.readlines()
  for line in content:
    test_words.append(line.strip())

runtimes = []
for word in test_words:
  start = time.time()
  # Create instance from dictionary file
  dict_path = files(anagramfinder).joinpath("words.txt")
  finder = anagramfinder.AnagramFinder(str(dict_path))

  # Find anagrams
  print(finder.find_anagram(word))

  end = time.time()

  print(f"Elapsed time: {end - start:.6f} seconds")
  runtimes.append(end-start)

print("total runtime is :", sum(runtimes))