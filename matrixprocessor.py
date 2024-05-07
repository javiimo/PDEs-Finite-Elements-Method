import numpy as np

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Find the line that contains the matrix dimensions. It's typically after the description line.
    # We look for the first line with numeric content after the initial comments.
    for line in lines:
        if line.strip().startswith('#'):
            continue  # Skip comment lines
        header = line.strip().split()
        break
    
    # Assuming the first two numbers after the initial comments are `n` and `m`
    n = int(header[0])  # The first numeric item on the line
    m = int(header[1])  # The second numeric item on the line

    # Create an empty matrix of size n x m, initially with zeros
    matrix = np.zeros((n, m))

    # Process the matrix entries, starting from the next line after the dimensions
    data_start_index = lines.index(line) + 1
    for line in lines[data_start_index:]:
        if line.strip() and not line.startswith('#'):  # Skip empty and comment lines
            elements = line.split()
            i = int(elements[0])
            j = int(elements[1])
            value = float(elements[2])
            matrix[i, j] = value

    return matrix


# Specify the path to your text file
filename = 'A_matrix_CaseA_0.dat'
matrix = read_matrix_from_file(filename)

# Print the matrix to verify
np.set_printoptions(suppress=True, precision=2)  # Adjust print options for better readability
print(matrix)

