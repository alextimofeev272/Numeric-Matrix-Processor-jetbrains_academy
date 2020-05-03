import copy


class Matrix:
    def __init__(self, demension, numbers):
        self.lst = numbers
        self.m = demension[0]
        self.n = demension[1]
        self.dimension = (self.m, self.n)

    def input_matrix(self):
        for i in range(self.m):
            self.lst.append([])
            for j in input().split(" "):
                self.lst[i].append(float(j))

    def __str__(self):
        """вывод матрицы"""
        _str = ''
        for i in self.lst:
            for j in i:
                _str += f"{j} "
            _str += "\n"
        return _str

    def __add__(self, other):
        """сложение матриц"""
        if self.dimension == other.dimension:
            a = []
            for i, j in zip(self.lst, other.lst):
                b = []
                for k, m in zip(i, j):
                    b.append(k + m)
                a.append(b)
            return Matrix(self.dimension, a)
        else:
            return "The operation cannot be performed"

    def __mul__(self, other):
        """умножение матриц"""
        if type(other) == int or type(other) == float:
            mul_matrix_list = [[j * other for j in i] for i in self.lst]
            return Matrix(self.dimension, mul_matrix_list)
        else:
            if self.dimension[1] == other.dimension[0]:
                mul_matrix_list = [[0] * other.dimension[1] for j in range(self.dimension[0])]
                for i in range(len(mul_matrix_list)):
                    for j in range(len(mul_matrix_list[i])):
                        for k in range(self.dimension[1]):
                            mul_matrix_list[i][j] += self.lst[i][k] * other.lst[k][j]
                return Matrix([self.dimension[0], other.dimension[1]], mul_matrix_list)
            else:
                return "The operation cannot be performed"

    def transponse_main_diagonal(self):
        """Транспонирование матрицы"""
        transponse_matrix_list = [[0] * self.dimension[0] for i in range(self.dimension[1])]
        for j in range(self.dimension[0]):
            for i in range(self.dimension[1]):
                transponse_matrix_list[i][j] = self.lst[j][i]
        return Matrix(self.dimension, transponse_matrix_list)

    def transponse_side_diagonal(self):
        """Транспонирование матрицы"""
        transponse_matrix_list = [[0] * self.dimension[0] for i in range(self.dimension[1])]
        for j in range(self.dimension[0]):
            m = self.m - 1 - j
            n = self.n - 1 - j
            for i in range(self.dimension[1]):
                transponse_matrix_list[j][i] = self.lst[j + m][i + n]
                m -= 1
                n -= 1
        return Matrix(self.dimension, transponse_matrix_list)

    def transponse_vertical(self):
        """Транспонирование матрицы"""
        transponse_matrix_list = [[0] * self.dimension[0] for i in range(self.dimension[1])]
        for j in range(self.dimension[0]):
            for i in range(self.dimension[1]):
                transponse_matrix_list[j][i] = self.lst[j][-i - 1]
        return Matrix(self.dimension, transponse_matrix_list)

    def transponse_horizontal(self):
        """Транспонирование матрицы"""
        transponse_matrix_list = [[0] * self.dimension[0] for i in range(self.dimension[1])]
        for j in range(self.dimension[0]):
            for i in range(self.dimension[1]):
                transponse_matrix_list[i][j] = self.lst[-i - 1][j]
        return Matrix(self.dimension, transponse_matrix_list)

    def delete_string(self, k):
        for i in range(self.n):
            if i == (k - 1):
                self.lst.pop(i)
        return Matrix([self.m, self.n - 1], self.lst)

    def delete_column(self, l):
        for i in self.lst:
            for j in range(self.m):
                if j == (l - 1):
                    i.pop(j)
        return Matrix([self.m - 1, self.n], self.lst)

    def determinate(self, l=1):
        if self.dimension == (1, 1):
            return self.lst[0][0]
        elif self.dimension == (2, 2):
            return self.lst[0][0] * self.lst[1][1] - self.lst[1][0] * self.lst[0][1]
        else:
            matrix1 = Matrix(self.dimension, self.lst)
            determinate_ = 0
            k = 1
            for i in range(1, matrix1.dimension[1] + 1):
                matrix2 = copy.deepcopy(matrix1)
                matrix2 = matrix2.delete_column(i)
                matrix2 = matrix2.delete_string(l)
                determinate_ += k * matrix1.lst[0][i - 1] * matrix2.determinate()
                k = -k
            return determinate_

    def adjugate(self):
        new_lst = []
        for i in range(1, self.m+1):
            new_lst.append([])
            for j in range(1, self.n+1):
                matrix2 = copy.deepcopy(Matrix(self.dimension, self.lst))
                matrix2 = matrix2.delete_string(i)
                matrix2 = matrix2.delete_column(j)
                new_lst[i-1].append(((-1)**(i+j))*matrix2.determinate())
        return Matrix(self.dimension, new_lst).transponse_main_diagonal()

    def invertible(self):
        if self.determinate() == 0:
            return f"This matrix doesn't have an inverse."
        else:
            return self.adjugate() * (1/self.determinate())


def menu():
    def matrix_input(name):
        dimension = input(f"Enter size of{name} matrix: ")
        lst = [int(j) for j in dimension.split(" ")]
        matrix = Matrix(lst, [])
        print(f"Enter{name} matrix:")
        matrix.input_matrix()
        return matrix

    menu_ = {1: "Add matrices",
             2: "Multiply matrix by a constant",
             3: "Multiply matrices",
             4: "Transpose matrix",
             5: "Calculate a determinant",
             6: "Inverse matrix",
             0: "Exit"}
    for i in menu_.items():
        print(f"{i[0]}. {i[1]}")
    number_menu = int(input("Your choice: "))
    if number_menu == 0:
        exit()
    elif number_menu == 1:
        print(f"The result is:\n{matrix_input(' first') + matrix_input(' second')}")
    elif number_menu == 2:
        print(f"The result is:\n{matrix_input('') * float(input('Enter constant: '))}")
    elif number_menu == 3:
        print(f"The result is:\n{matrix_input(' first') * matrix_input(' second')}")
    elif number_menu == 4:
        print("""1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line""")
        number_menu2 = int(input("Your choice: "))
        if number_menu2 == 1:
            print(f"The result is:\n{matrix_input('').transponse_main_diagonal()}")
        elif number_menu2 == 2:
            print(f"The result is:\n{matrix_input('').transponse_side_diagonal()}")
        elif number_menu2 == 3:
            print(f"The result is:\n{matrix_input('').transponse_vertical()}")
        elif number_menu2 == 4:
            print(f"The result is:\n{matrix_input('').transponse_horizontal()}")
    elif number_menu == 5:
        print(f"The result is:\n{matrix_input('').determinate()}")
    elif number_menu == 6:
        print(f"The result is:\n{matrix_input('').invertible()}")


while True:
    menu()

