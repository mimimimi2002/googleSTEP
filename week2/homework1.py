import random, sys, time
import matplotlib.pylab as plt

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    hash = 0
    prime_numbers = [257, 263, 269, 271, 277, 281, 283, 293, 307, 311]

    for i, c in enumerate(key):
      hash += prime_numbers[i] * prime_numbers[i] * ord(c)
    return hash




# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:
    # Initialize the hash table.
    def __init__(self, bucket_size = 97):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.default_bucket_size = bucket_size
        self.bucket_size = bucket_size
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Put key and value to the bucket.
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    def __put_item_to_bucket(self, key, value):

      # calculate hash for the key and get the reminder divided by the size of bucket.
      # and get the index of bucket.
      bucket_index = calculate_hash(key) % self.bucket_size
      item = self.buckets[bucket_index]

      # iterate the linked list in the bucket at the index.
      # if you find the same key, put the updated value in it.
      while item:
          if item.key == key:
              item.value = value
              return False
          item = item.next

      # if it is the new key,
      # put the new item at the first element in the linked list.
      new_item = Item(key, value, self.buckets[bucket_index])
      self.buckets[bucket_index] = new_item
      return True

    # Get all the key and value in the bucket.
    def get_all_items(self):
      items = []
      for i in range(self.bucket_size):
        if self.buckets[i] != None:
          item = self.buckets[i]
          while item:
            items.append(item)
            item = item.next

      return items

    # replace all the items in the bucket
    # |items|: a list of Item instances
    def __replace_all(self, items):
      for item in items:
        self.__put_item_to_bucket(item.key, item.value)

    # shrink the bucket size
    def __shrink_bucket_size(self):
      items = self.get_all_items()

      # recreate new hash table
      # if it the half of the original size is less than 100, make the bucket size 97.
      if int(self.bucket_size / 2) < 100:
        self.bucket_size = self.default_bucket_size

      # half the bucket size and make it odd
      else:
        self.bucket_size = (
            int(self.bucket_size / 2) + 1
            if int(self.bucket_size / 2) % 2 == 0
            else int(self.bucket_size / 2)
        )

      self.buckets = [None] * self.bucket_size

      # replace all the items
      self.__replace_all(items)

    # Increase the size of the bucket.
    def __increase_bucket_size(self):
      items = self.get_all_items()

      # make the size odd
      # try use the prime numbers for bucket size
      self.bucket_size = self.bucket_size * 2 + 1

      # still make sure it will not be divided in small numbers
      # while self.bucket_size % 2 == 0 or self.bucket_size % 5 == 0 or self.bucket_size % 7 == 0 or self.bucket_size % 11 == 0 or self.bucket_size % 13 == 0 or self.bucket_size % 17 == 0 or self.bucket_size % 19 == 0 or self.bucket_size % 23 == 0:
      #   self.bucket_size += 1

      self.buckets = [None] * self.bucket_size

      # replace all the items
      self.__replace_all(items)

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.

        # if the ration of items and bucket size is 70 %, increase the size
        if self.item_count / self.bucket_size >= 0.7:
          self.__increase_bucket_size()

        if self.__put_item_to_bucket(key, value):
          self.item_count += 1
          return True

        return False

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                return (item.value, True)
            item = item.next
        return (None, False)

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str

        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]

        # when item is empty
        if item == None:
          return False

        # when the first elemnt is the target
        if item.key == key:
          self.buckets[bucket_index] = item.next
          self.item_count -= 1

          # check if it can shrink
          if self.bucket_size > 97 and self.item_count <= self.bucket_size * 0.3:
            self.__shrink_bucket_size()
          return True

        # when the middle element or the last element is the target
        prev = item
        curr = item.next
        while curr:
          # find the target
          if curr.key == key:
            prev.next = curr.next
            self.item_count -= 1
            # check if it can shrink
            if self.bucket_size > 97 and self.item_count <= self.bucket_size * 0.3:
              self.__shrink_bucket_size()
            return True

          prev = curr
          curr = curr.next

        return False

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)

# Plot the runtime from the results
def plot_runtime_result(runtimes):
    plt.figure(figsize=(8, 4))
    plt.plot(runtimes, marker='o', linestyle='-')
    plt.title("Runtime Results")
    plt.xlabel("Iteration times")
    plt.ylabel("Runtime")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable()

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0

    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable()
    runtimes = []

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.get(str(rand))
        end = time.time()
        print("%d %.6f" % (iteration, end - begin))
        runtimes.append(end - begin)

    plot_runtime_result(runtimes)

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))

    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()