import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import os
import glob
import matplotlib.pyplot as plt

'''
Key Notes:
Memory Efficiency: Sparse matrices use much less memory than dense matrices for storing large matrices with many zero elements.

Condition Number: Calculating the exact condition number for large sparse matrices might be impractical due to computational or memory constraints. Approximations or iterative methods might be more appropriate depending on the size and sparsity of your matrix.

Sparse Matrix Conversion: When necessary, converting a sparse matrix to a dense format (todense()) is used, but keep in mind that this can be very memory-intensive for large matrices.
'''


def visualize_sparse_matrix(sparse_matrix, filename):
    """
    Visualize a sparse matrix with an option to manually proceed to the next visualization.

    Args:
    sparse_matrix (sp.coo_matrix): A scipy COO sparse matrix.
    filename (str): The name of the file from which the matrix was read.

    Returns:
    A plot showing the non-zero entries of the sparse matrix, waits for user input to close.
    """
    fig, ax = plt.subplots(figsize=(10, 10))  # Create a figure and an axes.
    # Scatter plot of non-zero entries.
    ax.scatter(sparse_matrix.col, sparse_matrix.row, c=sparse_matrix.data, marker='s', s=100, cmap='viridis')
    ax.set_xlim(-1, sparse_matrix.shape[1])  # Set limits for x-axis.
    ax.set_ylim(-1, sparse_matrix.shape[0])  # Set limits for y-axis.
    ax.invert_yaxis()  # Invert the y-axis to match matrix indexing.
    ax.set_aspect('equal')  # Set aspect of the plot to be equal.
    ax.set_title(f'Non-zero entries of the Sparse Matrix from {filename}')  # Use the filename in the title.
    ax.set_xlabel('Column Index')
    ax.set_ylabel('Row Index')
    plt.colorbar(ax.collections[0], ax=ax, orientation='vertical', label='Value')  # Add a colorbar.
    plt.show(block=True)  # Display the plot and block execution until closed manually.


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


def compute_cond_num(filename, display=False):
    print(filename)
    sparse_matrix = read_matrix_from_file_and_create_sparse_matrix(filename)
    if display:
        visualize_sparse_matrix(sparse_matrix, filename)
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
    if int(file[-5])<4:
        compute_cond_num(file, display=0)