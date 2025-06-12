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
      dictionary: token that represents right parentheses, {'type': 'PARENTHESES_RIGHT'}
  """
  token = {'type': 'PARENTHESES_RIGHT'}
  return token, index + 1

def read_parentheses_left(index):
  """
  Given the index of minus symbol and return token that represents left parentheses
  and the next index.

  Args:
      index (int): index of left parentheses symbol

  Returns:
      dictionary: token that represents left parentheses, {'type': 'PARENTHESES_LEFT'}
  """
  token = {'type': 'PARENTHESES_LEFT'}
  return token, index + 1

def read_function(line, index):
  f_names = ["abs", "int", "round"]
  name_char = []
  while line[index].isalpha() and index < len(line):
    name_char.append(line[index])
    index += 1

  f_name = "".join(name_char)
  if f_name in f_names:
    token = {'type': 'FUNCTION', 'name': f_name.upper()}
    return token, index
  else:
    print("Invalid function name:", f_name)
    exit(1)

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
      token = {}
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
      elif line[index].isalpha(): # if it is function
          (token, index) = read_function(line, index)
      else:
          print('Invalid character found: ' + line[index])
          exit(1)
      tokens.append(token)
  return tokens

def parse_parentheses(index, tokens):
  if tokens[index]['type'] == 'PARENTHESES_LEFT' and tokens[-1]['type'] == 'PARENTHESES_RIGHT':
    answer = parse_expression(0, tokens[index + 1: -1])
    return answer
  else:
    print('Invalid syntax')
    exit(1)

def parse_factor(index, tokens):
    if tokens[index]['type'] == 'NUMBER':
      answer = tokens[index]['number']
      return answer

    elif tokens[index]['type'] == 'MINUS':
      answer = (-1) *  parse_factor(0, tokens[index + 1:])
      return answer

    elif tokens[index]['type'] == 'FUNCTION':
      f_name = tokens[index]['name'].lower()
      result = parse_parentheses(0, tokens[index+1:])
      result_evaluate = eval(f"{f_name}({result})")
      return result_evaluate
    elif tokens[index]['type'] == 'PARENTHESES_LEFT':
      answer = parse_parentheses(0, tokens)
      return answer
    else:
        print('Invalid syntax')
        exit(1)

def parse_term(index, tokens):
  parentheses_right_stack = []
  answer = 0
  index = len(tokens) - 1
  while index >= 0:
      if len(parentheses_right_stack) == 0:
        if tokens[index]['type'] == 'TIMES':
            factor1 = parse_term(0, tokens[:index])
            factor2 = parse_factor(0, tokens[index + 1:])
            answer = factor1 * factor2
            return answer
        elif tokens[index]['type'] == 'DIVIDE':
            factor1 = parse_term(0, tokens[:index])
            factor2 = parse_factor(0, tokens[index + 1:])
            answer = factor1 / factor2
            return answer
      if tokens[index]['type'] == 'PARENTHESES_RIGHT':
          parentheses_right_stack.append(index)
      elif tokens[index]['type'] == 'PARENTHESES_LEFT':
          if len(parentheses_right_stack) == 0:
            print('Invalid syntax')
            exit(1)
          parentheses_right_stack.pop()
      index -= 1
  answer = parse_factor(0, tokens)
  return answer

def parse_expression(index, tokens):
  answer = 0
  index = len(tokens) - 1

  parentheses_right_stack = []
  while index >= 0:
      if len(parentheses_right_stack) == 0:
        if tokens[index]['type'] == 'PLUS':
            term1 = parse_expression(0, tokens[:index])
            term2 = parse_term(0, tokens[index + 1:])
            answer = term1 + term2
            return answer
        elif index != 0 and tokens[index]['type'] == 'MINUS':
            term1 = parse_expression(0, tokens[:index])
            term2 = parse_term(0, tokens[index + 1:])
            answer = term1 - term2
            return answer
      if tokens[index]['type'] == 'PARENTHESES_RIGHT':
          parentheses_right_stack.append(index)
      elif tokens[index]['type'] == 'PARENTHESES_LEFT':
          if len(parentheses_right_stack) == 0:
            print('Invalid syntax')
            exit(1)
          parentheses_right_stack.pop()

      index -= 1
  answer = parse_term(0, tokens)
  return answer

def evaluate(tokens):
  # Insert a dummy '+' token
  # need to specify the place it is inserted
  index = 0

  answer = parse_expression(index, tokens)
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