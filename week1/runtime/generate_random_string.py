import random
import nltk
nltk.download('words')
from nltk.corpus import words

def get_random_real_word():
    word_list = words.words()
    return random.choice(word_list)

print(get_random_real_word())

with open("random_words.txt", 'w') as f:
  for i in range(100):
    f.write(get_random_real_word().lower())
    f.write("\n")
