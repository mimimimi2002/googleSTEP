import sys

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

def get_score(letter_word_pair):
  """
  Given a tuple of letter dictionary and the word,
  returns the word's score and the word.

  Args:
      letter_word_pair (tuple): a tuple of letter dictionary and the word.
      ex: ({"b": 1, "e": 2, "f": 1}, beef)
  """
  score = 0
  letter_scores = {
      'a': 1, 'e': 1, 'h': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1,
      'c': 2, 'd': 2, 'l': 2, 'm': 2, 'u': 2,
      'b': 3, 'f': 3, 'g': 3, 'p': 3, 'v': 3, 'w': 3, 'y': 3,
      'j': 4, 'k': 4, 'q': 4, 'x': 4, 'z': 4
  }
  for key, value in letter_word_pair[0].items():
    score += letter_scores[key] * value
  return letter_word_pair[1], score

def count_letter(word):
  """
  Given a string of word and returns a dictionary of its letters.

  Args:
      word (string): a string of word
  """
  letter_dict = {}
  for c in word:
      if c not in letter_dict:
          letter_dict[c] = 0
      letter_dict[c] += 1
  return letter_dict


def find_best_anagram(targeted_word, letter_word_dict_all):
  """
  Given a targeted word and a list of tuples of letter dictionary and word in the dictionary,
  find the anagrams that use the part of the word that is also in the dictionary.
  Then within the anagrams that are found, get the one that has the highest score.
  Returns the best anagram and its score.

  Args:
      targeted_word (string): a string of word
      letter_word_dict_all (list): a list of tuples of letter dictionary and word in the dictionary.
                                  ex: [({"b": 1, "e": 2, "f": 1}, beef) , ({"e": 1, "g": 2}, egg)]

  """
  answers = {}
  letter_target = count_letter(targeted_word)

  for letter_word_pair in letter_word_dict_all:

    # get the anagram and its socre
    if compare_two_dictionary(letter_target, letter_word_pair[0]):
      anagram, score = get_score(letter_word_pair)
      answers[anagram] = score

  # find the word that has highest score
  best_word = max(answers, key=answers.get)
  best_score = answers[best_word]
  return best_word, best_score

if __name__ == "__main__":

  # get all the words from words.txt
  dictionary = []
  with open("words.txt", 'r') as f:
    content = f.readlines()
    for line in content:
      dictionary.append(line.strip())

  # get the list of a pair of letter count and its original word from dictionary
  letter_word_dict_all = []
  for word in dictionary:
    letter_word_dict_all.append((count_letter(word), word))

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
      best_word, best_score = find_best_anagram(word, letter_word_dict_all)
      score_sum += best_score
      f.write(best_word)
      f.write("\n")

  print(score_sum)