from bs_fdm import price_european, price_bs
def test_european_call_close_to_bs():
    S0,K,r,sigma,T = 100.0,100.0,0.02,0.20,1.0
    price, greeks = price_european(S0,K,r,sigma,T,kind='call',scheme='cn',M=220,N=2000)
    ref = price_bs(S0,K,r,sigma,T,'call')
    assert abs(price - ref) < 0.5
