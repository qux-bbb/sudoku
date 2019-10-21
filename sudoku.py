# coding:utf8

'''
idea:
1. find empty positions (from left to right, from top to bottom)
2. find what number can fill in an empty position(except row, line, 9 position)
3. fill a position, one by one, finally have not a empty position. That is a solution.
'''

import sys
import time

all_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
legal_chars = all_nums + ['*']
answer_filename = ''


# check matrix format and chars
def check_matrix(matrix):
    if len(matrix) != 9:
        print("input_file format is false!")
        exit(0)
    else:
        for i in range(9):
            if(len(matrix[i]) != 9):
                print("input_file format is false!")
                exit(0)
            for j in range(9):
                if matrix[i][j] not in legal_chars:
                    print("input_file has illegal char!")
                    exit(0)


# find what number can fill in an empty position
def get_alternative_nums(matrix, i, j):

    conflict_nums = []
    # add conflic num in row
    for tmp_j in range(0, 9):
        if tmp_j != j and matrix[i][tmp_j] != '*' and matrix[i][tmp_j] not in conflict_nums:
            conflict_nums.append(matrix[i][tmp_j])

    # add conflic num in column
    if len(conflict_nums) < 9:
        for tmp_i in range(0, 9):
            if tmp_i != i and matrix[tmp_i][j] != '*' and matrix[tmp_i][j] not in conflict_nums:
                conflict_nums.append(matrix[tmp_i][j])

    # add conflic num in a small matrix nums
    if len(conflict_nums) < 9:
        start_i = i / 3 * 3
        start_j = j / 3 * 3
        for tmp_i in range(start_i, start_i + 3):
            for tmp_j in range(start_j, start_j + 3):
                if tmp_i != i and tmp_j != j and matrix[tmp_i][tmp_j] != '*' and matrix[tmp_i][tmp_j] not in conflict_nums:
                    conflict_nums.append(matrix[tmp_i][tmp_j])

    # get alternative nums
    alternative_nums = []
    if len(conflict_nums) < 9:
        for num in all_nums:
            if num not in conflict_nums:
                alternative_nums.append(num)

    return alternative_nums


# get all empty positions at start
def get_init_blank_positions(matrix):
    init_blank_positions = []
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == '*':
                init_blank_positions.append([i, j])
    return init_blank_positions


# print matrix to screen
def print_matrix(matrix):
    for i in range(9):
        print(' '.join(matrix[i]))
    print("\n")


# save matrix solution to file
def save_matrix(matrix):
    answer_file = open(answer_filename, 'a')
    for i in range(9):
        answer_file.write(''.join(matrix[i]) + "\n")
    answer_file.write("\n")
    answer_file.close()


# check if it end and fill empty position
def fill_matrix(matrix, init_blank_positions, fill_position):
    global fill_matrix_call_count
    fill_matrix_call_count += 1
    if fill_position == init_blank_positions_sum:  # success
        global solution_sum
        solution_sum += 1
        print("Congratulation!")
        print_matrix(matrix)
        save_matrix(matrix)
        # exit(0)  # if just want a solution , add this
        return
    alternative_nums = get_alternative_nums(
        matrix, init_blank_positions[fill_position][0], init_blank_positions[fill_position][1])
    if len(alternative_nums) < 1:  # have not a num can fill, failure and return
        return
    for alternative_num in alternative_nums:
        matrix[init_blank_positions[fill_position][0]
               ][init_blank_positions[fill_position][1]] = alternative_num
        fill_matrix(matrix, init_blank_positions, fill_position + 1)

    # alternative_num all tested and all failure, affect the matrix position's init value, need change the position value back
    matrix[init_blank_positions[fill_position][0]
           ][init_blank_positions[fill_position][1]] = '*'
    return


def main():

    if len(sys.argv) != 3:
        print("Usage: python sudoku.py <input_file> <output_file>")
        exit(0)

    start_time = time.time()

    question_filename = sys.argv[1]

    global answer_filename
    answer_filename = sys.argv[2]

    global solution_sum
    solution_sum = 0

    global fill_matrix_call_count
    fill_matrix_call_count = 0

    lines = open(question_filename, 'r').read().strip().split("\n")
    matrix = []
    for line in lines:
        matrix.append(list(line))

    check_matrix(matrix)

    init_blank_positions = get_init_blank_positions(matrix)

    global init_blank_positions_sum
    init_blank_positions_sum = len(init_blank_positions)

    if len(init_blank_positions) == 0:  # No star. print, save and exit
        print_matrix(matrix)
        save_matrix(matrix)
    elif init_blank_positions_sum > 70:  # Too many stars, mean too many solutions, exit
        print("No kidding! Too many stars.")
    else:
        fill_position = 0
        fill_matrix(matrix, init_blank_positions, fill_position)

    run_time = time.time() - start_time
    print("Done!")
    print("Used time: " + str(run_time))
    print("fill_matrix call count: " + str(fill_matrix_call_count))
    print("solution sum: " + str(solution_sum))


if __name__ == '__main__':
    main()
