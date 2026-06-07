#!/usr/bin/env python3
"""
Export OHLC DAILY split-adjusted per la watchlist.
Output: UN SOLO CSV consolidato (formato long) -> daily.csv
        colonne: Ticker, Date, Open, High, Low, Close, Volume
        Il file viene SOVRASCRITTO a ogni esecuzione.
Requisiti:  pip install yfinance pandas
Uso:        python export_daily_yfinance.py
"""

import os
from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from tickers import TICKERS   # <-- lista unica condivisa (tickers.py, stessa cartella)

# ----------------- CONFIG -----------------
MONTHS_BACK = 18
OUTFILE = "daily.csv"        # un unico file, sovrascritto
# ------------------------------------------

start = date.today() - timedelta(days=int(MONTHS_BACK * 30.5))
end = date.today() + timedelta(days=1)          # +1 per includere oggi

frames = []
for t in TICKERS:
    try:
        df = yf.Ticker(t).history(
            start=start.isoformat(),
            end=end.isoformat(),
            interval="1d",
            auto_adjust=True,        # OHLC tutti aggiustati per split (e dividendi)
        )
        if df.empty:
            print(f"[!]  {t}: nessun dato")
            continue

        out = df[["Open", "High", "Low", "Close", "Volume"]].round(4)
        out.index = out.index.date              # toglie l'orario -> YYYY-MM-DD
        out.index.name = "Date"
        out = out.reset_index()
        out.insert(0, "Ticker", t)              # colonna Ticker in testa
        frames.append(out)
        print(f"[ok] {t}: {len(out)} barre")
    except Exception as e:
        print(f"[err] {t}: {e}")

if not frames:
    print("\n[!] Nessun dato scaricato. File non scritto.")
else:
    alldata = pd.concat(frames, ignore_index=True)
    alldata.to_csv(OUTFILE, index=False)        # SOVRASCRIVE
    print(f"\nFatto. {len(frames)} ticker, {len(alldata)} righe -> {OUTFILE}  — caricami questo file qui.")