# coding:utf8
# __author__ = "qx"

import sys
import time
import random
import copy
from optparse import OptionParser

'''
generate a sudoku having a solution or more
idea:
fill 1 in 9 little matrixs
fill 2 in 9 little matrixs
...
one by one until all filled

you can generate a sudoku question to test you script
'''


all_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
area_position = [[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]


# print matrix question to screen
def print_matrix(matrix):
    for i in range(9):
        print(' '.join(matrix[i]))
    print("\n")


# save matrix question to file
def save_matrix(matrix, matrix_filename):
    matrix_file = open(matrix_filename, 'w')
    for i in range(8):
        matrix_file.write(''.join(matrix[i]) + "\n")
    matrix_file.write(''.join(matrix[8]))
    matrix_file.close()


# get a num can fill in what position in a small matrix
def get_alternative_positions(matrix, all_nums_position, area_num):
    conflict_positions = []

    # add conflict position in small matrix
    for i in range(area_position[area_num][0], area_position[area_num][0] + 3):
        for j in range(area_position[area_num][1], area_position[area_num][1] + 3):
            if matrix[i][j] != '*':
                conflict_positions.append([i,j])

    # add conflict position about row
    for i in range(area_position[area_num][0], area_position[area_num][0]+3):
        for j in range(9):
            if matrix[i][j] == all_nums[all_nums_position]:
                for k in range(area_position[area_num][1], area_position[area_num][1] + 3):
                    if [i,k] not in conflict_positions:
                        conflict_positions.append([i,k])
                break
    
    # add conflict position about column
    for j in range(area_position[area_num][1], area_position[area_num][1] + 3):
        for i in range(9):
            if matrix[i][j] == all_nums[all_nums_position]:
                for k in range(area_position[area_num][0], area_position[area_num][0] + 3):
                    if [k,j] not in conflict_positions:
                        conflict_positions.append([k,j])
                break
    
    # get alternative positions
    alternative_positions = []
    if len(conflict_positions) < 9:
        for i in range(area_position[area_num][0], area_position[area_num][0] + 3):
            for j in range(area_position[area_num][1], area_position[area_num][1] + 3):
                if [i,j] not in conflict_positions:
                     alternative_positions.append([i,j])
        random.shuffle(alternative_positions) # here import some random
     
    return alternative_positions


# fill a special num in 9 small matrix
def fill_the_num(matrix, all_nums_position, area_num):
    if area_num == 9: # the num fill finished, continue with next num
        generate_matrix(matrix, all_nums_position+1, 0)
        return

    alternative_positions = get_alternative_positions(matrix, all_nums_position, area_num)
    for alternative_position in alternative_positions:
        matrix[alternative_position[0]][alternative_position[1]] = all_nums[all_nums_position]
        fill_the_num(matrix, all_nums_position, area_num + 1)
        matrix[alternative_position[0]][alternative_position[1]] = '*'


    # all tested and all failed, need to reset matrix
    for alternative_position in alternative_positions:
        matrix[alternative_position[0]][alternative_position[1]] = '*'
    return


# del some position from a filled matrix
def random_remove_num(matrix, del_sum):
    while del_sum > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if matrix[i][j] != '*':
            matrix[i][j] = '*'
            del_sum -= 1
    return matrix


# about generate end and change num
def generate_matrix(matrix, all_nums_position, area_num):
    if all_nums_position == 9:
        
        final_matrix = copy.deepcopy(matrix)
        final_matrix = random_remove_num(final_matrix, blank_sum)
        
        print("quesiton_matrix:")
        print_matrix(final_matrix)
        print("answer_matrix:")
        print_matrix(matrix)

        save_matrix(final_matrix, "question.txt")
        save_matrix(matrix, "answer.txt")

        run_time = time.time() - start_time
        print("Done!")
        print("The question saved in question.txt")
        print("The answer saved in answer.txt")
        print("Used time: " + str(run_time))
        exit(0)
        
    fill_the_num(matrix, all_nums_position, area_num)

    # run here mean all failure, reset and return
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == all_nums[all_nums_position]:
                matrix[i][j] = '*'
    return


def main():
    
    parser = OptionParser(
        "Usage:    python sudoku_generate.py [options]\nExample:  python sudoku_generate.py -b 30")
    parser.add_option("-b", "--blank", type="int",
                      dest="blank_sum", help="blank sum in sudoku")
    (options, args) = parser.parse_args()

    global blank_sum
    blank_sum = options.blank_sum

    if blank_sum == None:
        parser.print_help()
        exit(0)
    
    if blank_sum > 81 or blank_sum < 0:
        print("Blank sum range is: 0 ~ 81")
        exit(0)

    global start_time
    start_time = time.time()

    matrix = []
    for i in range(9):
        matrix.append(list('*' * 9))
    generate_matrix(matrix, 0, 0)

if __name__ == '__main__':
    main()
