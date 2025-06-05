# googleSTEP

## File Descriptions

| File name, folder name               | Usage                             | Command |
|-----------------------|--------------------------------------------------|---------|
| homework1.py          | Main code for homework1                          |python homework1.py|
| homework2.txt          | Answer for homework2                            |           |
| homework3.txt          | Answer for homework3                            |           |
| homework4.py           | Main code for homework4                         |           |
| hashmap_visualize      | A website to visualize the customized hash map  |url: https://mimimimi2002.github.io/googleSTEP/|

# Homework1
## Overview
Implement hash function. We have a hashmap table(bucket) with the size of 97 as default.
Each bucket holds a linked list that stores a pair of key and value which has the same calculated hash. This calculated by our own hash_function and get the index of bucket by the remainder when divided by the bucket size.

`index = hash_function(key) % bucket_size`

## Resize
Hash map has a issue with memeory where if the items are almost full of hash map, increase the size of hashmap and if the items only take up small amout of hash map,
decrease the sisze of hashmap.
This time, I implement this by increasing the size when the number of items takes up 70 % of bucket size and decreasing the size when it takes up 30 % of bucket size.

## Hash function
Hash function calculates the hash number which is a number that represents the key.

## What is the good hash size and good hash function?
To make sure the index for each element is distributed evenly, we need to carefully determine the size of hash map and hash function to avoid collision.

### What is good hash size?
When increasing the size, is it ok to just double it? After doubling it, the size is even number that might cause the conflicts more easily. For example,
the reminder of even number divided by even number is even and
the reminder of odd number divided by even number is odd.
Therefore, I expect that the odd number and if it is prime number, it can distribute the index almost evenly.

### What is good hash function?
Ideally, the hash function will not produce the same number if the key is different.
Also, it needs to be distributed to prevent the numbers from clustering around certain values.

## A tool to visualize hash map
Although we predict some of the features of the hash function and the size of hash map can contribute to the distribution of index of table, it is challenging to visualize how these features can affect the distribution.
We create a tool that can visualize the hash map by putting table size and number of keys and range of key (we conver the number that is range between 0 to this number and conver to string as input) and how to implement hash map and output the two kind of way to visualize hashmap, one is the grids with numbers with dense red color as the numbers that index holds is large. The other is to　dot the canvas with red point.

### How to use the tool to visualize hash map?
1. visit `https://mimimimi2002.github.io/googleSTEP/`

2. put the table size in Hash table size blank, the size of keys, the range of key, and
   the hash function using javascript.

3. click test button

4. The result of distribution including mean, variation, standard deviation, max, min of the number of keys each index holds will be shown.
   Also there is a number mode and canvas mode you can choose to visualize the hash map.

5. If you want to change the value of input at 4, change the input and click the test button, then different result will be shown.

