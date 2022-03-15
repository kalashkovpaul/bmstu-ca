import numpy as np

def function(x, y, z):
    # if (abs(x + y) <=  1e-5):
    #     return 1e6
    # return 1 / (x + y) - z
    return np.exp(2 * x - y) * z**2

def main():

    file = open("./lab_02/data", "w")
    xmin, ymin, zmin = map(float, input("Минимальные значения (x, y, z): ").split())
    xmax, ymax, zmax = map(float, input("Максимальные значения (x, y, z): ").split())
    xn, yn, zn = map(float, input("Шаг (x, y, z): ").split())
    xd = (xmax - xmin) / xn
    yd = (ymax - ymin) / yn
    zd = (zmax - zmin) / zn
    z = zmin
    while (z <= zmax):
        file.write("    " * int((zmax - zmin) / zn) + f"z={z}\n")
        file.write("y\\x ")
        x = xmin
        while (x <= xmax):
            file.write(f"{x} ")
            x += xd
        file.write("\n")
        y = ymin
        while (y <= ymax):
            file.write(f"{y} ")
            x = xmin
            while (x <= xmax):
                file.write(f"{function(x, y, z)} ")
                x += xd
            file.write("\n")
            y += yd
        file.write("\n\n")
        z += zd
    file.close()

if __name__ == "__main__":
    main()
