import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

home = './btl/sample_data'
COL_pv = ['date', 'opn', 'cls', 'low', 'high', 'nsh', 'vol', 'adj']

stk = 's1'
A = np.load(f"{home}/{stk}.npy", allow_pickle=True)
P, V = A[:, 2], A[:, 6]

# customize your prediction
def prediction(P, V):
    c = [0.036, -0.041, 0.005, -0.010, 0.025, -0.025, 0.000, -0.005, -0.010, -0.005]

    Q = [0] * len(P)
    rets = [0] * len(P)
    for i in range(1, len(P)):
        rets[i] = P[i] / P[i-1] - 1

    limit = 0.003
    for i in range(len(P)):
        if i >= len(c):
            val = 0
            for j in range(len(c)):
                val += rets[i-j] * c[j]

            if val > limit: val = limit
            elif val < -limit: val = -limit
            Q[i] = val

    return Q

# keep the core function unchanged
def target(P, V):
    n, Q = len(P), [0]
    for i in range(1, n):
        Q.append(P[i] / P[i -1] - 1)
    return Q

def evaluate(p, t, dspl=False):
    p, t = p[1 :], t[1 :]
    n, e, f = len(t), [], []
    for i in range(1, n):
        e.append(t[i] - p[i - 1])
        f.append(t[i])
    den = np.nanquantile(np.abs(e), 0.5) + 0.5 * np.nanquantile(np.abs(e), 0.9)
    num = np.nanquantile(np.abs(f), 0.5) + 0.5 * np.nanquantile(np.abs(f), 0.9)
    if dspl == True:
        print(f"\n\tbase = {round(num, 3)}  |  abs = {round(den, 3)}  |  rel = {round(1 - den / num, 3)}\n")
        plt.hist(e, edgecolor='black')
        plt.show()
    else:
        return den, 1 - den / num
    
p, t = prediction(P, V), target(P, V)
evaluate(p, t, False)