import sys
import collections
from collections import deque
import random

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A mapping from the page title to a page ID (integer).
        # For example, self.titles["渋谷"] returns its ID.
        self.title_to_id = {}

        # A mapping from the page ID to its page ranks
        self.id_to_page_ranks = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.id_to_page_ranks[id] = 1.0
                self.title_to_id[title] = id
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)

        print()

    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def find_path_from_start(self, start_id, next_id):
        path = []
        node_id = start_id
        path.append(self.titles[node_id])

        while node_id in next_id and next_id[node_id]:
            node_id = next_id[node_id]
            path.append(self.titles[node_id])
        return path

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):

      # Using recursion might be better because we don't know
      # how to choose the route until we find the actual goal
      # use recursion to get the each child's path length and choose the maximum
      visited_id = {}
      next_id = {}

      if start not in self.title_to_id or goal not in self.title_to_id:
          print("Start or goal is not in page dictionary")
          exit(1)

      # get the id for each start and goal
      start_id = self.title_to_id[start]
      goal_id = self.title_to_id[goal]

      start_id = self.title_to_id[start]
      goal_id = self.title_to_id[goal]

      visited_id[start_id] = True
      next_id = {}

      # call recursion to renew next_id, in next_id, we have
      # key as id and the next_id that connects from id.
      # ex: {4: 5, 5: 6}, then it means 4 -> 5 -> 6
      self.find_child_with_maximum_path(start_id, goal_id, visited_id, next_id)

      # get the actual path
      if start_id in next_id:
          print(" -> ".join(self.find_path_from_start(start_id, next_id)))
      else:
          print("Not found")

    # return a pair of the next node and the maximum path from node_id to goal_id
    # ex: (4, 10), this means 4 is one of the node_id's child and has the longest
    # path as 10 in all children.
    def find_child_with_maximum_path(self, node_id, goal_id, visited_id, next_id):
      if node_id == goal_id:
        return 0

      # this stores all the possible path from node_id
      paths = []
      for child_id in self.links[node_id]:
        if child_id not in visited_id or visited_id[child_id] == False:
          visited_id[child_id] = True # visit one of the children

          # get the maximum path from the child to goal
          maximum_path = self.recursion(child_id, goal_id, visited_id, next_id)

          # if this path cannot reach to goal, return (child_id, -1),
          # if not return (child_id, maximum_path + 1),
          if maximum_path == -1:
            paths.append((child_id, -1))
          else:
            paths.append((child_id, maximum_path + 1))

          # to visit all the child, reset the child's visit False
          visited_id[child_id] = False
        else: # if there is no child that has not been visited , return (child_id, -1) again
          paths.append((child_id, -1))

      # if there is no child, return -1
      if len(paths) == 0:
        return -1

      # set the next node_id to the node that has maximum path
      next_id[node_id] = max(paths, key=lambda x: x[1])[0]
      return max(paths, key=lambda x: x[1])[1]


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Homework #3 (optional)
    # wikipedia.find_longest_path("渋谷", "池袋")
    wikipedia.find_longest_path("E", "F")