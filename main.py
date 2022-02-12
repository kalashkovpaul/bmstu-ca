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
    filename = input("Введите имя файла с данными: ")
    try:
        with open(filename) as file:
            matrix = [row.split() for row in file.readlines()]
        arg = float(input("Введите значение аргумента: "))
    except:
        print("Ошибка. Данные представлены в некорректном формате")
        exit()
    to_float(matrix)
    return matrix, arg

def print_results(newton, hermite, root):
    print("Ньютон: {:.6f}".format(newton))
    print("Эрмит: {:.6f}".format(hermite))
    print("Корень: {:.6f}".format(root))

def get_range(matrix, degree, arg):
    for right in range(len(matrix)):
        if matrix[right][0] > arg:
            break
    left = right
    while right - left < degree:
        if left > 0:
            left -= 1
        if right - left < degree:
            break
        if right < len(matrix) - 1:
            right += 1
    return left, right

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

def polynom(matrix, degree, arg):
    matrix.sort()
    rng = get_range(matrix, degree, arg)
    diffs_table = get_diff_matrix(matrix, rng)
    mul = 1
    val = diffs_table[1][0]
    for i in range(2, len(diffs_table)):
        mul *= arg - diffs_table[0][i - 2]
        val += diffs_table[i][0] * mul
    return val

def main():
    inform = input_information()
    table, arg_val = inform[0], inform[1]
    ext_table = multiply_rows(table)
    new_table = swap_columns(table)
    for degree in range(1, 6):
        print("n = {}".format(degree))
        newton = polynom(table, degree, arg_val)
        hermite = polynom(ext_table, degree, arg_val)
        root = polynom(new_table, degree, 0)
        print_results(newton, hermite, root)

if __name__ == "__main__":
    main()
