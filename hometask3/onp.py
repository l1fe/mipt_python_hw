__author__ = 'inaumov'

import sys

def convert(expr):
    output = []
    operators = []

    for char in expr:
        if char.isalpha():
            output.append(char)
        elif char in ['+', '-', '*', '/', '^']:
            operators.append(char)
        elif char == ')':
            output.append(operators.pop())

    return ''.join(output)

if __name__ == '__main__':
    for _ in range(int(sys.stdin.readline())):
        print(convert(sys.stdin.readline()))