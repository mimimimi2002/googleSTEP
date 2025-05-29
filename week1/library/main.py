from importlib.resources import files
import anagramfinder

# Create instance from dictionary file

dict_path = files(anagramfinder).joinpath("words.txt")
finder = anagramfinder.AnagramFinder(str(dict_path))

# Find anagrams
print(finder.find_anagram("silent"))