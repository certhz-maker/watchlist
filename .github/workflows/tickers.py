#!/usr/bin/env python3
"""
Lista UNICA dei ticker della watchlist — fonte di verita' unica.
La modifichi QUI e basta: la importano sia export_1H_yfinance.py (snapshot live)
sia export_daily_yfinance.py (export daily 18 mesi).

NB: questo file deve stare nella STESSA cartella dei due script .py.
"""

TICKERS = [
    # --- posizioni in carico ---
    "AMPG", "CPSH", "OPEN", "RDW", "SMR",
    # --- vari ---
    "BBAI",  "IREN", "CIFR", "NXDR",      
    # --- spazio  ---
    "ASTS", "FLY",  "PL", "SIDU", "BKSY", "SATL", "SPIR", "VOYG", "VELO", "MNTS",
    # --- uranio ---
    "OKLO", "SMR", "UUUU",   
    # --- quantum ---
    "LAES","IONQ", "QBTS", "QBTS","ARQQ",  
    # --- tec ---
    "AMD","MRVL", "PLTR", "NVDA",    
    # "POET",   # CONGELATO (gate class action) — scommenta solo se riattivato
]
