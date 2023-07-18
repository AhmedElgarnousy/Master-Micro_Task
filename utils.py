import re

ALLOWED_OPERATORS = ['x', '+', '-', '/', '*', '^']

def string_to_function(expression):
    ''' Evaluates the expression and returns a function of x '''
    # Find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', expression):
        if word not in ALLOWED_OPERATORS:
            raise ValueError(
                f"'{word}' is forbidden to use in math expression.\nOnly the operators '+', '-', '/', '*', and '^', along with 'x' are allowed.\nExample: 5*x^3 + 2/x - 1"
            )

    # To deal with constant functions e.g., y = 1
    if "x" not in expression:
        expression = f"{expression}+0*x"

    def func(x):
        return eval(expression)

    return func
