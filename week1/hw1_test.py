from homework1 import create_new_dictionary
from homework1 import find_anagram
from hw1_class import Anagram

def test_find_anagram():
  # test case 1 Basic test
  targeted_word = "acdr"
  dictioanry = ["egg", "card", "dog", "a"]
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == "card"

  # test case 2 If the anagram is not included in dictionary
  targeted_word = "zhegg"
  dictioanry = ["egg", "card", "dog", "a"]
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == "Cannot find the anagram of the word in the dictionary"

  # test case 3 if the targeted word is empty
  targeted_word = ""
  dictioanry = ["egg", "card", "dog", "a"]
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == "Word is empty"

  # test case 4 if the dictionary is empty
  targeted_word = "egg"
  dictioanry = []
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == "Cannot find the anagram of the word in the dictionary"

  # test case 5 if the word has multiple anagrams
  targeted_word = "ogd"
  dictioanry = ["egg", "card", "dog", "a", "god"]
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == ["dog", "god"]

  # test case 6 When the targeted_word is too long
  targeted_word = "".join(chr(c) for c in range(1000))
  dictioanry = ["egg", "card", "dog", "a", "god"]
  assert find_anagram(targeted_word, create_new_dictionary(dictioanry)) == "Cannot find the anagram of the word in the dictionary"

def test_find_anagram_using_class():
  anagram1 = Anagram(["egg", "card", "dog", "a"])
  assert anagram1.find_anagram("acdr") == "card"
  assert anagram1.find_anagram("zhegg") == "Cannot find the anagram of the word in the dictionary"
  assert anagram1.find_anagram("") == "Word is empty"

  anagram2 = Anagram([])
  assert anagram2.find_anagram("egg") == "Cannot find the anagram of the word in the dictionary"

  anagram3 = Anagram(["egg", "card", "dog", "a", "god"])
  assert anagram3.find_anagram("ogd") == ["dog", "god"]

if __name__ == "__main__":
  test_find_anagram()
  test_find_anagram_using_class()