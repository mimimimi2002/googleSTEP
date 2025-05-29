#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <chrono>
using namespace std;

class AnagramFinder {
    private:
        map<string, vector<string>> dictionary_map;
    public:

        AnagramFinder(vector<string> dictionary) {
        for (string word: dictionary) {
            string sorted_word = sort_word(word);
            dictionary_map[sorted_word].push_back(word);
        }
        }

        AnagramFinder(const string& filename) {
        load_dictionary(filename);
        }

        void load_dictionary(const string& filename) {
            ifstream file(filename);
            if (!file) {
                perror("cannot open the file");
                exit(1);
            }

            string word;
            while (getline(file, word)) {
                string sorted_word = sort_word(word);
                dictionary_map[sorted_word].push_back(word);
            }
            file.close();
        }

        string sort_word(const string& word) {
            string sorted = word;
            sort(sorted.begin(), sorted.end());
            return sorted;
        }

        vector<string> find_anagram(const string& target_word) {
            string sorted_target = sort_word(target_word);
            auto it = dictionary_map.find(sorted_target);
            if (it != dictionary_map.end()) {
                return it->second;
            } else {
                return {};
            }
        }
};

int main() {
  vector<string> test_words;
  ifstream file("random_words.txt");
  if (!file) {
      perror("cannot open the file");
      exit(1);
  }

  string word;
  while (getline(file, word)) {
      test_words.push_back(word);
  }
  file.close();

  vector<double> runtimes;

  for (string word: test_words) {

    auto start = std::chrono::high_resolution_clock::now();
    AnagramFinder anagramfinder = AnagramFinder("words.txt");
    vector<string> anagrams = anagramfinder.find_anagram(word);

    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> duration = end - start;

    for (string anagram: anagrams) {
        cout << anagram << endl;
    }

    std::cout << "Execution time: " << duration.count() << " seconds" << std::endl;
    runtimes.push_back(duration.count());

  }

  double total_runtime = 0.0;
  for (double r : runtimes) {
      total_runtime += r;
  }

  cout << "total runtime: " << total_runtime << endl;

}

