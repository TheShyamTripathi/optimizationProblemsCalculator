'''
T1:
Maximize: Z = 40x1 + 30x2
Subject to: x1 + x2 <= 12
2x1 + x2 <= 16
x1 >= 0, x2 >= 0
solution:
x1 = 4.0
x2 = 8.0
Objective function value: 400.0
'''

'''
T2:
Maximize Z=3x1+2x2+4x3+x4
subject to:
2x1+3x2+x3+4x4<=8
x1+4x2+2x3+5x4<=10
3x1+x2+2x3+3x4<=7
x1,x2,x3,x4>=0
solution:
x1 = 0
x2 = 0
x3 = 3.5
x4 = 0
Objective function value: 14.0
'''

'''
MAX Z = x1 + 2x2 + 3x3 - x4
subject to
x1 + 2x2 + 3x3 +0x4= 15
2x1 + x2 + 5x3 +0x4= 20
x1 + 2x2 + x3 + x4 = 10
and x1,x2,x3,x4 >= 0 
solution:
x1=2.5,x2=2.5,x3=2.5,x4=0
Max Z=15
'''

'''
unbounded solution 
MAX Z = 2x1 + 3x2
subject to
x1 + x2 >= 5
-x1 + x2 >= 2
and x1,x2 >= 0
#convert it into < symbols
solution:
the solution to the given problem is unbounded.
'''

'''
INFESIBLE SOLUTION
MAX Z = 4x1 + 5x2
subject to
3x1 + 2x2 <= 4
x1 - 2x2 >= 3
x1 + x2 <= 1
and x1,x2 >= 0 
solution:
infeasible solution
'''

def print_table(table, num_vars, num_constraints):
    print(f"{'Basic Variables':<15}|", end="")
    for j in range(num_vars):
        print(f"x{j + 1:<10} ", end="")
    for i in range(num_constraints):
        print(f"S{i + 1:<10} ", end="")
    print("RHS")
    print("-" * 60)

    for i in range(len(table)):
        if i < num_constraints:
            print(f"Constraint {i + 1:<15}|", end="")
        else:
            print("Objective Function |", end="")
        for j in range(len(table[i]) - 1):
            print(f"{table[i][j]:<10.3f} ", end="")
        print(f"{table[i][-1]:<10.3f}")
    print("-" * 60)

def find_pivot_column(table, is_maximize):
    pivot_col = 0
    for i in range(1, len(table[0]) - 1):
        if (is_maximize and table[-1][i] < table[-1][pivot_col]) or \
           (not is_maximize and table[-1][i] > table[-1][pivot_col]):
            pivot_col = i
    return pivot_col

def find_pivot_row(table, pivot_col):
    pivot_row = -1
    min_ratio = float('inf')
    for i in range(len(table) - 1):
        if table[i][pivot_col] > 0:
            ratio = table[i][-1] / table[i][pivot_col]
            if ratio < min_ratio:
                min_ratio = ratio
                pivot_row = i
    return pivot_row

def check_degeneracy(table):
    return any(row[-1] == 0 for row in table[:-1])

def check_multiple_solutions(table, num_vars):
    for j in range(num_vars):
        if table[-1][j] == 0 and all(table[i][j] == 0 for i in range(len(table) - 1)):
            return True
    return False

def check_infeasibility(table, num_constraints):
    # Infeasibility occurs if there's an artificial variable with a non-zero value in the final solution.
    return any(row[-1] < 0 for row in table[:num_constraints])

def pivot(table, pivot_row, pivot_col):
    pivot_value = table[pivot_row][pivot_col]
    table[pivot_row] = [x / pivot_value for x in table[pivot_row]]

    for i in range(len(table)):
        if i != pivot_row:
            factor = table[i][pivot_col]
            table[i] = [table[i][j] - factor * table[pivot_row][j] for j in range(len(table[i]))]

def simplex_method(table, is_maximize, num_vars, num_constraints):
    iteration = 0

    while True:
        print(f"Iteration {iteration + 1}:")
        print_table(table, num_vars, num_constraints)

        if check_degeneracy(table):
            print("Degenerate solution detected.")

        pivot_col = find_pivot_column(table, is_maximize)
        if (is_maximize and table[-1][pivot_col] >= 0) or \
           (not is_maximize and table[-1][pivot_col] <= 0):
            print("Optimal solution found.")
            if check_multiple_solutions(table, num_vars):
                print("Multiple solutions exist.")
            break

        pivot_row = find_pivot_row(table, pivot_col)
        if pivot_row == -1:
            print("Unbounded solution detected.")
            return

        pivot(table, pivot_row, pivot_col)
        iteration += 1

        # Check infeasibility
        if check_infeasibility(table, num_constraints):
            print("Infeasible solution detected.")
            return

    print("Final solution:")
    print_table(table, num_vars, num_constraints)

    variable_values = [0] * num_vars
    for i in range(num_constraints):
        for j in range(num_vars):
            if table[i][j] == 1 and all(table[k][j] == 0 for k in range(num_constraints) if k != i):
                variable_values[j] = table[i][-1]

    print("\nValues of decision variables:")
    for i in range(num_vars):
        print(f"x{i + 1} = {variable_values[i]}")
    print(f"Objective function value: {table[-1][-1]}")

def main():
    num_vars = int(input("Enter the number of variables: "))
    num_constraints = int(input("Enter the number of constraints: "))

    # Initialize the table with zeros
    table = [[0] * (num_vars + num_constraints + 1) for _ in range(num_constraints + 1)]

    print("Enter the coefficients of the constraints:")
    for i in range(num_constraints):
        print(f"Constraint {i + 1} coefficients:")
        table[i][:num_vars] = list(map(float, input().split()))
        table[i][num_vars + i] = 1  # Add slack variable
        table[i][-1] = float(input("Enter the RHS value for this constraint: "))

    print("Enter the coefficients of the objective function:")
    table[-1][:num_vars] = list(map(float, input().split()))

    choice = input("Do you want to (M)aximize or (m)inimize the objective function? ").strip()
    is_maximize = choice.lower() == 'm'

    if is_maximize:
        table[-1][:num_vars] = [-x for x in table[-1][:num_vars]]

    simplex_method(table, is_maximize, num_vars, num_constraints)

if _name_ == "_main_":
    main()
