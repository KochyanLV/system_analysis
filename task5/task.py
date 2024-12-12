import numpy as np

def build_ranking_matrix(data):
    rankings = {}
    for idx, item in enumerate(data):
        if isinstance(item, list):
            for elem in item:
                rankings[elem] = idx
        else:
            rankings[item] = idx

    matrix = []
    for i in range(1, len(rankings) + 1):
        row = []
        for key in rankings:
            row.append(1 if rankings[key] >= rankings[i] else 0)
        matrix.append(row)

    return matrix

def compute_combined_matrix(matrix_a, matrix_b):
    matrix_a, matrix_b = np.array(matrix_a), np.array(matrix_b)
    combined_matrix = matrix_a * matrix_b
    combined_transpose = matrix_a.T * matrix_b.T
    result_matrix = np.logical_or(combined_matrix, combined_transpose)
    print(result_matrix)

def main(data_a, data_b):
    ranking_a = build_ranking_matrix(data_a)
    ranking_b = build_ranking_matrix(data_b)
    compute_combined_matrix(ranking_a, ranking_b)


data_a = [1, [2, 3], 4, [5, 6, 7], 8, 9, 10]
data_b = [[1, 3], [2, 4, 5], 6, 7, 9, [8, 10]]

if __name__ == "__main__":
    main(data_a, data_b)