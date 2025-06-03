import sys
from homework1 import HashTable, Item

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

class Website:
  # Initialize the Website node
  # |url|: A string of the accessed URL
  # |contents|: A string of the contents of the URL
  def __init__(self, url, contents):
    self.url = url         # The accessed URL
    self.contents = contents  # The contents of the URL
    self.next = None       # Pointer to the next Website in the linked list
    self.prev = None       # Pointer to the previous Website in the linked list

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
      self.cache_size = n  # The size of the cache
      self.url_website_node_hash_table = HashTable(self.cache_size) # The hash table of the size of cache, take url as key and take Website node as value.
      self.head = None     # Pointer to the first element in the linked list
      self.tail = None     # Pointer to the last element in the linked list
      self.item_count = 0  # The number of elements in the linekd list

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):

      # check if the url as key has already been stored in hash table
      (website_node, success_to_get) = self.url_website_node_hash_table.get(url)

      # if already stored in hash table, delete the node from linked list and make the node to the first.
      # At the same time, we delete the node from hash table and after make it to the first,
      # put the updated node to the hash table again.
      if success_to_get:

        # if it is not the most recent one, divide to two senarios, when it is the middle node or tail node
        if website_node.prev != None:

          # if it is the oldest one (it is tail), delete the node from linked list
          if website_node.next == None:
            self.tail = self.tail.prev
            website_node.prev.next = None

          # if it is middle one, delete the node from linked list
          else:
            website_node.prev.next = website_node.next
            website_node.next.prev = website_node.prev

          # delete this node from hash table
          self.url_website_node_hash_table.delete(url)

          # add the node to the fisrt in linked list
          website_node.next = self.head
          website_node.prev = None
          self.head.prev = website_node
          self.head = website_node

          # put the updated node to the hash table
          self.url_website_node_hash_table.put(url, website_node)

      # If this website has not visited in recent n times, add current website to the linked list
      else:
        curr_website = Website(url, contents)

        # if there is nothing yet in linked list, put the node to the head
        if self.item_count == 0:
          self.head = curr_website
          self.tail = curr_website
          self.url_website_node_hash_table.put(url, curr_website)
          self.item_count += 1

        # if there is already some nodes in the linked list, put the node to the head
        # and put the new node to hash map.
        else:
          curr_website.next = self.head
          self.head.prev = curr_website
          self.head = curr_website
          self.url_website_node_hash_table.put(url, curr_website)
          self.item_count += 1

        # after put the current website, if it is over the size of hash table, throw away the tail
        if self.item_count > self.cache_size:
          self.tail = self.tail.prev
          self.tail.next = None

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
      all_pages = []
      curr = self.head
      while(curr):
        all_pages.append(curr.url)
        curr = curr.next
      return all_pages


def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()