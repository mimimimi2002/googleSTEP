import sys
from homework1 import HashTable, Item

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!

class Website:
  def __init__(self, url, contents):
    self.url = url
    self.contents = contents
    self.next = None
    self.prev = None

class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
      self.cache_size = n
      self.website_node_table = HashTable(self.cache_size)
      self.head = None
      self.tail = None
      self.item_count = 0

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        (website_node, success_to_get) = self.website_node_table.get(url)
        if success_to_get:
          print("get the same key")
          print(website_node.url, website_node.contents)
          # then make the node to the first

          # if it is not the most recent one
          if website_node.prev != None:

            # if it is the oldest one
            if website_node.next == None:
              print("move the tail to the first")
              self.tail = self.tail.prev
              website_node.prev.next = None

            else:
              print("move the middle one to the first")
              # delete this node from linked list
              website_node.prev.next = website_node.next
              website_node.next.prev = website_node.prev

            # delete this node from hash table
            self.website_node_table.delete(url)

            # add the node to the fisrt in linked list
            website_node.next = self.head
            website_node.prev = None
            self.head.prev = website_node
            self.head = website_node

            self.website_node_table.put(url, website_node)

        # add curr website to the linked list
        else:
          curr_website = Website(url, contents)

          # if there is nothing yet in linked list
          if self.item_count == 0:
            print("add first element")
            self.head = curr_website
            self.tail = curr_website
            self.website_node_table.put(url, curr_website)
            self.item_count += 1
          else:
            print("add next element")
            curr_website.next = self.head
            self.head.prev = curr_website
            self.head = curr_website
            self.website_node_table.put(url, curr_website)
            self.item_count += 1

          # after put if it is over the size of hash table, throw away the tail
          if self.item_count > self.cache_size:
            print("throw tail")
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
    print(cache.get_pages())
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