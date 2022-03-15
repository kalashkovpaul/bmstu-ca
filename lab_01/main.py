from cmath import inf
import copy

def to_float(matrix):
    for row in matrix:
        for i in range(len(row)):
            row[i] = float(row[i])

def swap_columns(matrix):
    new_matrix = copy.deepcopy(matrix)
    for row in new_matrix:
        row[0], row[1] = row[1], row[0]
    return new_matrix

def multiply_rows(matrix):
    new_matrix = []
    for row in matrix:
        new_matrix.append(row)
        new_matrix.append(row)

    return new_matrix

def input_information():
    # filename = input("Введите имя файла с данными: ")
    filename = "./lab_01/table"
    try:
        with open(filename) as file:
            matrix = [row.split() for row in file.readlines()]
        arg = float(input("Введите значение аргумента: "))
    except:
        print("Ошибка. Данные представлены в некорректном формате")
        exit()
    to_float(matrix)
    return matrix, arg

def print_results(newton, hermite, newton_root, hermite_root):
    print("Ньютон: {:.6f}".format(newton))
    print("Эрмит: {:.6f}".format(hermite))
    print("Корень(Ньютон): {:.6f}".format(newton_root))
    print("Корень(Эрмит): {:.6f}".format(hermite_root))

def get_range(matrix, degree, arg):
    for right in range(len(matrix)):
        if matrix[right][0] > arg:
            break
    left = right
    while right - left < degree:
        if left > 0:
            left -= 1
        if right - left > degree or left == 0 and right == len(matrix) - 1:
            break
        if right < len(matrix) - 1:
            right += 1
    if matrix[left][0] == matrix[left - 1][0]:
        left -= 1
        right -= 1
    return left, right - 1

def get_diff_matrix(matrix, rng):
    diff_matrix = [[], []]
    der_matrix = []
    for i in range(rng[0], rng[1] + 1):
        diff_matrix[0].append(matrix[i][0])
        diff_matrix[1].append(matrix[i][1])
        der_matrix.append(matrix[i][2])
    for i in range(1, rng[1] - rng[0] + 1):
        row = []
        for j in range(rng[1] - rng[0] - i + 1):
            if diff_matrix[0][j] - diff_matrix[0][j + i] == 0:
                row.append(der_matrix[j])
                continue
            row.append(
                (diff_matrix[i][j] - diff_matrix[i][j + 1])
                / (diff_matrix[0][j] - diff_matrix[0][j + i])
            )
        diff_matrix.append(row)
    return diff_matrix

def print_diff_matrix(matrix):
    i = 0
    while i < len(matrix[0]):
        for row in matrix:
            if i < len(row):
                print(f'{row[i]:2.5f}   ', end='')
        i += 1
        print()


def polynom(matrix, degree, arg):
    rng = get_range(matrix, degree, arg)
    diffs_table = get_diff_matrix(matrix, rng)
    # print("Range:", rng)
    print_diff_matrix(diffs_table)
    print('-------------------------------------------------------')
    mul = 1
    val = diffs_table[1][0]
    for i in range(2, len(diffs_table)):
        mul *= (arg - diffs_table[0][i - 2])
        val += diffs_table[i][0] * mul
    return val


def calc_root(diffs_table, arg):
    val = diffs_table[1][0]
    mul = 1
    for i in range(2, len(diffs_table)):
        mul *= (arg - diffs_table[0][i - 2])
        val += diffs_table[i][0] * mul
    return val

def get_root(matrix, degree, arg):
    rng = get_range(matrix, degree, arg)
    diffs_table = get_diff_matrix(matrix, rng)
    # print("Range:", rng)
    print_diff_matrix(diffs_table)
    print('-------------------------------------------------------')
    mul = 1
    val = diffs_table[1][0]
    
    lo = diffs_table[0][0]
    hi = diffs_table[0][len(diffs_table[0]) - 1]
    while lo < hi:
        mid = (lo + hi)//2
        midval = calc_root(diffs_table, mid)
        if abs(midval) < 1e-7:
            return mid
        elif midval < 0:
            lo = mid + 1
        elif midval > 0:
            hi = mid
    return -1

def change_diff(matrix):
    new_matrix = []
    for row in matrix:
        if row[2] != 0:
            row[2] = 1 / row[2]
        else:
            row[2] = inf
        new_matrix.append(row)
    return new_matrix

def inf_filter(matrix):
    new_matrix = []
    for row in matrix:
        if row[2] != inf:
            new_matrix.append(row)
    return new_matrix

def main():
    inform = input_information()
    table, arg_val = inform[0], inform[1]
    table = sorted(table)
    ext_table = multiply_rows(table)
    newton_table = table
    # new_table = inf_filter(multiply_rows(change_diff(swap_columns(sorted(table)))))
    new_table = multiply_rows(sorted(table))
    for degree in range(1, 6):
        print("n = {}".format(degree))
        newton = polynom(table, degree, arg_val)
        hermite = polynom(ext_table, degree, arg_val)
        newton_root = get_root(newton_table, degree, 0)
        hermite_root = get_root(new_table, degree, 0)
        print_results(newton, hermite, newton_root, hermite_root)

if __name__ == "__main__":
    main()
