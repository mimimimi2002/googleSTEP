import anagramfinder
print(anagramfinder.__file__)

# Create instance from dictionary file
finder = anagramfinder.AnagramFinder("words.txt")

# Find anagrams
print(finder.find_anagram("silent"))
