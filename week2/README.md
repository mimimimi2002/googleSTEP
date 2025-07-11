# googleSTEP

## File Descriptions

| File name, folder name               | Usage                             | Command |
|-----------------------|--------------------------------------------------|---------|
| homework1.py          | Main code for homework1                          |python homework1.py|
| homework2.txt          | Answer for homework2                            |           |
| homework3.txt          | Answer for homework3                            |           |
| homework4.py           | Main code for homework4                         |python homework4.py     |
| hashmap_visualize      | A website to visualize the customized hash map  |url: https://mimimimi2002.github.io/googleSTEP/|

# Homework1
## Overview
Implement hash function. We have a hashmap table(bucket) with the size of 97 as default.
Each bucket holds a linked list that stores a pair of key and value which has the same calculated hash. This is calculated by our own hash_function and get the index of bucket by the remainder when divided by the bucket size.

`index = hash_function(key) % bucket_size`

## Resize Hash Table
Hash map needs a flexibility with memeory where if the items are almost full of hash map, increase the size of hashmap and if the items only take up small amout of hash map,
decrease the size of hashmap.
This time, I implemented this by increasing the size when the number of items takes up 70 % of the bucket size and decreasing the size when it takes up 30 % of bucket size.

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
Also, it needs to be distributed to prevent the numbers from clustering around certain values. We use ascii code for each character in the string to create a hash number for that string.

## A tool to visualize hash map
Although we predict some of the features of the hash function and the size of hash map can contribute to the distribution of index of table, it is challenging to visualize how these features can affect the distribution.
We create a tool that can visualize the hash map by putting table size and number of keys and range of key (we convert the number that is ranged between 0 to this number and convert it to string as input) and how to implement hash map and output the two kind of way to visualize hashmap, one is the grids with numbers with red color and the other is the dot of canvas with red point. The color density aligns with the ratio of number of keys with same index to the total number of keys.

The color is calculated by

| Color | RGB Value Calculation |
|---------------|------------------------|
| Red (R) |  always `255` |
|Green (G) | `(1 - number of the keys the index holds / total number of keys) * 255` |
| Blue (B) | `(1 - number of the keys the index holds / total number of keys) * 255` |

If the index holds nothing, the color is white, if the index holds all the keys, the color is maximum red.


### How to use the tool to visualize hash map?
1. visit `https://mimimimi2002.github.io/googleSTEP/`

2. put the table size, the size of keys, the range of key, and
   the hash function using javascript into the inputs.

3. click test button

4. The result of distribution including mean, variation, standard deviation, max, min of the number of keys each index holds will be shown.
   Also there is a number mode and canvas mode you can choose to visualize the hash map.

5. If you want to change the value of input at 4, change the input and click the test button, then different result will be shown.

## Experiments
There are several senarios we can test if it is good hash function and good hash table size. In the following explanation, ord(c) means the ascii code for c character.

### Experiment1
#### Hash function : (index + 1) * ord(c) Table size : prime number

Considerinig that "alice" and "elica" is the same if their ascii codes are added.
If there is a factor that the order matters to create a unique hash number.

#### Small table size
##### Hash Function
```
let hash = 0;
for (let i = 0; i < key.length; i++) {
  hash = (i + 1) * key[i].charCodeAt(0);
}
return hash;
```

#### Setting1
- Hash table size 101
- Number of keys 100
- Range of key 100000

#### Result1
- Variance : 7.36
- Max number of same index: 12
- Min number of same index : 0

<p align="center">
  <img src="./experiment1_small_size.png" alt="Index distribution in experiment1 with small table size" width="300"/>
  <br>
  <strong>Figure 1:</strong> Index distribution in <code>Experiment1</code> with small table size
</p>

#### Setting2
- Hash table size 100003
- Number of keys 100000
- Range of key 10000000

#### Result2
- Variance : 7.36
- Max number of same index: 12
- Min number of same index : 0

<p align="center">
  <img src="./experiment1_large_size.png" alt="Index distribution in experiment1 with small table size" width="300"/>
  <br>
  <strong>Figure 2:</strong> Index distribution in <code>Experiment1</code> with large table size
</p>

#### Observation
This hash function does not apply to the large number where it reqires the large number as hash number.

### Experiment2
#### Hash function : primeNumber(larger than the maximum of ascii code) * primeNumber(larger than the maximum of ascii code) * ord(c) Table size: prime number

Considerinig that reaching to the large number and not overlapped with ascii code, we chosed large number of prime number and power them by 2.

#### Hash Function
```
let hash = 0;
const primesFrom256 = [257, 263, 269, 271, 277, 281, 283, 293, 307, 311];
for (let i = 0; i < key.length; i++) {
  hash += primesFrom256[i] * primesFrom256[i] * key[i].charCodeAt(0);
}
return hash;
```

#### Setting1
- Hash table size 101
- Number of keys 100
- Range of key, 100000

#### Result1
- Variance : 1.02
- Max number of same index: 4
- Min number of same index : 0

<p align="center">
  <img src="./experiment2_small_size.png" alt="Index distribution in experiment1 with small table size" width="300"/>
  <br>
  <strong>Figure 3:</strong> Index distribution in <code>Experiment2</code> with small table size
</p>

#### Setting2
- Hash table size 100003
- Number of keys 100000
- Range of key 10000000

#### Result2
- Variance : 1.02
- Max number of same index: 9
- Min number of same index : 0

<p align="center">
  <img src="./experiment2_large_size.png" alt="Index distribution in experiment2 with large table size" width="300"/>
  <br>
  <strong>Figure 4:</strong> Index distribution in <code>Experiment2</code> with large table size
</p>

### Experiment3
#### Hash function : Rolling hash Table size: prime number
This is a common hash that does not occur the collision using the idea of converting to another base. In this way, the small number will be changed to corresponding number in that base.

#### Hash Function
```
let base = 256;
let hash = 0;
for (let i = 0; i < key.length; i++) {
  hash = (hash * base + key[i].charCodeAt(0));
}
return hash;
```

#### Setting1
- Hash table size 101
- Number of keys 100
- Range of key, 100000

#### Result1
- Variance : 0.82
- Max number of same index: 3
- Min number of same index : 0

<p align="center">
  <img src="./experiment3_small_size.png" alt="Index distribution in experiment2 with large table size" width="300"/>
  <br>
  <strong>Figure 5:</strong> Index distribution in <code>Experiment3</code> with small table size
</p>


#### Setting2
- Hash table size 100003
- Number of keys 100000
- Range of key 10000000

#### Result2
- Variance : 1.00
- Max number of same index: 8
- Min number of same index : 0

<p align="center">
  <img src="./experiment3_large_size.png" alt="Index distribution in experiment3 with large table size" width="300"/>
  <br>
  <strong>Figure 5:</strong> Index distribution in <code>Experiment3</code> with large table size
</p>


## Result
Take into account that the hash number is unique and has a variety of range and make sure that the number is way bigger than the bucket size, it is more easy to distribute the index of bucket. Using prime number in hash function and bucket size is also efficeint way.

## Further question
If the hash function is good enough which can produce unique number, does table size matter? Is it still ok even you use the even number?
How about odd number, does it matter to be a prime number?
We will use Rolling Hash as hash number.

### Experiment4
#### Hash function : Rolling hash Table size: even number

#### Setting
- Hash table size 100000
- Number of keys 100000
- Range of key 10000000

#### Result
- Variance : 6.82
- Max number of same index: 21
- Min number of same index : 0

<p align="center">
  <img src="./experiment4.png" alt="Index distribution in experiment5" width="300"/>
  <br>
  <strong>Figure 5:</strong> Index distribution in <code>Experiment4</code>
</p>


### Experiment5
#### Hash function : Rolling hash Table size: odd number

#### Setting
- Hash table size 99999
- Number of keys 99999
- Range of key 10000000

#### Result
- Variance : 1.02
- Max number of same index: 8
- Min number of same index : 0

<p align="center">
  <img src="./experiment5.png" alt="Index distribution in experiment5" width="300"/>
  <br>
  <strong>Figure 5:</strong> Index distribution in <code>Experiment5</code>
</p>


## Conclusion
Good hash function is one that produces unique number and has a variety of range and way bigger than the bucket size. Regarding table size, it seems it doesn't matter the size is prime number but as long as it is odd number and hash function is good enough to distribute, it works.

## The method used in homework1
In homework1, we used the original hash function from `Experiment2` and when resizing, make sure that the hash table's size is odd number but we didn't care whether it is prime number.

This is the graph that shows how much it takes to put the random string that is ranged from 0 to 99999999 and get the each item for 10000 times. We consider this is one iteration and did 100 iterations and keep adding 10000 items to the hash map for each iteration.

<p align="center">
  <img src="./homework1_result.png" alt="homework1 result graph"/>
  <br>
  <strong>Figure 6:</strong> The runtime of test in homework1
</p>

If we did not use the appropriate hash function and hash table size, the collision makes the runtime longer and usually it is O(N). However, using the original hash function that produces unique number and odd number as the table size, we successfully make the insertion of the element and get the element with O(1) time complexity.

# Homework2
This is the answer why tree structure is more likely to be used when it comes to storing a huge data compared to hash map.

# Homework3, 4
## Overview
Cashe is common idea that is used to store a certain amount of data especially for recent data. This time we implemented a cache that can store recent N websites including its url and contetns. To ignore that we will need the order from recent website to old website, we can store into hash map to achieve adding and deleting and seaching with O(1) time complexity. However, we need to keep track of the history and also change the order whenever we access the new pate.

To store the history, we have two main data structure, array and linked list.
Array can hold the order of time by index as well as linked list can hold the order by
pointing to the next node or previous node.
Considering that for array adding takes O(1) and O(N) if the resize is needed, and deleting takes O(N), and searching for O(N), even though we store the index for each element in hash table, to resizing and moving the elements after deleting still remain issues.

On the other hand, the linked list takes O(1) to add new element to head, and deleting the last node for O(1) if we have a tail pointer to keep track the last node. We ususllay come across the problem that searching takes O(N) because we need to search from the first node.

Then we came up with an idea that what if we store the key and its node in hash table so that we don't need to search from the head to the specific node we want to delete.

## Implementation with linked list and hash table
Linked list: the list of Website node that has its url and contents and next pointer to point to older website node and previous pointer to point to newer website node.

Hash table: Hash table with n size and hold url as key and Website node as value.

To achieve cashe, we have several features for it.

1. If there is no same url as the new visited page in the cache, add the new pair of (url, contents) to the head and delete the oldest node.
First, use hash table to search the key(O(1)). Then make the tail pointer point to the previous node (O(1)). Then add the new node to the head (O(1)).


2. If there is the same url in the cache already, delete the node and make the node to the head. First, use hash table to search the key(O(1)) and if they find the key, take the node it is coresponded. Delete the node (O(1)) and add the node to the head(O(1)).
As they delete the node from linked list , delete the node from hash table as well (O(1)) and after make it to the head, add the updated node to the hash table(O(1)).

