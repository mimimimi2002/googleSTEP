def get_all_anagrams(sorted_new_dictionary, sorted_word, idx):
  """
  This function returns a list of string of all anagrams of
  the word that has the same sorted word as given sorted_word.

  Args:
      sorted_new_dictionary (list): this is a list of the tuple of the new dictionary that holds the sorted word and origianl word.
                                    this is already sorted by the first element of the tuple.
      sorted_word (string): a sorted word that you want to find all anagrams.
      idx (int): the index of the sorted word in the sorted_new_dictionary.
  """

  left = idx - 1
  right = idx + 1
  all_anagrams = []

  all_anagrams.append(sorted_new_dictionary[idx][1])

  while left >= 0 and sorted_new_dictionary[left][0] == sorted_word:
    all_anagrams.append(sorted_new_dictionary[left][1])
    left -= 1

  while right < len(sorted_new_dictionary) and sorted_new_dictionary[right][0] == sorted_word:
    all_anagrams.append(sorted_new_dictionary[right][1])
    right += 1

  return all_anagrams

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
      return get_all_anagrams(sorted_new_dictionary, sorted_word, mid)
    elif mid_word < sorted_word:
      left = mid + 1
    else:
      right = mid - 1

  return []

def find_anagram(tarted_word, sorted_new_dictionary):
  """
  This function returns the anagram of the tarted_word if it is in dictionary.
  Assume that this function is used in different targed_word in the same dictionary.
  If the tarted_word is empty, returns "word is empty".
  If the tarted_word does not have anagram that is in this dictionary, returns "Cannot find the anagram of the word in the dictionary".
  Args:
      targeted_word (string): the word that is needed to find its anagram.
      dictionary (a list of string): a list of string that represents a dictionary.
  """

  # if the targeted word is empty
  if tarted_word == "":
    return "Word is empty"

  # binary search
  sorted_word = "".join(sorted(tarted_word))
  anagrams = binary_serach(sorted_word, sorted_new_dictionary)

  if len(anagrams) == 0:
    return 'Cannot find the anagram of the word in the dictionary'
  elif len(anagrams) == 1:
    return anagrams[0]
  else:
    return anagrams

if __name__ == "__main__":
  dictionary = []
  with open("words.txt") as f:
    contents = f.readlines()
    for line in contents:
      dictionary.append(line.strip())

  new_dictionary = []
  for word in dictionary:
      new_dictionary.append(("".join(sorted(word)), word))

  # sort new dictionary
  sorted_new_dictionary = sorted(new_dictionary, key=lambda x:x[0])

  print(find_anagram("listen", sorted_new_dictionary))
