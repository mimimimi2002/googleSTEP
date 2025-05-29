class AnagramFinder:
  def __init__(self, dictionary):
    self.new_dictionary = {}
    self.create_new_dictionary(dictionary)

  def create_new_dictionary(self, dictionary):
    """
    Given a list of string, returns a dictionary of a sorted word as a key and the list of the origianl
    words as a value.
    Args:
        dictionary (list of string): a list of string that holds words in dictioanry.

    Returns:
        dictioanry: a dictionary of a sorted word as a key and the list of the origianl
                    words as a value.
    """
    self.new_dictionary = {}
    for word in dictionary:
      sorted_word = "".join(sorted(word))
      if sorted_word not in self.new_dictionary:
        self.new_dictionary[sorted_word] = []
      self.new_dictionary[sorted_word].append(word)


  def find_anagram(self, targeted_word):
    """
    This function returns a string of anagram of the tarted_word if it is in dictionary.
    Assume that this function is used in different targed_word in the same dictionary.
    If the target word has mutiple anagrams, returns a list of all anagrams.
    If the tarted_word is empty, returns 'Word is empty'.
    If the tarted_word does not have anagram that is in this dictionary, returns 'Cannot find the anagram of the word in the dictionary'.
    Args:
        targeted_word (string): the word that is needed to find its anagram.
        new_dictionary (dictionary): a dictionary of a sorted word as a key and the list of the origianl
                                    words as a value.
    Returns:
        string or list: a string of anagram of the tarted_word if it is in dictionary.
                        If the target word has mutiple anagrams, returns a list of all anagrams.
                        If the tarted_word is empty, returns 'Word is empty'.
                        If the tarted_word does not have anagram that is in this dictionary,
                        returns 'Cannot find the anagram of the word in the dictionary'.
    """

    # if the targeted word is empty
    if targeted_word == "":
      return 'Word is empty'

    # get a list of anagrams
    sorted_word = "".join(sorted(targeted_word))
    if sorted_word not in self.new_dictionary:
      return 'Cannot find the anagram of the word in the dictionary'
    anagrams = self.new_dictionary[sorted_word]

    if len(anagrams) == 1:
      return anagrams[0]
    else:
      return anagrams