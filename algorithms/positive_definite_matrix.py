import numpy as np
def positive_definite_matrix(matrix : np.array):
    
    if matrix.shape[0] == matrix.shape[1]:
        for index_column in range(matrix.shape[0]):
            col = matrix[ : , index_column]
            result = col.T @ matrix @ col
            if result < 0:
                return "is not positive definite matrix"

    return "is positive definite matrix"
