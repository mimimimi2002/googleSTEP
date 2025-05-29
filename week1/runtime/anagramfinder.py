import time
import anagramfinder

test_words = []
with open("random_words.txt" ,'r') as f:
  content = f.readlines()
  for line in content:
    test_words.append(line.strip())

runtimes = []
for word in test_words:
  start = time.time()
  # Create instance from dictionary file
  finder = anagramfinder.AnagramFinder("words.txt")

  # Find anagrams
  print(finder.find_anagram(word))

  end = time.time()

  print(f"Elapsed time: {end - start:.6f} seconds")
  runtimes.append(end-start)

print("total runtime is :", sum(runtimes))