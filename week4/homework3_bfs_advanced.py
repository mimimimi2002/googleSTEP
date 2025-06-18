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

    def find_longest_path(self, start, goal):
        if start not in self.title_to_id or goal not in self.title_to_id:
          print("Start or goal is not in page dictionary")
          exit(1)
        start_id = self.title_to_id[start]
        goal_id = self.title_to_id[goal]
        paths_previous_ids = self.find_long_path(start_id, goal_id, extend_mode=False)
        longest_path, corresponding_prev = max(paths_previous_ids, key=lambda x: len(x[0]))

        # extend path using the same way.
        # example, ..-> ..-> 新宿 -> 池袋 then, get the longer path for 新宿 -> 池袋
        # then replace it with longer path.
        path = self.extend_path(start_id, goal_id, corresponding_prev, longest_path)
        print(" -> ".join(path))
        print(len(path))

        # if goal_id in previous_id:
        #   path = self.find_path(goal_id, previous_id)

        #   # extend path, try to find the long path between two nodes and extend it
        #   # path = self.extend_path(start_id, goal_id, previous_id, path)
        #   print(" -> ".join(path))
        #   print(len(path))
        # else:
        #   print("Not found")

    # パスの延長
    # 最初に見つけた長いパスを後ろから順に二つの隣同士のパスをさらに延長する
    # 例： 秋葉原-> 新宿-> 池袋.   => 秋葉原-> 新宿->渋谷->山手線-> 池袋. => => 秋葉原->焼肉きんぐ-> 新宿->渋谷->山手線-> 池袋.
    def extend_path(self, start_id, node_id, previous_id, path):
      index = 0
      while node_id != start_id:
        paths_previous_ids = self.find_long_path(previous_id[node_id], node_id, extend_mode=True)
        for i in range(len(paths_previous_ids)):
          extended_path, extended_previous_id = paths_previous_ids[i]
          print(extended_path)
          if index == 0:
            combined = path[:-2] + extended_path
          else:
            combined = path[:- (index + 2)] + extended_path + path[-(index) :]
          print(combined)
          if len(combined) == len(set(combined)):
            print("not duplicate")
            path = combined
            index += len(extended_path) - 2
            break
        index += 1
        node_id = previous_id[node_id]

      return path

    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_long_path(self, start_id, goal_id, extend_mode = False):

      # use bfs
        queue = deque()
        visited_id = {}
        previous_id = {}

        queue.append(start_id)
        visited_id[start_id] = True
        count = 0
        paths_previous_ids = []

        if extend_mode:
          max_count = 5
        else:
          max_count = 1000
        print(max_count)


        while len(queue) > 0:
          node_id = queue.popleft()
          visited_id[node_id] = True
          if node_id == goal_id:
              path = self.find_path(goal_id, previous_id)
              paths_previous_ids.append((path, copy.deepcopy(previous_id)))
              if count == max_count:
                return paths_previous_ids
              else:
                visited_id[node_id] = False
                count += 1
                continue
          for child_id in self.links[node_id]:
            if child_id not in visited_id or visited_id[child_id] == False:
              queue.append(child_id)
              previous_id[child_id] = node_id
        if len(paths_previous_ids) == 0:
          return ([start_id, goal_id], previous_id)
        return paths_previous_ids




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