# googleSTEP

## homework1
### runtime
Given the target_word and dictionary, find the anagram of the target_word in dictionary.

M: target_word's length

N: dictionary's length

Q: how many times they search the anagram of different words in the dictionary.

L: the length of the longest word in dictionary

In a greedy way, we rearrange the target_word(O(M!)) and then comapre with all the words in dictionary.
If we do Q times, the runtime will be

O(Q * M! * N).

Assume that N has a large number, we can decrease the runtime.

Next, if we can sort the dictionary(O(N * logN)) we can do binary search to find the anagram.
Moreover, considering that we only sort the dictionary once, the runtime will be

O(N * logN + Q * M! * logN).

We cannot conclude that this is faster than the greedy way, but based on how many
times you request and the length of the target_word, this will be faster.

Finally, to make it even faster, we pay attention the fact that we need to rearrange the target_word.
Considering that anagram means they have the same component and if they are sorted,
if we sort the each word in dictionary and the target_word is also sorted, it is not needed to be rearranged.

To take this way, we first sort the each word in the dictionary but still need to store the original word,
we will make a pair of (sorted_word, origianl_word) for each of the word in dict.(N * L * logL) This process is only done once.

Then sort the dictionary again by sorted_word. (N * logN)
Then sort the target_word. (M * logM)
Then use the binary search to find the same sorted_word as the sorted target_word. (logN)

So the total runtime will be

O(N * L * logL + N * logN + Q * M * logM * logN)

### more effective way
We created a sorted new dictionary, but if you want to find the sorted_word and get the origianl word,
store them in dictionary and use O(1) to find the correspoinding origianl word.
In this way, we don't need to do binary search.

### test
We will test in the small dictionary whose length is less than 10.
However, this function is assuming that you use the same dictionary and they will only sort the
dictionary once.

We will create a new class that can test the different dictionary and also sort it once no
matter how many request you do.

## homework2
### runtime
This time, we will use a part of the letters in the targeted_word and find the anagram that has the highest score.
Fisrt we can make use of the homework1's algorithm.

We need to get all the subset of the targeted word.(O(2^M)).
Then do the same thing as the algorithm1.

The runtime will be
O(N * L * logL + N * logN + Q * 2^M * M * logM * logN)

Considering that anagrams can be created as long as the targeted_word has enough letters.
So this time, we will use the letters dictionary for both targeted_word and words in dictionary.

First, we create a pair of letters dictionary and the original word for each word in dictionary.(O(L * N))

We create a dictionary for the letters in targeted_word(O(M))

Then we will compare the letters in targeted_word and each word in dictionary and check if it is a subset of the targeted_word. If so, we will get the score and store to list. (O(M * N))

After getting the all possible anagrams and their score, choose the best anagram and its score.
(O(length_longest_possible_anagram))

The total runtime will be

O(L * N + Q * (M + M * N + length_longest_possible_anagram))

### more efficient way
Is it necessary to hold all the possible anagrams to get the highest score?

If the dictionary is sorted by score, the first anagrams we find is guaranteed to have
the highest score.

the runtime will be

O(L * N + N * logN + Q * (M + M * (the times to find the highest score(most is way less than N))))

## library
Considering that c++ or c language runs faster than python, we created a library that can be
imported by python file and compare runtime for this.

### To make it a library
1. use c++ to write the hw1 using class.

2. add code in cpp file.
```
PYBIND11_MODULE(anagramfinder, m) {
    py::class_<AnagramFinder>(m, "AnagramFinder")
        .def(py::init<std::vector<std::string>>())
        .def(py::init<const std::string&>())
        .def("find_anagram", &AnagramFinder::find_anagram);
}
```

3. create setup.py
```
ext_modules = [
    Extension(
        "anagramfinder",
        ["anagramfinder.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
        extra_compile_args=['-std=c++11'],
    ),
]

setup(
    name="anagramfinder",
    version="0.1",
    ext_modules=ext_modules,
)
```

4. `pip install -e .`

5. `python setup.py build`

6. `python setup.py install`

7. then be able to use import anagramfinder in main.py

### C++ vs python
コンパイル言語 vs インタプリタ言語
C++はコンパイル言語で、コードがあらかじめマシン語に変換されているため、CPUが直接理解して高速に実行できる。

Pythonはインタプリタ言語で、実行時に1行ずつ読み込んで処理しているため、C++に比べてオーバーヘッドが大きくなる。

### run C++ file
`cd library`
`g++ -O3 -std=c++11 main.cpp -o main`
`./main`