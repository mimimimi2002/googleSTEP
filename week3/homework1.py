#! /usr/bin/python3

# read number for integer and float number
def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def calculate_times_divide(index, tokens):
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
        print("times_divide_number")
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
          print("plus or minus")
          answer = tokens[index]['number']
        else:
            print('Invalid syntax')
            exit(1)
    index += 1
  return tokens

def calculate_plus_minus_to_get_answer(index, tokens):
  answer = 0
  while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            print("plust_minus_number")
            if tokens[index - 1]['type'] == 'PLUS':
                print("plus")
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                print("minus")
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
  return answer

def evaluate(tokens):

    # Insert a dummy '+' token #need to specify the place it is inserted
    tokens.insert(0, {'type': 'PLUS'})
    index = 1

    # process times and divide calculation
    tokens = calculate_times_divide(index, tokens)

    # process plus and minus calculation
    answer = calculate_plus_minus_to_get_answer(index, tokens)

    return answer


def test(line):
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
      line = input()
      tokens = tokenize(line)
      answer = evaluate(tokens)
      print("answer = %f\n" % answer)