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

        # A set of page that has no links to other pages
        self.id_with_no_children = []

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

        for id, link in self.links.items():
          if len(link) == 0:
            self.id_with_no_children.append(id)

        # calculate page ranks so that this will not be called whenever searching
        # the popular page.
        self.ids_sorted_by_popularity = self.calculate_page_ranks()

        print()

    def calculate_variation(self, old_page_ranks, new_page_ranks):
      if len(old_page_ranks) != len(new_page_ranks):
        print("Old page ranks and new page ranks have different length")
        exit(1)
      total = 0
      for old_id, old_page_rank in old_page_ranks.items():
        if old_id not in new_page_ranks:
          print("Some id in old page ranks are not in new page ranks")
          exit(1)
        total += pow((new_page_ranks[old_id] - old_page_rank), 2)
      variation = total / len(old_page_ranks)

      return variation

    def calculate_page_ranks (self, p = 0.85):
      while True:

        # set old page ranks and empty new page ranks
        old_page_ranks = self.id_to_page_ranks
        new_page_ranks = {}

        distribute_to_all_page_ranks = 0
        for id in self.id_with_no_children:
          distribute_to_all_page_ranks += old_page_ranks[id] / len(old_page_ranks)

        for id, old_page_rank in old_page_ranks.items():
          if id not in new_page_ranks:
            new_page_ranks[id] = 0

          # if there is no children, not distribute but remains in the same node
          if len(self.links[id]) == 0:
            continue

          # get distributed ratio
          distribute_ratio = 1 / len(self.links[id])

          # add the distributed rank to its children
          # only add to 85% of children
          for child_id in self.links[id]:
            if child_id not in new_page_ranks:
              new_page_ranks[child_id] = 0
            new_page_ranks[child_id] += old_page_rank * distribute_ratio * p

          distribute_to_all_page_ranks += old_page_ranks[id] * (1 - p) / len(old_page_ranks)

        for id, new_page_rank in new_page_ranks.items():
          new_page_ranks[id] += distribute_to_all_page_ranks
        # if the variation difference is small enough, then break
        if self.calculate_variation(old_page_ranks, new_page_ranks) < 0.01:
          break

        # renew the page ranks
        self.id_to_page_ranks = new_page_ranks

        # check if the total page ranks remain the same
        total = 0
        for id, page_ranks in self.id_to_page_ranks.items():
          total += page_ranks
        print("total", total)

      sorted_ids = sorted(self.id_to_page_ranks, key=lambda x: self.id_to_page_ranks[x], reverse=True)
      return sorted_ids

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

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        # use bfs
        queue = deque()
        visited_id = {}
        previous_id = {}

        if start not in self.title_to_id or goal not in self.title_to_id:
          print("Start or goal is not in page dictionary")
          exit(1)
        start_id = self.title_to_id[start]
        goal_id = self.title_to_id[goal]

        start_id = self.title_to_id[start]
        goal_id = self.title_to_id[goal]

        queue.append(start_id)
        visited_id[start_id] = True

        while len(queue) > 0:
          node_id = queue.popleft()
          if node_id == goal_id:
            break
          for child_id in self.links[node_id]:
            if child_id not in visited_id:
              queue.append(child_id)
              visited_id[child_id] = True
              previous_id[child_id] = node_id

        if goal_id in previous_id:
          print(" -> ".join(self.find_path(goal_id, previous_id)))
        else:
          print("Not found")

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

    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
      numbers_page = 10
      if len(self.ids_sorted_by_popularity) < 10:
        numbers_page = len(self.ids_sorted_by_popularity)
      for i in range(numbers_page):
        print(self.titles[self.ids_sorted_by_popularity[i]])


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


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
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    #wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    #wikipedia.find_longest_path("渋谷", "池袋")