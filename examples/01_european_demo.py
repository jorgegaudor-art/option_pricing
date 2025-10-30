from bs_fdm import price_european, price_bs
import numpy as np, matplotlib.pyplot as plt
S0,K,r,sigma,T = 100.0,100.0,0.02,0.20,1.0
price, greeks, extra = price_european(S0,K,r,sigma,T,kind='call',scheme='cn',M=250,N=1500,return_full=True)
bs = price_bs(S0,K,r,sigma,T,'call')
print(f'FD(CN)={price:.4f}  BS={bs:.4f}  | Delta={greeks['delta']:.4f}  Gamma={greeks['gamma']:.6f}')
S,V = extra['S'], extra['V']
plt.figure(); plt.plot(S,V,label='FD (t=0)'); plt.xlabel('S'); plt.ylabel('Option value');
plt.title('European Call: value vs S (CN + Rannacher)'); plt.grid(True); plt.legend(); plt.tight_layout();
plt.savefig('/mnt/data/adv_euro_value.png',dpi=140)
print('Saved /mnt/data/adv_euro_value.png')
