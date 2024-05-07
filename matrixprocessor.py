import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import os
import glob

'''
Key Notes:
Memory Efficiency: Sparse matrices use much less memory than dense matrices for storing large matrices with many zero elements.

Condition Number: Calculating the exact condition number for large sparse matrices might be impractical due to computational or memory constraints. Approximations or iterative methods might be more appropriate depending on the size and sparsity of your matrix.

Sparse Matrix Conversion: When necessary, converting a sparse matrix to a dense format (todense()) is used, but keep in mind that this can be very memory-intensive for large matrices.
'''

def read_matrix_from_file_and_create_sparse_matrix(filename):
    rows, cols, vals = [], [], []
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the line that contains the matrix dimensions. It's typically after the description line.
    for line in lines:
        if line.strip().startswith('#'):
            continue  # Skip comment lines
        header = line.strip().split()
        break

    data_start_index = lines.index(line) + 1
    for line in lines[data_start_index:]:
        if line.strip() and not line.startswith('#'):  # Skip empty and comment lines
            elements = line.split()
            rows.append(int(elements[0]))
            cols.append(int(elements[1]))
            vals.append(float(elements[2]))

    # Convert lists to numpy arrays
    rows = np.array(rows)
    cols = np.array(cols)
    vals = np.array(vals)
    
    # Dimensions are maximum indices plus 1
    n = max(rows) + 1
    m = max(cols) + 1

    # Create a COO sparse matrix
    matrix = sp.coo_matrix((vals, (rows, cols)), shape=(n, m))

    return matrix


def compute_cond_num(filename):
    print(filename)
    sparse_matrix = read_matrix_from_file_and_create_sparse_matrix(filename)
    
    # Compute the condition number using an approximation or conversion to dense matrix if feasible
    try:
        # Attempt to compute the condition number directly (feasible for smaller matrices)
        aux = sparse_matrix.todense()
        cond_number = np.linalg.cond(aux)
        print("EXACT Condition number of the matrix:", cond_number)
    except MemoryError:
        # If the matrix is too large, use an iterative method to approximate the condition number
        cond_number = spla.cond(sparse_matrix, p=None)# None implies 2-norm, which is generally used for condition numbers
        print("APPROXIMATE Condition number of the matrix:", cond_number)  


# Use glob to find all files matching the pattern
files = glob.glob('*.dat')
# Loop through the found files and delete them
for file in files:
    if int(file[-5])<3:
        compute_cond_num(file)