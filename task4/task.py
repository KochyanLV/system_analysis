import numpy as np
from math import log2

def compute_entropy(probabilities):
    entropy = 0
    for prob in np.nditer(probabilities):
        if prob > 0:
            entropy -= prob * log2(prob)
    return entropy

def analyze_data(input_matrix):
    data_matrix = np.array(input_matrix)
    total_purchases = data_matrix.sum()
    prob_matrix = data_matrix / total_purchases

    p_y = prob_matrix.sum(axis=1)
    p_x = prob_matrix.sum(axis=0)

    H_XY = compute_entropy(prob_matrix)
    H_Y = compute_entropy(p_y)
    H_X = compute_entropy(p_x)

    conditional_prob_matrix = np.copy(prob_matrix)
    total_conditional_entropy = 0

    for i in range(len(prob_matrix)):
        conditional_prob_matrix[i] /= p_y[i]
        conditional_entropy = compute_entropy(conditional_prob_matrix[i])
        total_conditional_entropy += conditional_entropy * p_y[i]

    information_content = H_X - total_conditional_entropy
    H_XY_calculated = H_Y + total_conditional_entropy

    print(f"Information quantity I(X,Y): {round(information_content, 2)}")
    print(f"Joint entropy H(XY): {round(H_XY_calculated, 2)} (calculated both ways)")

test_data = [[20, 15, 10, 5],
             [30, 20, 15, 10],
             [25, 25, 20, 15],
             [20, 20, 25, 20],
             [15, 15, 30, 25]]

if __name__ == "__main__":
    analyze_data(test_data)
