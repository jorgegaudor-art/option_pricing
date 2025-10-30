
import numpy as np

def thomas(a, b, c, d):
    n = len(d)
    ac, bc, cc, dc = map(np.array, (a, b, c, d))
    for i in range(1, n):
        mc = ac[i-1]/bc[i-1]
        bc[i] = bc[i] - mc*cc[i-1]
        dc[i] = dc[i] - mc*dc[i-1]
    xc = bc
    xc[-1] = dc[-1]/bc[-1]
    for i in range(n-2, -1, -1):
        xc[i] = (dc[i]-cc[i]*xc[i+1])/bc[i]
    return xc
