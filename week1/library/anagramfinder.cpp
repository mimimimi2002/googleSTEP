#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
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

namespace py = pybind11;

PYBIND11_MODULE(anagramfinder, m) {
    py::class_<AnagramFinder>(m, "AnagramFinder")
        .def(py::init<std::vector<std::string>>())
        .def(py::init<const std::string&>())
        .def("find_anagram", &AnagramFinder::find_anagram);
}

