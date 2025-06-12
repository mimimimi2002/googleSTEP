# googleSTEP

## File Descriptions

| File name, folder name               | Usage                             | Command |
|-----------------------|--------------------------------------------------|---------|
| homework1.py          | Main code for homework1                         |python homework1.py|
| homework2.py          | Test code for homework1                         |python homework2.py|
| homework3.py          | Main codeforhomework3                           |python homework3.py|
| homework3_test.py     | Test code for homework3                         |python homework3_test.py|
| homework4.py          | Main code for homework4                         |python homework4.py     |
| homework4_test.py     | Test code for homework4                         |python homework4_test.py|

# Homework1
## Overview
Implement to compute the equation including +, -, *, /.
This is done by first calculating the mutiples and divide function and replace them with
the result. Then it only contains +, - and can be calcualted.

## Strucrure
The main flow is

1. calculate *, / operations and replace thses equation with its result.
Iterate from the beginning, the previous token is * or /, calculate it and replace with its result and iterate until it reaches the end

ex: `3 + 4 * 6 / 2` -> `3 + 24 / 2` -> `3 + 12`

2. calcualte +, - operations and get the answer.

ex: `3 + 12 - 14` -> `15 - 14` -> `1`

# Homework2
This is the test for homework1.

# Homework3
## Overview
Implement to compute the equation including +, -, *, / and '()'.
This is done by calculating the computation inside the parentheses and replace all parentheses with result. Then calculate the *, / part and +, - part as homework1 did.

## Strucrure
The main flow is

1. calculate the inside of parenthese and replace it with its result.
First, we stack the '(' and whenever we encounter ')', calculate the equation with +, -, *, / because we are guaranteed that whenever we encounter ')', from the '(' that we take from stack to ')' only has four operations (+, -, *, /).

ex: `(3 + 2 * (4 + 3)) * 6 / 2 + 3` -> `(3 + 2 * 7) * 6 / 2 + 3` -> `17 * 6 / 2 + 3`

2. calculate *, / operations and replace thses equation with its result.
Iterate from the beginning, the previous token is * or /, calculate it and replace with its result and iterate until it reaches the end

ex: `17 * 6 / 2 + 3` -> `102 / 2 + 3` -> `51 + 3`

3. calcualte +, - operations and get the answer.

ex: `51 + 3` -> `54`

## Is this applied to more complex equation?
Can this be applied to complex equation including the function and even can expand to programming language? Now we adapt how the order we calculate because it happened to be clear so far. If we consider to expand this to programming language we introduce
a concept called recursive descent parsing which parses the equation
using our rules.

# Recursive descent parsing
A recursive descent parser is a top-down parser that processes input based on a set of recursive functions, where each function corresponds to a grammar rule. It parses the input from left to right, constructing a parse tree by matching the grammar's production rules.
Whenever it godes to recursive funcitons, a value is returned to calculate the origianl equation.

## Why using the previous method cannot work when function appears in the equation.
When an equation only includes basic operations like +, -, *, /, and parentheses, there are clear and simple rules for evaluating it. For example, we can recursively evaluate the innermost parentheses with + , -, *, / operations because we can assume only this equation comes. Even without explicitly drawing a dependency graph, we can follow a  algorithm to evaluate the expression step by step.

However, when functions (like f(x), g(y), etc.) are involved, the situation becomes more complex. The calculation of one part of the equation may depend on the result of another function or subexpression. As the number of operations and dependencies increases, it's harder to keep track of the relationships between different parts of the equation. In such cases, drawing a dependency graph helps visualize and clarify these relationships, making the problem easier to understand and solve.

Also, I couldn’t divide the equation based on the roles of each part, which made it confusing and hard to focus on what the equation was actually doing.

For example, when a function appears in the equation, I wasn’t able to break it down into smaller, meaningful parts that I could compute step by step. As a result, the only way I could try to parse the function was by going through all the remaining tokens at once, without a clear structure. This made it difficult to understand the role of each part of the equation and how they relate to each other.

# Homework4
## Overview
Implement to compute the equation including +, -, *, / and '()' and several function including abs(), int(), round().
Let's break down this probelm using recursive descent parsing.

P(Parentheses): (E)
L(Literal): Int | Float
F(Factor):  - F | L  | P | func P
T(Term): F | T * F | T / F
E(Expression): T | E + T | E - T

Based on this rule, we will break the equation down.

## What is the motivation to create recursive descent parsing above?
The Expression(whole equation) has a different priority for calculating, first of all plus and - should be the least priority for calculating so we can decompose Expression into T | E + T | E - T.


### Why E - T not T - E
Even though E - E seems ok for analyzing equation, there is a huge trap. For example,

`3 - 4 + 9` -> `3 - 13` -> `-10`

This equation is not correct because even though + and - has the same priority, we need to calculate from left to right, which means we need to consider left side of `-` as an Expression and right side as Term.
