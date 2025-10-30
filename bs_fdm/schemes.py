
import numpy as np

def build_implicit_tridiag(M, dt, r, sigma, scheme='implicit'):
    j = np.arange(1, M)
    alpha = 0.5*dt*(sigma*sigma*j*j - r*j)
    beta  = 1.0 - dt*(sigma*sigma*j*j + r)
    gamma = 0.5*dt*(sigma*sigma*j*j + r*j)
    if scheme == 'implicit':
        a = -alpha
        b = 1.0 - beta
        c = -gamma
    elif scheme == 'cn':
        a = -0.5*alpha
        b = 1.0 + 0.5*(1.0 - beta)
        c = -0.5*gamma
    else:
        raise ValueError('scheme must be implicit or cn')
    return a, b*np.ones(M-1), c

def explicit_step(V, dt, r, sigma, M, V0, VM):
    Vn = V.copy()
    j = np.arange(1, M)
    alpha = 0.5*dt*(sigma*sigma*j*j - r*j)
    beta  = 1.0 - dt*(sigma*sigma*j*j + r)
    gamma = 0.5*dt*(sigma*sigma*j*j + r*j)
    V[1:M] = alpha*Vn[0:M-1] + beta*Vn[1:M] + gamma*Vn[2:M+1]
    V[0], V[M] = V0, VM
    return V

def rhs_cn(Vn, dt, r, sigma, M, V0, VM):
    j = np.arange(1, M)
    alpha = 0.5*dt*(sigma*sigma*j*j - r*j)
    beta  = 1.0 - dt*(sigma*sigma*j*j + r)
    gamma = 0.5*dt*(sigma*sigma*j*j + r*j)
    rhs = alpha*Vn[0:M-1] + (1.0 - (1.0-beta))*Vn[1:M] + gamma*Vn[2:M+1]
    rhs[0]  += 0.5*(-alpha[0]) * V0
    rhs[-1] += 0.5*(-gamma[-1]) * VM
    return rhs
