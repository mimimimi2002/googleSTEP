#! /usr/bin/python3

def read_number(line, index):
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
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_times(index):
  token = {'type': 'TIMES'}
  return token, index + 1

def read_divide(index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def read_parentheses_right(index):
  token = {'type': 'PARENTHESES_RIGHT'}
  return token, index + 1

def read_parentheses_left(index):
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

# parse parentheses to get the answer
# |tokens| : a list of dictionary that represents each toekn
def parse_parentheses(tokens):
  index = 0
  if tokens[index]['type'] == 'PARENTHESES_LEFT' and tokens[-1]['type'] == 'PARENTHESES_RIGHT':
    answer = parse_expression(tokens[index + 1: -1])
    return answer
  else:
    print('Invalid syntax')
    exit(1)

# parse factor to get the answer
# |tokens| : a list of dictionary that represents each toekn
def parse_factor(tokens):
    index = 0

    # when factor is Literal
    if tokens[index]['type'] == 'NUMBER':
      answer = tokens[index]['number']
      return answer

    # when factor is - factor
    elif tokens[index]['type'] == 'MINUS':
      answer = (-1) *  parse_factor(tokens[index + 1:])
      return answer

    # when factor is function Parentheses
    elif tokens[index]['type'] == 'FUNCTION':
      f_name = tokens[index]['name'].lower() # get function name
      result = parse_parentheses(tokens[index+1:]) # parse Parentheses following function name

      result_evaluate = eval(f"{f_name}({result})") # evaluate function P
      return result_evaluate

    # when factor is Parentheses
    elif tokens[index]['type'] == 'PARENTHESES_LEFT':
      answer = parse_parentheses(tokens)
      return answer
    else:
        print('Invalid syntax')
        exit(1)

# parse term to get the answer
# |tokens| : a list of dictionary that represents each toekn
def parse_term(tokens):

  # store right parentheses and if the index is between (), skip it
  parentheses_right_stack = []
  answer = 0
  index = len(tokens) - 1
  while index >= 0:
      # if the index is outside of (), if it is times, decompose to
      # term and factor and multiply them
      if len(parentheses_right_stack) == 0:
        if tokens[index]['type'] == 'TIMES':
            factor1 = parse_term(tokens[:index])
            factor2 = parse_factor(tokens[index + 1:])
            answer = factor1 * factor2
            return answer

        # if the index is outside of (), if it is divide, decompose to
        # term and factor and divide them
        elif tokens[index]['type'] == 'DIVIDE':
            factor1 = parse_term(tokens[:index])
            factor2 = parse_factor(tokens[index + 1:])
            answer = factor1 / factor2
            return answer

      # keep track of the number of parentheses
      if tokens[index]['type'] == 'PARENTHESES_RIGHT':
          parentheses_right_stack.append(index)
      elif tokens[index]['type'] == 'PARENTHESES_LEFT':
          if len(parentheses_right_stack) == 0:
            print('Invalid syntax')
            exit(1)
          parentheses_right_stack.pop()
      index -= 1

  # When Term is Factor
  answer = parse_factor(tokens)
  return answer

# parse expresssion to get the answer
# |tokens| : a list of dictionary that represents each toekn
def parse_expression(tokens):
  answer = 0
  index = len(tokens) - 1

  # store right parentheses and if the index is between (), skip it
  parentheses_right_stack = []
  while index >= 0:
      if len(parentheses_right_stack) == 0:

        # if the index is outside of (), if it is plus, decompose to
        # expression and term and do addition.
        if tokens[index]['type'] == 'PLUS':
            term1 = parse_expression(tokens[:index])
            term2 = parse_term(tokens[index + 1:])
            answer = term1 + term2
            return answer

        # skip the first minus
        # if the index is outside of (), if it is minus, decompose to
        # expression and term and do subtraction.
        elif index != 0 and tokens[index]['type'] == 'MINUS':
            term1 = parse_expression(tokens[:index])
            term2 = parse_term(tokens[index + 1:])
            answer = term1 - term2
            return answer

      # keep track of the number of parentheses
      if tokens[index]['type'] == 'PARENTHESES_RIGHT':
          parentheses_right_stack.append(index)
      elif tokens[index]['type'] == 'PARENTHESES_LEFT':
          if len(parentheses_right_stack) == 0:
            print('Invalid syntax')
            exit(1)
          parentheses_right_stack.pop()

      index -= 1

  # When Expression is Term
  answer = parse_term(tokens)
  return answer

def evaluate(tokens):
  answer = parse_expression(tokens)
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