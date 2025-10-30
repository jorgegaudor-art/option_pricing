
import numpy as np
from .tridiag import thomas
from .schemes import build_implicit_tridiag, explicit_step, rhs_cn

def payoff_grid(S, K, kind):
    return np.maximum(S-K,0.0) if kind=='call' else np.maximum(K-S,0.0)

def boundaries(kind, K, r, t, T, Smax):
    tau = T - t
    if kind=='call':
        return 0.0, Smax - K*np.exp(-r*tau)
    else:
        return K*np.exp(-r*tau), 0.0

def setup_grid(S0, K, M, N, T, Smax_factor=4.0):
    Smax = Smax_factor*max(S0, K)
    S = np.linspace(0.0, Smax, M+1)
    dS = S[1]-S[0]
    dt = T/N
    return S, dS, dt, Smax

def greeks_from_grid(S, V, idx):
    if idx <= 0 or idx >= len(S)-1:
        return {'delta': float('nan'), 'gamma': float('nan'), 'theta': float('nan')}
    dS = S[idx+1]-S[idx-1]
    delta = (V[idx+1]-V[idx-1])/dS
    gamma = (V[idx+1]-2*V[idx]+V[idx-1]) / ((dS/2.0)**2)
    return {'delta': float(delta), 'gamma': float(gamma)}

def price_european(S0, K, r, sigma, T, kind='call', scheme='cn', M=200, N=1000,
                   Smax_factor=4.0, rannacher=True, return_full=False):
    S, dS, dt, Smax = setup_grid(S0, K, M, N, T, Smax_factor)
    V = payoff_grid(S, K, kind)  # at t = T
    for n in range(N, 0, -1):
        t = n*dt
        V0, VM = boundaries(kind, K, r, t, T, Smax)
        if scheme == 'explicit':
            V = explicit_step(V, dt, r, sigma, M, V0, VM)
        elif scheme in ('implicit','cn'):
            sch = 'implicit' if (rannacher and n in (N, N-1) and scheme=='cn') else scheme
            a,b,c = build_implicit_tridiag(M, dt, r, sigma, scheme=sch)
            if sch == 'implicit':
                rhs = V[1:M].copy()
            else:
                rhs = rhs_cn(V, dt, r, sigma, M, V0, VM)
            rhs[0]  -= a[0]*V0
            rhs[-1] -= c[-1]*VM
            V[1:M] = thomas(a, b, c, rhs)
            V[0], V[M] = V0, VM
        else:
            raise ValueError('scheme must be explicit, implicit or cn')
    price = float(np.interp(S0, S, V))
    idx = np.searchsorted(S, S0)
    g = greeks_from_grid(S, V, idx)
    if return_full:
        return price, g, {'S':S, 'V':V}
    return price, g

def psor(A_lower, A_diag, A_upper, rhs, payoff, omega=1.3, tol=1e-8, itmax=5000, V_init=None):
    n = len(rhs)
    V = payoff.copy() if V_init is None else V_init.copy()
    for it in range(itmax):
        err = 0.0
        for i in range(n):
            left  = A_lower[i-1]*V[i-1] if i>0 else 0.0
            right = A_upper[i]*V[i+1] if i<n-1 else 0.0
            Vi = (rhs[i] - left - right)/A_diag[i]
            Vi = (1-omega)*V[i] + omega*Vi
            Vi = max(Vi, payoff[i])
            err = max(err, abs(Vi - V[i]))
            V[i] = Vi
        if err < tol:
            return V, it+1, True
    return V, itmax, False

def price_american(S0, K, r, sigma, T, kind='put', scheme='cn', M=200, N=1000,
                   Smax_factor=4.0, omega=1.3, tol=1e-8, itmax=10000, return_full=False):
    S, dS, dt, Smax = setup_grid(S0, K, M, N, T, Smax_factor)
    V = payoff_grid(S, K, kind)  # at t = T
    for n in range(N, 0, -1):
        t = n*dt
        V0, VM = boundaries(kind, K, r, t, T, Smax)
        a,b,c = build_implicit_tridiag(M, dt, r, sigma, scheme=('implicit' if n in (N,N-1) and scheme=='cn' else scheme))
        if scheme=='cn':
            rhs = rhs_cn(V, dt, r, sigma, M, V0, VM)
        else:
            rhs = V[1:M].copy()
            rhs[0]  -= a[0]*V0
            rhs[-1] -= c[-1]*VM
        payoff_int = payoff_grid(S[1:M], K, kind)
        V_int, iters, ok = psor(a, b, c, rhs, payoff_int, omega=omega, tol=tol, itmax=itmax, V_init=V[1:M])
        V[1:M] = V_int
        V[0], V[M] = V0, VM
    price = float(np.interp(S0, S, V))
    idx = np.searchsorted(S, S0)
    g = greeks_from_grid(S, V, idx)
    if return_full:
        return price, g, {'S':S,'V':V}
    return price, g
