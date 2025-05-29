from homework2 import find_best_anagram
from homework2 import letter_word_score_by_score

letter_scores = {
      'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
      'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
      'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
      'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
  }

def test_find_anagram():
  # test case 1 Basic test
  targeted_word = "aakk"
  dictioanry = ["a", "ak", "akk", "qqq"] #a: 1, ak:5, akk:9, qqq:12

  assert find_best_anagram(targeted_word, letter_word_score_by_score(dictioanry)) == "akk", 9

  # test case 2 Basic test
  targeted_word = "aakk"
  dictioanry = ["qqq", "a", "ak", "akk"] #qqq:12, a: 1, ak:5, akk:9

  assert find_best_anagram(targeted_word, letter_word_score_by_score(dictioanry)) == "akk", 9

  # test case 3 if the targeted_word is empty
  targeted_word = ""
  dictioanry = ["qqq", "a", "ak", "akk"] #qqq:12, a: 1, ak:5, akk:9

  assert find_best_anagram(targeted_word, letter_word_score_by_score(dictioanry)) == "Word is empty"

  # test case 4 if cannot find the anagram
  targeted_word = "aakk"
  dictioanry = ["qqq", "vxx", "vz", "org"] #qqq:12, vxx: 11, vz:7, org:5

  assert find_best_anagram(targeted_word, letter_word_score_by_score(dictioanry)) == "", 0