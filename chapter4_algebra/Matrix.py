def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0  # number of elements in first row
    return num_rows, num_cols


def get_row(A, i):
    return A[i]


def get_column(A, j):
    return [A_i[j] for A_i in A]


def make_matrix(num_rows, num_cols, entry_fn):
    """return a num_rows * num_cols matrix
    whose (i,j)th entry is entry_fn(i,j)"""
    return [[entry_fn(i, j)  # given i, create a list [entry_fn(i,0), ...], create one list for each i
             for j in range(num_cols)]
            for i in range(num_rows)]


# identity matrix (with 1s on the diagonal and 0s elsewhere)
def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0

identity_matrix = make_matrix(5,5,is_diagonal)
print(identity_matrix)