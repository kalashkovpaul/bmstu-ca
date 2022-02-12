import numpy as np
from table import *

def divided_difference(xs, ys, n):
    def _dd(yi, yj, xi, xj):
        denom = 1e-12 if xi == xj else xi - xj
        return (yi - yj) / denom
    dd = np.zeros((n, n))
    for i in range(n):
        dd[i][0] = _dd(ys[i], ys[i + 1], xs[0], xs[1])
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = _dd(dd[i][j - 1], dd[i + 1][j - 1], xs[i], xs[i + j + 1])
    return dd

def lower_bound(lst, key):
    left = -1
    right = len(lst)
    while left + 1 < right:
        middle = (left + right) // 2
        if lst[middle] >= key:
            right = middle
        else:
            left = middle
    return right

def nodes(xs, ys, n, x):
    s = [[xs[i], ys[i]] for i in range(len(xs))]
    s = np.array(sorted(s, key=lambda x: x[0]))
    xs, ys = s[:,0], s[:,1]
    xm = lower_bound(xs, x)
    rh = n // 2
    lh = n - rh
    
    start = xm - lh
    stop = xm + rh

    if start < 0:
        stop -= start
        start = 0
    elif stop >= len(xs):
        start -= stop - len(xs) + 1
        stop = len(xs) - 1
    
    return xs[start:stop+1], ys[start:stop+1]

def newton_polynomial(xs, ys, n, x):
    xs, ys = nodes(xs, ys, n, x)
    dd = divided_difference(xs, ys, n)
    xc, y = 1, ys[0]
    for i in range(n):
        xc *= x - xs[i]
        y += xc * dd[0][i]
    return y

def print_title(title):
    print('─' * 4, title, '─' * (80 - 4 - 1 - len(title) - 1))

z = 0
def assign_z_to(value):
    global z
    z = value

def spline_interpolation(xs, ys, x):
    j = lower_bound(xs, x)

    n = len(xs)
    h = np.zeros((n))
    A = np.zeros((n))
    B = np.zeros((n))
    D = np.zeros((n))
    F = np.zeros((n))
    a = np.zeros((n))
    b = np.zeros((n))
    c = np.zeros((n + 1))
    d = np.zeros((n))
    xi = np.zeros((n + 1))
    eta = np.zeros((n + 1))

    for i in range(1, n):
        h[i] = xs[i] - xs[i-1]

    for i in range(2, n):
        A[i] = h[i-1]
        B[i] = -2 * (h[i-1] + h[i])
        D[i] = h[i]
        F[i] = -3 * ((ys[i] - ys[i-1]) / h[i] - (ys[i-1] - ys[i-2]) / h[i-1])

    for i in range(2, n):
        xi[i+1] = D[i] / (B[i] - A[i] * xi[i])
        eta[i+1] = (A[i] * eta[i] + F[i]) / (B[i] - A[i] * xi[i])

    for i in range(n - 2, -1, -1):
        c[i] = xi[i] * c[i+1] + eta[i+1]

    for i in range(1, n):
        a[i] = ys[i-1]
        b[i] = (ys[i] - ys[i-1]) / h[i] - h[i] / 3 * (c[i+1] + 2 * c[i])
        d[i] = (c[i+1] - c[i]) / (3 * h[i])

    return a[j] \
         + b[j] * (x - xs[j-1]) \
         + c[j] * ((x - xs[j-1]) ** 2) \
         + d[j] * ((x - xs[j-1]) ** 3)

def main():
    print_title('List of tables')
    list_tables()

    print_title('Menu:')
    filename = input('Input filename: ')
    title, xs, ys = load_table(filename)

    print_title('Table:')
    print_table(title, xs, ys)

    print_title('Menu:')
    x = float(input('Input x: '))

    y = spline_interpolation(xs, ys, x)
    eval('assign_z_to({})'.format(title))

    ae = fabs(z - y)
    re = ae / fabs(z)

    print('Interpolated value: {:.3f}'.format(y))
    print('Real value        : {:.3f}'.format(z))
    print('Absolute error    : {:.3f}'.format(ae))
    print('Relative error    : {:.3f}'.format(re))

# def main():
#     print_title('List of tables:')
#     list_tables()
    
#     print_title('Menu:')
#     filename = input('Input filename: ')
#     title, xs, ys = load_table(filename)

#     print_title('Table:')
#     print_table(title, xs, ys)

#     print_title('Menu:')
#     x = float(input('Input x: '))
#     n = int(input('Input n: '))

#     y = newton_polynomial(xs, ys, n, x)
#     if 'x' in title:
#         eval('assign_z_to({})'.format(title))
#     else:
#         global z
#         z = float(title)

#     ae = fabs(z - y)
#     re = ae / fabs(z)

#     print('Interpolated value: {:.3f}'.format(y))
#     print('Real value        : {:.3f}'.format(z))
#     print('Absolute error    : {:.3f}'.format(ae))
#     print('Relative error    : {:.3f}'.format(re))

if __name__ == '__main__':
    main()

