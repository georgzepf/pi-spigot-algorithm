# Copyright (C) Georg Zepf <contact@zepfgeorg.com>
# Idea / Explanation Prof. Dr. Edmund Weitz / HAW Hamburg

import math, sys, os

# generate new pi matrix
def matrix_generator():
    i = 1
    j = 3
    while True:
        yield [[i, 2 * j], [0, j]]
        i += 1
        j += 2

matrix = matrix_generator()

# convert matrix M to fraction with vector n/1
def matrix_to_fraction(M, n):
    counter = (M[0][0] * n) + (M[0][1] * 1)
    denominator = (M[1][0] * n) + (M[1][1] * 1)

    return math.floor(counter / denominator)

# multiply matrix V and M
def multiply_matrices(M1, M2):
    m1 = (M1[0][0] * M2[0][0]) + (M1[0][1] * M2[1][0])
    m2 = (M1[0][0] * M2[0][1]) + (M1[0][1] * M2[1][1])
    m3 = (M1[1][0] * M2[0][0]) + (M1[1][1] * M2[1][0])
    m4 = (M1[1][0] * M2[0][1]) + (M1[1][1] * M2[1][1])

    return [[m1, m2], [m3, m4]]

# consume matrix M
def consume(V, M):
    return multiply_matrices(V, M)

# apply matrix V to number n
def produce(V, n):
    digit = math.floor(matrix_to_fraction(V, n))
    help_matrix = [[10, -10 * digit], [0, 1]]
    produced_matrix = multiply_matrices(help_matrix, V)

    return { 'digit': digit, 'produced_matrix': produced_matrix }

# check if matrix is save to produce
def save(V): 
    min_produced_digit = matrix_to_fraction(V, 3)
    max_produced_digit = matrix_to_fraction(V, 4)

    if math.floor(min_produced_digit) == math.floor(max_produced_digit):
        return True
    else:
        return False

# append digit d file pi.txt and increase digit count produced_digits
produced_digits = -1

def write_file(d):
    file.write(d)
    global produced_digits
    produced_digits = produced_digits + 1

# append digit count produced_digits
def sign():
    write_file('\n' + str(produced_digits) + " digits produced")

# check if matrix V is save then produce or consume
current_V = [[1, 0], [0, 1]]

def stream(V):
    if save(V):
        produced_result = produce(V, 3)
        write_file(str(produced_result['digit'])) 
        global current_V
        current_V = produced_result['produced_matrix']
    else:
        consumed_matrix = consume(V, next(matrix))
        current_V = consumed_matrix

# get range_input from user
range_input = input('How much decimals? (integer): ')

# generate file with file_name_input name 
file = open(os.path.join('./', range_input + '.decimals.txt'), 'w+')

# while range range_input stream / show produced_progress
while (produced_digits <= int(range_input) - 1):
    stream(current_V)
    produced_progress = math.ceil(produced_digits / int(range_input) * 100)
    sys.stdout.write("\r%d[" %produced_progress + "%]" + "#" * produced_progress)

# print success message with file_name_input name
print('\n>> generated file ' + range_input + '.decimals.txt')

# sign file
sign()