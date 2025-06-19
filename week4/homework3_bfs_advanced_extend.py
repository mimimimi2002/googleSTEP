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

        # 最初の二つ目のパスを探す
        second_path = self.find_long_path(start_id, goal_id)
        print(second_path, len(second_path))
        extended_index = [(0, len(second_path) - 1)]

        # 元の経路と、延長した経路が同じ長さでない限り、延長し続ける
        while True:
            previous_path = second_path

            # second_pathを後ろから順々に延長する
            second_path, extended_index = self.extend_path(previous_path, extended_index)

            # もしパスが伸びなかったら、候補のパスの数を増やしてループを続行
            if len(second_path) <= len(previous_path):
                break
            print("longest")
            print(" -> ".join(second_path))
            print("length: ", len(second_path))

    # 後ろから順に隣接する二つのパスを延長する、それを追加したときに、延長したパスに重複がなければ、元のパスと置き換える。
    # ただし前回のループで延長しなかった部分は調べても意味ないので、飛ばすようにする (new_extended_indexに前回延長した部分のindexの情報が入っている)
    def get_combined_path(self, start_index , end_index , path, new_extended_index):
      start_id = self.title_to_id[path[start_index]]
      goal_id = self.title_to_id[path[end_index]]

      visited_id = {}

      for node in path:
        visited_id[self.title_to_id[node]] = True

      visited_id[start_id] = False
      visited_id[goal_id] = False

      extended_path = self.find_long_path(start_id, goal_id, visited_id)
      print(extended_path)

      if end_index == len(path) - 1:
        combined = path[:-2] + extended_path
      else:
        combined = path[: start_index] + extended_path + path[end_index + 1:]

      # もし直接パス以外の候補の中で、延長したあとに
      # # 重複がなければ、元のパスと置き換える、もしあれば、置き換えず続行
      if len(combined) == len(set(combined)):
        print("not duplicate")
        new_extended_index.append((len(path) - 1 - end_index, len(path) - 1 - end_index + len(extended_path) - 1))
        print(combined)
        print("combined length: ", len(combined))
        return combined
      return path

    # 見つけたパスを後ろから順に二つの隣同士のパスをさらに延長する
    # これを延長できなくなるまで続ける
    # 例： 秋葉原-> 新宿-> 池袋.   => 秋葉原-> 新宿->渋谷->山手線-> 池袋. => 秋葉原->焼肉きんぐ-> 新宿->渋谷->山手線-> 池袋.
    def extend_path(self, path, extended_index):
      original_length = len(path)

      new_extended_index = []
      count_from_back = 0
      extend_index_count = 0
      print(extended_index)

      while count_from_back < original_length and extend_index_count < len(extended_index):
        print(original_length - 1 - count_from_back)

        if count_from_back == extended_index[extend_index_count][0]:
          while count_from_back < extended_index[extend_index_count][1]:
            end_index = original_length - 1 - count_from_back
            start_index = original_length - 1 - count_from_back - 1

            path = self.get_combined_path(start_index, end_index, path, new_extended_index)
            print(start_index, end_index)
            count_from_back += 1
          extend_index_count += 1

        else:
          count_from_back += 1


      return path, new_extended_index

    # startとgoalが直接繋がっていると仮定した時に、直接ではないもう一つのパスを返す関数
    # 直接パス以外のfind_count分のパスのリストを返す関数
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

              # 最初に見つけたパスでない時にパスを返す
              if first_goal  == False:
                return path

              # 最初に見つけたパスの時は、goalを一旦visitedからはずし、
              # 探索を再開する
              else:
                visited_id[node_id] = False # visitedからgoalを外す

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