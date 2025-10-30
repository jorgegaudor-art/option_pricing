from bs_fdm import price_european, price_bs
from bs_fdm.analytics import convergence_table
S0,K,r,sigma,T = 100.0,100.0,0.02,0.20,1.0
def runner(M,N):
    p,g = price_european(S0,K,r,sigma,T,kind='call',scheme='cn',M=M,N=N)
    return p,g
rows = convergence_table(lambda M,N: runner(M,N), {'S0':S0,'K':K,'r':r,'sigma':sigma,'T':T,'kind':'call'}, Ms=[80,120,180,260], Ns=[400,900,1600,2500])
for r in rows: print(r)
