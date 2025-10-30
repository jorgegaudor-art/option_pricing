# Finite-Difference Option Pricing (Black-Scholes) — Advanced, Interview-Ready

A clean, modular PDE solver for vanilla options under Black–Scholes featuring:
- Explicit, Implicit and Crank–Nicolson (default) time stepping
- Rannacher smoothing for payoff kink
- PSOR solver for American options (LCP formulation)
- Greeks from the grid (Delta, Gamma, Theta)
- Richardson extrapolation & convergence study (accuracy vs runtime)
- Example plots & unit tests

> Design goal: production-quality clarity you can explain in an interview, with minimal code size and strong validation.
