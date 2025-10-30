from bs_fdm import price_american
S0,K,r,sigma,T = 100.0,100.0,0.02,0.25,1.0
price, greeks, extra = price_american(S0,K,r,sigma,T,kind='put',scheme='cn',M=250,N=1500,return_full=True)
print(f'American Put (PSOR) price = {price:.4f}')
