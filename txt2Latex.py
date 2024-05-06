'''
This file takes the .txt output of FreeFEM++ and generates latex tables with errors and convergence rate
'''

import os

def parse_errors(file_content):
    """
    Parses the file content and extracts errors and convergence rates.
    """
    lines = file_content.split('\n')
    data = {}
    convergence_data = {}
    current_h = None

    for line in lines:
        line = line.strip()
        if line.startswith('FOR h ='):
            current_h = line.split('=')[1].strip()
            data[current_h] = {}
        elif 'errInf' in line or 'errL2' in line or 'errL2Grad' in line:
            key, value = line.split('=')
            data[current_h][key.strip()] = float(value.strip())
        elif 'convergence rate' in line:
            key, value = line.split('=')
            convergence_data[key.strip()] = float(value.strip())

    return data, convergence_data

def generate_latex_table(data, convergence_data):
    """
    Generates a LaTeX table from the parsed data.
    """
    latex = "\\begin{tabular}{|c|c|c|c|}\n\\hline\n"
    latex += "h & $\\| \\Pi_h^1 u - u_h \\|_{L^\\infty (\\Omega)}$ & $\\|\\Pi_h^1 u - u_h \\|_{L^2 (\\Omega)}$ & $\\|\\nabla (\\Pi_h^1 u - u_h) \\|_{L^2 (\\Omega)}$ \\\\\n\\hline\n"
    for h in sorted(data, key=lambda x: float(x.split('/')[1])):
        h_data = data[h]
        latex += f"{h} & {h_data.get('errInf', 'N/A')} & {h_data.get('errL2', 'N/A')} & {h_data.get('errL2Grad', 'N/A')} \\\\\n"
    latex += "\\hline\n"
    latex += f"Convergence Rates & {convergence_data.get('convergence rate Inf', 'N/A')} & {convergence_data.get('convergence rate L2', 'N/A')} & {convergence_data.get('convergence rate L2Grad', 'N/A')} \\\\\n"
    latex += "\\hline\n\\end{tabular}\n"
    return latex

# Get the directory where the current script is located
directory = os.path.dirname(os.path.abspath(__file__))

# Collecting all text files and processing them
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as file:
            file_content = file.read()
            data, convergence_data = parse_errors(file_content)
            latex_output = generate_latex_table(data, convergence_data)
            print(f"LaTeX table for {filename}:\n{latex_output}\n")

