import sys
import collections
from collections import deque
import random
import copy

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

    # A helper function to find a path.
    def find_path(self, goal_id, previous_id):
        path = []
        node_id = goal_id
        path.append(self.titles[node_id])

        while node_id in previous_id and previous_id[node_id]:
            node_id = previous_id[node_id]
            path.append(self.titles[node_id])
        path.reverse()
        return path

    # find the longest path from start to goal
    # print a list of path whenever it is extended
    def find_longest_path(self, start, goal):

      # get start id and goal id, if not, exit
      if start not in self.title_to_id or goal not in self.title_to_id:
        print("Start or goal is not in page dictionary")
        exit(1)
      start_id = self.title_to_id[start]
      goal_id = self.title_to_id[goal]

      # get the second shortest path between start and goal
      second_path = self.find_long_path(start_id, goal_id)
      print(second_path, len(second_path))

      # extend the path from back with two nodes that are next to each other
      # extend the path as long as it is longer than original path
      while True:
          previous_path = second_path

          # extend all the nodes that are next to each other
          extended_path_to_all_nodes_next_to_each_other = self.extend_path(previous_path)

          # if the extended path is longer than the orignial path, break the loop
          if len(second_path) <= len(previous_path):
              break
          print("longest")
          print(" -> ".join(second_path))
          print("length: ", len(second_path))


    # extend the path from back, compare two nodes from back and extend them
    def extend_path(self, path):
      index = len(path) - 1
      while index - 1 >= 0:

        # two nodes that are next to each other from back
        start_id = self.title_to_id[path[index - 1]]
        goal_id = self.title_to_id[path[index]]

        # put the all the id of current path to visited_id
        visited_id = {}
        for node in path:
          visited_id[self.title_to_id[node]] = True

        # make the start id and goal id to unvisited
        visited_id[start_id] = False
        visited_id[goal_id] = False

        print(index-1, index)

        # use the visited id, it will return the path that will not duplicate the current path.
        extended_path = self.find_long_path(start_id, goal_id, visited_id)

        if index == len(path) - 1:
          combined = path[:-2] + extended_path
        else:
          combined = path[: index - 1] + extended_path + path[index + 1: ]

        # if it still has duplicate node, do not extend
        # if there is duplicate node, extend it
        if len(combined) == len(set(combined)):
          print("not duplicate")
          path = combined
          print(combined)
          print("combined length: ", len(combined))
        index -= 1

      return path

    # if the start id and goal id has direct path, return
    # the second shortest path that goes from start to goal
    def find_long_path(self, start_id, goal_id, visited_id = {}):

        # use bfs
        queue = deque()
        previous_id = {}

        queue.append(start_id)
        visited_id[start_id] = True

        first_goal = True

        print("finding longer path" , self.titles[start_id], self.titles[goal_id])

        while len(queue) > 0:
          node_id = queue.popleft()
          visited_id[node_id] = True
          if node_id == goal_id:
              path = self.find_path(goal_id, previous_id)

              # if it is the second time to reach to the goal, return its path
              if first_goal  == False:
                return path

              # if it is first time to find the goal,
              # make the goal node unvisited and restart the search again
              else:
                visited_id[node_id] = False
                first_goal = False
                continue

          for child_id in self.links[node_id]:
            if child_id not in visited_id or visited_id[child_id] == False:
              queue.append(child_id)
              previous_id[child_id] = node_id

        path = self.find_path(goal_id, previous_id)
        return path




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
    wikipedia.find_longest_path("渋谷", "池袋")
    # wikipedia.find_longest_path("C", "E")