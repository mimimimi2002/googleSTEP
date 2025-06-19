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
Given the page file and link file, find the fortest path from start and goal.

## Algorithm
Use BFS(breadth first search) to find the shortest path. BFS uses queue and needs to
keep track of visited node to prevent loop.

1. Set queue with start node and make the start node visited

2. While the queue is not empty, pop the node from the queue

3. If the node is goal, break the while loop

4. If not, if the neighbors of the node is not visited, put the neighbors to the queue and make them all visited.

5. back to 2