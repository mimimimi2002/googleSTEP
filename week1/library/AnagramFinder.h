#ifndef ANAGRAMFINDER_H
#define ANAGRAMFINDER_H

#include <string>
#include <vector>
#include <map>

class AnagramFinder {
private:
    std::map<std::string, std::vector<std::string>> dictionary_map;
    std::string sort_word(const std::string& word);
public:
    AnagramFinder(const std::vector<std::string>& dictionary);
    AnagramFinder(const std::string& filename);
    void load_dictionary(const std::string& filename);
    std::vector<std::string> find_anagram(const std::string& target_word);
};

#endif // ANAGRAMFINDER_H
