#substring DP
import numpy as np

def multiply_recur(chain):
    return _multiply_recur(zip(chain, chain[1:]))
#k = 0
#from the var k - its O(3^N). Cant work out how
def _multiply_recur(matrices):
    #global k
    #k += 1
    if len(matrices) == 1:
        return (0, matrices[0], matrices[0])
    min_ = None
    costs = []
    for i in range(1, len(matrices)):
        m1, m2= _multiply_recur(matrices[:i]), _multiply_recur(matrices[i:])
        (rows_m1, cols_m1), (rows_m2, cols_m2) = m1[1], m2[1]
        cost = m1[0] + m2[0] + rows_m1 * cols_m1 * cols_m2
        costs.append(cost)
        if not min_ or cost < min_[0]:
            min_ = (cost, (rows_m1, cols_m2), (m1, m2))
    return min_

def rep(res):
    return (("(%s * %s)" % (rep(res[2][0]), rep(res[2][1]))) if res[0]
            else "%s x %s" % res[2])
            
def multiply_dp(chain):
    n = len(chain) - 1
    dp_table = np.zeros((n, n))

    dp_table = [[None for i in range(n)] for j in range(n)]
    for i in range(n):
        matrix_dims = (chain[i], chain[i + 1])
        dp_table[i][i] = (0, matrix_dims, matrix_dims)
    #for k in range(n): iterate matrix traingle including diagonal
    #    for i in range(n -  k):
    #        print i,(i + k)

    #iterate excluding diagonal
    for k in range(n - 1):
        for i in range(n - k - 1):
            j=i+k+1
            choices = []
            m = k + 2
            for l in range(1, m):
                    m1, m2 = dp_table[i][j - l], dp_table[i + m - l][j]
                    (rows_m1, cols_m1), (rows_m2, cols_m2) = m1[1], m2[1]
                    choices.append((m1[0] + m2[0] + rows_m1 * cols_m1 * cols_m2,
                                      (rows_m1, cols_m2), (m1, m2)))
            
            dp_table[i][j] = min(choices)
            
    return dp_table[0][n - 1]
             
    
############################## TESTS ##############################
import pytest

@pytest.mark.parametrize('algorithm', [multiply_recur, multiply_dp])
@pytest.mark.parametrize(('input', 'expected'), [
    ([10, 100, 5, 50, 1], (1750, (10, 1),
                           '(10 x 100 * (100 x 5 * (5 x 50 * 50 x 1)))')),    
    ([10, 100, 5, 50], (7500, (10, 50), '((10 x 100 * 100 x 5) * 5 x 50)')),    
    ([30, 35, 15, 5, 10, 20, 25],
     (15125, (30, 25),
      '((30 x 35 * (35 x 15 * 15 x 5)) * ((5 x 10 * 10 x 20) * 20 x 25))'))])

def should_matrix_chain_multiply_optimal(input, expected, algorithm):
#    global k
#    k = 0
    res = algorithm(input)
    #print expected, (res[0], res[1], rep(res)), res
    assert expected == (res[0], res[1], rep(res))
    #if algorithm == multiply_recur:
 #       print k, len(input) - 1
    #    assert 0