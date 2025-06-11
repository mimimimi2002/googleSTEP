#! /usr/bin/python3

def read_number(line, index):
  """
  Given a string of number and the start of index of the string of number and
  return the token that represents number and the index after going through
  all the characters in the given string of number.

  Args:
      line (string): a string of number including integer and float number
      index (int): the start of index of the string of number

  Returns:
      dictionary: the token that represents the given string of number
                  ex {'type' : 'NUMBER', 'number': 8}
                     {'type' : 'NUMBER', 'number': 12.455}
      int: the index after going through all the characters in the given string of number.

  """
  number = 0

  while index < len(line) and line[index].isdigit(): # read integer part
      number = number * 10 + int(line[index])
      index += 1
  if index < len(line) and line[index] == '.': # read float part
      index += 1
      decimal = 0.1
      while index < len(line) and line[index].isdigit():
          number += int(line[index]) * decimal
          decimal /= 10
          index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(index):
  """
  Given the index of plus symbol and return token that represents plus
  and the next index.

  Args:
      index (int): index of plus symbol

  Returns:
      dictionary: token that represents plus, {'type': 'MINUS'}
  """
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(index):
  """
  Given the index of minus symbol and return token that represents minus
  and the next index.

  Args:
      index (int): index of minus symbol

  Returns:
      dictionary: token that represents minus, {'type': 'MINUS'}
  """
  token = {'type': 'MINUS'}
  return token, index + 1

def read_times(index):
  """
  Given the index of minus symbol and return token that represents times
  and the next index.

  Args:
      index (int): index of times symbol

  Returns:
      dictionary: token that represents times, {'type': 'TIMES'}
  """
  token = {'type': 'TIMES'}
  return token, index + 1

def read_divide(index):
  """
  Given the index of minus symbol and return token that represents divide
  and the next index.

  Args:
      index (int): index of divide symbol

  Returns:
      dictionary: token that represents divide, {'type': 'DIVIDE'}
  """
  token = {'type': 'DIVIDE'}
  return token, index + 1

def read_parentheses_right(index):
  """
  Given the index of minus symbol and return token that represents right parentheses
  and the next index.

  Args:
      index (int): index of right parentheses symbol

  Returns:
      dictionary: token that represents right parentheses, {'type': 'PARNTHESES_RIGHT'}
  """
  token = {'type': 'PARNTHESES_RIGHT'}
  return token, index + 1

def read_parentheses_left(index):
  """
  Given the index of minus symbol and return token that represents left parentheses
  and the next index.

  Args:
      index (int): index of left parentheses symbol

  Returns:
      dictionary: token that represents left parentheses, {'type': 'PARNTHESES_LEFT'}
  """
  token = {'type': 'PARNTHESES_LEFT'}
  return token, index + 1

def tokenize(line):
  """
  Given the string of equation and returns a list of toekns that represents this equation.
  If the line contains the invalid characters, print Invalid character found: character

  Args:
      line (string): string of equation

  Returns:
      list: list of dictionary that represents this equation
            ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 15}]
  """
  tokens = []
  index = 0
  while index < len(line):
      if line[index].isdigit():
          (token, index) = read_number(line, index)
      elif line[index] == '+':
          (token, index) = read_plus(index)
      elif line[index] == '-':
          (token, index) = read_minus(index)
      elif line[index] == '*':
          (token, index) = read_times(index)
      elif line[index] == '/':
          (token, index) = read_divide(index)
      elif line[index] == '(':
          (token, index) = read_parentheses_left(index)
      elif line[index] == ')':
          (token, index) = read_parentheses_right(index)
      else:
          print('Invalid character found: ' + line[index])
          exit(1)
      tokens.append(token)
  return tokens

def calculate_times_divide(index , tokens):
  """
  Given the index that starts to compute tokens and a list of tokens,
  returns the list of tokens that times or divide calculations are replaced with
  the computed result.

  Args:
      index (int): index that starts to compute tokens
      tokens (list): a list of dictionary that represents as tokens
                     ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 15}, {'type' : 'DIVIDE'},{'type': 'NUMBER', 'number' : 5}]

  Returns:
      list: a list of tokens that times or divide calculations are replaced with
            the computed result.
            ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 3}]
  """
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
        if tokens[index - 1]['type'] == 'TIMES':
            answer *= tokens[index]['number']
            tokens.pop(index)
            tokens.pop(index - 1)
            tokens.pop(index - 2)
            tokens.insert(index - 2, {'type' : 'NUMBER', 'number': answer})
            index -= 2
        elif tokens[index - 1]['type'] == 'DIVIDE':
            answer /= tokens[index]['number']
            tokens.pop(index)
            tokens.pop(index - 1)
            tokens.pop(index - 2)
            tokens.insert(index - 2, {'type' : 'NUMBER', 'number': answer})
            index -= 2
        elif tokens[index - 1]['type'] == 'PLUS' or tokens[index - 1]['type'] == 'MINUS':
          answer = tokens[index]['number']
        else:
            print('Invalid syntax')
            exit(1)
    index += 1
  return tokens

def calculate_plus_minus_to_get_answer(index, tokens):
  """
  Given the index that starts to compute tokens and a list of tokens,
  returns the list of tokens that plus or minus calculations are replaced with
  the computed result.

  Args:
      index (int): index that starts to compute tokens
      tokens (list): a list of dictionary that represents as tokens
                     ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 15}, {'type' : 'PLUS'},{'type': 'NUMBER', 'number' : 5}]

  Returns:
      list: a list of tokens that plus or minus calculations are replaced with
            the computed result.
            ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 20}]
  """
  answer = 0
  while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
  return answer

def calculate_parentheses(index, tokens):
  """
  Given a list of tokens representing a mathematical equation the
  and the index that starts the computation of the tokens,
  returns the tokens which the equation with parentheses are replaced with the
  computed result with the style of {'type': 'NUMBER', 'number' : result}

  Args:
      index (int): index of the tokens that starts the computation
      tokens (list): a list of tokenized tokens. Each element is a dictionary with
                     'type' as key and the type of the token as value.
                     if the type of element is number, 'number' as key and the value
                     of the number as value is added to the dictionray
                     ex) [{'type' : 'PLUS'}, {'type': 'PARNTHESES_RIGHT'}, {'type': 'NUMBER', 'number' : 15}, {'type': 'PLUS'}, {'type': 'NUMBER', 'number' : 3}, {'type': 'PARNTHESES_LEFT'}]

  Returns:
      list: a list of tokens which the equation with parentheses are replaced with the
            computed result with the style of {'type': 'NUMBER', 'number' : result}
            ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 18}]

  """

  parentheses_left_index_stack = [] # store the index of left parentheses
  while index < len(tokens):
    if tokens[index]['type'] == 'PARNTHESES_LEFT':
      tokens.insert(index + 1, {'type': 'PLUS'}) # insert a dummy '+' token after '('
      parentheses_left_index_stack.append(index) # add the index of '('
      index += 1

    if tokens[index]['type'] == 'PARNTHESES_RIGHT':
      parentheses_right_index = index

      if len(parentheses_left_index_stack) == 0: # when there is no corresponding left parentheses, print invalid syntax
        print('Invalid syntax')
        exit(1)

      parentheses_left_index = parentheses_left_index_stack.pop() # get the newest left parentheses
      start = parentheses_left_index + 1
      end = parentheses_right_index - 1

      result = calculate_four_operation(1, tokens[start:end + 1]) # get the result of computation of the equation in the parentheses

      # delete the parentheses including the equation inside the parentheses
      for i in range(parentheses_right_index - parentheses_left_index + 1):
        tokens.pop(parentheses_left_index)

      # insert the computed result to where the parentheses equation is used to be
      tokens.insert(parentheses_left_index, {'type': 'NUMBER', 'number': result})
      index = parentheses_left_index

    index += 1
  return tokens

def evaluate(tokens):
  """
  Takes a list of tokens representing a mathematical expression
  and returns the computed result.
  If there is a invalid syntax including there is a invalid char or space or
  the structure of parentheses is not proper, print 'Invalid syntax'.
  Args:
      tokens (list): a list of tokenized tokens. Each element is a dictionary with
                     'type' as key and the type of the token as value.
                     if the type of element is number, 'number' as key and the value
                     of the number as value is added to the dictionray
                     ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 15}]

  Returns:
      int or float: the result of the computing of tokens.
  """

  # Insert a dummy '+' token
  # need to specify the place it is inserted
  tokens.insert(0, {'type': 'PLUS'})
  index = 1

  # Replace the parentheses part with the computed result of the equation that is
  # inside of parentheses.
  tokens = calculate_parentheses(index, tokens)

  # Get the answer of computed reuslt of the equation only with four operations
  return calculate_four_operation(index, tokens)

def calculate_four_operation(index, tokens):
  """
  Given a list of tokens representing a mathematical equation the
  and the index that starts the computation of the tokens,
  returns the computed result of tokens that only consists of plus, minus, times, divide
  functions.
  Args:
      index (int): index of the tokens that starts the computation
      tokens (list): a list of tokenized tokens. Each element is a dictionary with
                     'type' as key and the type of the token as value.
                     if the type of element is number, 'number' as key and the value
                     of the number as value is added to the dictionray
                     ex) [{'type' : 'PLUS'}, {'type': 'NUMBER', 'number' : 15}]

  Returns:
      int or float: the result of the computing of tokens.
  """
  # process times and divide calculation
  tokens = calculate_times_divide(index, tokens)

  # process plus and minus calculation
  answer = calculate_plus_minus_to_get_answer(index, tokens)

  return answer

def test(line):
  """
  Given the the string of whole equation and test the computed result.
  If it is the correct answer, print "PASS! (computed result = expected result)"

  Args:
      line (string): the string of whole equation string.
  """
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
      print("PASS! (%s = %f)" % (line, expected_answer))
  else:
      print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

if __name__ == "__main__":
  while True:
      print('> ', end="")
      line = input() # get the equation
      tokens = tokenize(line) # tokenize every character in the equation
      answer = evaluate(tokens) # get the answer
      print("answer = %f\n" % answer)