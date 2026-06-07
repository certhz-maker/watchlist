#!/usr/bin/env python3
"""
Export OHLC 60m (ORARIO) split-adjusted per la watchlist.
Output: UN SOLO CSV consolidato (formato long) -> 60m.csv
        colonne: Ticker, Datetime, Open, High, Low, Close, Volume
        Il file viene SOVRASCRITTO a ogni esecuzione.
Requisiti:  pip install yfinance pandas
Uso:        python export_60m_yfinance.py

NB: yfinance limita l'intervallo 60m a max ~730 giorni indietro.
    Finestra consigliata ~60 gg: copre le ultime 2-3 onde daily
    (~290-420 barre orarie), abbastanza per ancorare il conteggio
    e cronometrare i trigger intraday, senza rumore inutile.
"""

import os
from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from tickers import TICKERS   # <-- lista unica condivisa (tickers.py, stessa cartella)

# ----------------- CONFIG -----------------
DAYS_BACK = 60               # consigliato 60 (max ~730 per il 60m)
OUTFILE = "60m.csv"          # un unico file, sovrascritto
# ------------------------------------------

start = date.today() - timedelta(days=DAYS_BACK)
end = date.today() + timedelta(days=1)          # +1 per includere oggi

frames = []
for t in TICKERS:
    try:
        df = yf.Ticker(t).history(
            start=start.isoformat(),
            end=end.isoformat(),
            interval="60m",
            auto_adjust=True,        # OHLC aggiustati per split (e dividendi)
        )
        if df.empty:
            print(f"[!]  {t}: nessun dato")
            continue

        out = df[["Open", "High", "Low", "Close", "Volume"]].round(4)
        out.index.name = "Datetime"             # TIENE data+ora (e' orario)
        out = out.reset_index()
        out.insert(0, "Ticker", t)              # colonna Ticker in testa
        frames.append(out)
        print(f"[ok] {t}: {len(out)} barre 60m")
    except Exception as e:
        print(f"[err] {t}: {e}")

if not frames:
    print("\n[!] Nessun dato scaricato. File non scritto.")
else:
    alldata = pd.concat(frames, ignore_index=True)
    alldata.to_csv(OUTFILE, index=False)        # SOVRASCRIVE
    print(f"\nFatto. {len(frames)} ticker, {len(alldata)} righe -> {OUTFILE}  — caricami questo file qui.")