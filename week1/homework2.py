import sys

def letter_word_score_by_score(dictionary):
  """
  Given a list of string of dictionary and returns a list of tuples that hold letter_dictionary, original_word, score.
  Then sorted by the score in descending order.
  Args:
      dictionary (list): a list of string of dictionary

  Returns:
      list: a list of tuples that hold letter_dictionary, original_word, score sorted by score in descending order.
  """
  # get the list of a pair of letter count and its original word from dictionary
  letter_word_score_all = []
  for word in dictionary:
    letter_dict = count_letter(word)
    letter_word_score_all.append((letter_dict, word, get_score(letter_dict)))

  # sort by score
  return sorted(letter_word_score_all, key=lambda x:x[2], reverse=True)

def compare_two_dictionary(dict1, dict2):
  """
  This is the function that returns true if dict2 is a subset of dict1.
  If not, returns false.

  Args:
      dict1 (dict): a dictionary that holds letters as keys and number of the letters as values.
      dict2 (dict): a dictionary that holds letters as keys and number of the letters as values.
      ex: {"b": 1, "e": 2, "f": 1}
  """
  if len(dict1) < len(dict2):
    return False

  for k, v in dict2.items():
    if k not in dict1 or dict1[k] < v:
      return False
  return True

def get_score(letter_dict):
  """
  Given a letter dictionary, returns its score.

  Args:
      letter_dict (dictioanry): a dictionary of letters.
      ex: {"b": 1, "e": 2, "f": 1}

  Returns:
      int: a int of the score
  """
  score = 0
  letter_scores = {
      'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
      'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
      'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
      'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
  }
  for key, value in letter_dict.items():
    score += letter_scores[key] * value
  return score

def count_letter(word):
  """
  Given a string of word and returns a dictionary of its letters.

  Args:
      word (string): a string of word

  Returns:
      dictionary: a dictionary of letters that make up the word.
      ex: {"b": 1, "e": 2, "f": 1}
  """
  letter_dict = {}
  for c in word:
      if c not in letter_dict:
          letter_dict[c] = 0
      letter_dict[c] += 1
  return letter_dict


def find_best_anagram(targeted_word, letter_word_score_all_by_score):
  """
  Given a targeted word and a list of tuples of letter dictionary and word in the dictionary,
  find the anagrams that use the part of the word that is also in the dictionary.
  Then within the anagrams that are found, get the one that has the highest score.
  Returns the best anagram and its score.
  If there is no matching anagram, return "", and 0

  Args:
      targeted_word (string): a string of word
      letter_word_score_all_by_score (list): a list of tuples of letter dictionary and word and its score in the dictionary.
                                  ex: [({"b": 1, "e": 2, "f": 1}, beef, 9) , ({"e": 1, "g": 2}, egg, 6)]

  Returns:
      str, int: the best anagram and its score. If there is no matching anagram, return "", and 0

  """
  letter_target = count_letter(targeted_word)

  for letter_word_score_pair in letter_word_score_all_by_score:

    # get the best anagram and its socre
    if compare_two_dictionary(letter_target, letter_word_score_pair[0]):
      best_word = letter_word_score_pair[1]
      best_score = letter_word_score_pair[2]
      return best_word, best_score

  return "", 0

if __name__ == "__main__":

  # get all the words from words.txt
  dictionary = []
  with open("words.txt", 'r') as f:
    content = f.readlines()
    for line in content:
      dictionary.append(line.strip())

  # get the list of a pair of letter count and its original word from dictionary
  letter_word_score_all_by_score = letter_word_score_by_score(dictionary)

  target_file = sys.argv[1]
  answer_file = sys.argv[2]

  targeted_words = []
  with open(target_file, 'r') as f:
    content = f.readlines()
    for line in content:
      targeted_words.append(line.strip())

  score_sum = 0
  with open(answer_file, 'w') as f:
    for word in targeted_words:
      best_word, best_score = find_best_anagram(word, letter_word_score_all_by_score)
      score_sum += best_score
      f.write(best_word)
      f.write("\n")

  print(score_sum)