import numpy as np
import warnings
warnings.filterwarnings('ignore') # ignore nan warnings from evaluation metric

home = './btl/sample_data'

def target(P):
    n, Q = len(P), [0]
    for i in range(1, n):
        Q.append(P[i] / P[i -1] - 1)
    return Q

def evaluate(p, t):
    p, t = p[1 :], t[1 :]
    n, e, f = len(t), [], []
    for i in range(1, n):
        e.append(t[i] - p[i - 1])
        f.append(t[i])
    if not e: return 1.0, 0.0
    den = np.nanquantile(np.abs(e), 0.5) + 0.5 * np.nanquantile(np.abs(e), 0.9)
    num = np.nanquantile(np.abs(f), 0.5) + 0.5 * np.nanquantile(np.abs(f), 0.9)
    return den, 1 - den / num

def evaluate_strategy(c_array, limit):
    total_rel = 0
    count = 0
    pos_count = 0

    for i in range(1, 31):
        try:
            A = np.load(f'{home}/s{i}.npy', allow_pickle=True)
            P = A[:, 2]
            t = target(P)

            Q = [0] * len(P)
            rets = [0] * len(P)
            for k in range(1, len(P)):
                rets[k] = P[k] / P[k-1] - 1

            for k in range(len(P)):
                if k >= len(c_array):
                    val = 0
                    for j in range(len(c_array)):
                        val += rets[k-j] * c_array[j]

                    if val > limit: val = limit
                    elif val < -limit: val = -limit
                    Q[k] = val

            den, rel = evaluate(Q, t)
            total_rel += rel
            if rel > 0:
                pos_count += 1
            count += 1
        except Exception as e:
            pass

    avg_score = total_rel / count if count > 0 else 0
    return avg_score, pos_count

def run_grid_search(max_lags=10, limit=0.003, search_range=np.arange(-0.05, 0.051, 0.005)):
    print(f"Starting greedy grid search up to {max_lags} lags...")
    print(f"Using output clipping limit: {limit}\n")

    best_c_array = []

    for lag in range(1, max_lags + 1):
        print(f"--- Searching for optimal coefficient for lag {lag} ---")
        best_avg = -float('inf')
        best_c_for_this_lag = 0
        best_pos = 0

        for test_c in search_range:
            test_array = best_c_array + [test_c]
            avg_score, pos_count = evaluate_strategy(test_array, limit)

            if avg_score > best_avg:
                best_avg = avg_score
                best_c_for_this_lag = test_c
                best_pos = pos_count

        best_c_array.append(best_c_for_this_lag)
        print(f"Found best C{lag} = {best_c_for_this_lag:.3f} | Current Avg Score: {best_avg:.4f} | Positive on {best_pos}/30 stocks")
        print(f"Current c array: {[round(c, 3) for c in best_c_array]}\n")

    print("=== Final Optimal Array ===")
    print(f"c = {[round(c, 3) for c in best_c_array]}")

if __name__ == "__main__":
    run_grid_search()
