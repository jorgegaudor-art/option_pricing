
import numpy as np
from math import erf

def _phi(x: float) -> float:
    return 0.5*(1.0 + erf(x/np.sqrt(2.0)))

def price_bs(S, K, r, sigma, T, kind='call'):
    if T <= 0:
        return max(S-K,0.0) if kind=='call' else max(K-S,0.0)
    if sigma <= 0:
        fwd = S - K*np.exp(-r*T)
        return max(fwd,0.0) if kind=='call' else max(-fwd,0.0)
    d1 = (np.log(S/K) + (r + 0.5*sigma*sigma)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if kind=='call':
        return S*_phi(d1) - K*np.exp(-r*T)*_phi(d2)
    else:
        return K*np.exp(-r*T)*_phi(-d2) - S*_phi(-d1)

def greeks_bs(S, K, r, sigma, T, kind='call'):
    if T <= 0 or sigma<=0:
        eps = 1e-4*S if S>0 else 1e-4
        v_plus = price_bs(S+eps,K,r,sigma,T,kind)
        v_minus= price_bs(S-eps,K,r,sigma,T,kind)
        v     = price_bs(S,K,r,sigma,T,kind)
        delta = (v_plus - v_minus)/(2*eps)
        gamma = (v_plus - 2*v + v_minus)/(eps*eps)
        theta = (price_bs(S,K,r,sigma,T-1e-5,kind)-v)/(-1e-5)
        return {'delta':delta,'gamma':gamma,'theta':theta}
    d1 = (np.log(S/K) + (r + 0.5*sigma*sigma)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    pdf = np.exp(-0.5*d1*d1)/np.sqrt(2*np.pi)
    if kind=='call':
        delta = _phi(d1)
        theta = (-S*pdf*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*_phi(d2))
    else:
        delta = _phi(d1) - 1.0
        theta = (-S*pdf*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*_phi(-d2))
    gamma = pdf/(S*sigma*np.sqrt(T))
    return {'delta':float(delta),'gamma':float(gamma),'theta':float(theta)}
