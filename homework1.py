# global variable to keep track whether the dictionary is already sorted.
sorted_new_dictionary_store = {}

def binary_serach(sorted_word, sorted_new_dictionary):
  """
  This function does binary search on the sorted word in new dictionary.
  This function searches the sorted word on the first element of the tuple in new dictioanry.
  Returns the origianl word if its anagram is in the sorted new dictionary.
  If it cannot find the anagram from the dictionary, they will return empty string.
  Args:
      sorted_word (string): this is the sorted word that you want to search from sorted_new_dictionary
      sorted_new_dictionary (list): this is a list of the tuple of the new dictionary that holds the sorted word and origianl word.
                                    this is already sorted by the first element of the tuple.
  """
  left = 0
  right = len(sorted_new_dictionary) - 1
  mid_word = ""

  # binary serach
  while left <= right:

    # prevent overflowing
    mid = int(left + (right - left) / 2)
    mid_word = sorted_new_dictionary[mid][0]

    # if find the right sorted word, return the pair of the original word
    # it does not matter which word will return as long as the sorted word matches the word in the new dict
    if mid_word == sorted_word:
      return sorted_new_dictionary[mid][1]
    elif mid_word < sorted_word:
      left = mid + 1
    else:
      right = mid - 1

  return ""

sorted_new_dictionary = []
def find_anagram(tarted_word, dictionary):
  """
  This function returns the anagram of the tarted_word if it is in dictionary.
  Assume that this function is used in different targed_word in the same dictionary.
  If the tarted_word is empty, returns "word is empty".
  If the tarted_word does not have anagram that is in this dictionary, returns "Cannot find the anagram of the word in the dictionary".
  Args:
      targeted_word (string): the word that is needed to find its anagram.
      dictionary (a list of string): a list of string that represents a dictionary.
  """

  # declare the stored new_dictionary as a global function
  global sorted_new_dictionary_store
  # if the targeted word is empty
  if tarted_word == "":
    return "Word is empty"

  # create a new dictionary that holds a list of tuple of sorted word and the original word in dictioanry.
  # if the dictionary is already sorted, not necessary
  if len(sorted_new_dictionary_store) == 0:
    new_dictionary = []
    for word in dictionary:
      new_dictionary.append(("".join(sorted(word)), word))

    # sort new dictionary
    sorted_new_dictionary = sorted(new_dictionary, key=lambda x:x[0])

    sorted_new_dictionary_store = sorted_new_dictionary

  # binary search
  sorted_word = "".join(sorted(tarted_word))
  anagram = binary_serach(sorted_word, sorted_new_dictionary_store)

  if anagram == "":
    return 'Cannot find the anagram of the word in the dictionary'
  else:
    return anagram

if __name__ == "__main__":
  # test
  assert find_anagram("", ["egg", "a", "bark", "card", "dog"]) == "Word is empty"
  assert find_anagram("acdr", ["egg", "a", "bark", "card", "dog"]) == "card"
  assert find_anagram("abcr", ["egg", "a", "bark", "card", "dog"]) == "Cannot find the anagram of the word in the dictionary"

  sorted_new_dictionary_store = {}
  dictionary = []
  with open("words.txt") as f:
    contents = f.readlines()
    for line in contents:
      dictionary.append(line.strip())
  print(find_anagram("otcopus", dictionary))
