# googleSTEP

## File Descriptions

| File name, folder name               | Usage                             | Command |
|-----------------------|--------------------------------------------------|---------|
| homework1.py          | Main code for homework1                         |python homework1.py pages_file links_file|
| homework1_answer.py   | The output of homework1.py path for each file   | |
| homework2.py          | Main code for homework2                         |python homework2.py pages_file links_file|
| homework2_answer.py   | The output of homework2 for each file           | |
| homework3.py          | Main codeforhomework3                           |python homework3.py pages_file links_file|
| homework3_answer.py   | The middle of output of homework3.py            | |
| dfs_with_stack_in_the_recursion_order.py| Code for DFS using stack to replicate recursion order         | python  dfs_with_stack_in_the_recursion_order.py |

# Homework1
## Overview
Given the page file and link file of the websites, find the fortest path from start and goal.

## Algorithm
Use BFS(breadth first search) to find the shortest path. BFS uses queue and needs to
keep track of visited node to prevent loop.

1. Set queue with start node and make the start node visited

2. While the queue is not empty, pop the node from the queue

3. If the node is goal, break the while loop

4. If not, if the neighbors of the node is not visited, put the neighbors to the queue and make them all visited.

5. back to 2

# Homework2
## Overview
Get most 10 poular pages that is calculated by PageRank.

## What is PageRank?
PageRank is an algorithm discovered by Larry Page and Sergey Brin, the founders of Google, to get the rankings of web pages. It determines how important or relevant a webpage is.

## Algorithm of PageRank
In this homework, we develop a PageRank algorithms in the following way.

1. Set the the page rank for all the node with 1

2. If the node has neighbors, distribute 85 % of its page rank to its neighbors and distribute 15% of its page rank to all the nodes.

3. If the node has no neighbors, distribute its page rank to all the nodes.

4. Repete 2 and 3 until the variation of the previous page rank and the updated page rank has less than 0.01 difference.

# Homework3
## Overview
Get the longest path between two nodes. We approached several methods to reach to  the efficient way to get the longest path.

1. Advanced BFS

In the BFS algorithm, while the queue is not empty, if we pop the node from the queue and is goal node, we get out of the loop to get the shortest path.
But, what if we did not break the loop when find the first goal node, but break the loop when the next time we find the goal? It means we when we first fid the goal node,
make the goal node unvisited (delete the path right before the goal in shortest path) and the other path still continues to find another path to reach to the goal.
The path we get would be another path but it is longer than the shortest path.

To implement this, we first use the boolean to record whether it is the first time to reach to the goal or not.

```
if node_id == goal_id:

  # if it is the second time to reach to the goal, return its path
  if first_goal  == False:
    break

  # if it is first time to find the goal,
  # make the goal node unvisited and restart the search again
  else:
    visited_id[node_id] = False
    first_goal = False
    continue
```

We successfully get the longer version from 渋谷 to 池袋 whose length was 56.

2. Still need to extend, what if we repeat the same algorithm to the two nodes that are
next to each other in the path from 1?

For example, if the path from 1 was `a -> b -> c`, then use the same algorithm from 1 to (b, c) and (a, b) and each of the pair of nodes can extend its path then becomes
`a -> d -> b -> e -> f -> c`.

To implement this, we create a function called extend_path to extend the path,

```
extended_path = self.find_long_path(start_id, goal_id, visited_id)

# get the extended path and combined with original path.
if index == len(path) - 1:
  combined = path[:-2] + extended_path
else:
  combined = path[: index - 1] + extended_path + path[index + 1: ]
```

We successfully repeat this process to get about 1700 length of path.

3. Still problems that this calculation is too slow, and it does not gurantee
that the extend path does not duplicate with the original path, we make all
the nodes in the crrent path visited, so that the the extended path is guaranteed to
be unique.

To implement this, when call the extend path function, make sure that make all the nodes except for the start node and end node visited the find the long path use the advanced bfs algorithm.

```
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

```

We successfully extend the path and the length of the long path is 141741.