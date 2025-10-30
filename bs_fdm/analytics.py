
import time, numpy as np
from .bs_closed import price_bs

def relative_error(x, ref):
    return abs(x-ref)/max(1.0, abs(ref))

def convergence_table(price_fn, params, Ms, Ns):
    rows = []
    ref = price_bs(params['S0'], params['K'], params['r'], params['sigma'], params['T'], params.get('kind','call'))
    for M,N in zip(Ms, Ns):
        t0 = time.time()
        price, greeks = price_fn(M=M, N=N)
        dt = time.time()-t0
        err = abs(price-ref)
        rows.append({'M':M,'N':N,'price':price,'ref':ref,'abs_err':err,'time_s':dt})
    for i in range(2, len(rows)):
        if rows[i-1]['abs_err']>0 and rows[i]['abs_err']>0:
            ratio = rows[i-1]['abs_err']/rows[i]['abs_err']
            rows[i]['order_est'] = np.log2(ratio)
        else:
            rows[i]['order_est'] = float('nan')
    return rows
