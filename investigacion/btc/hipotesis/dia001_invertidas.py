"""BTC · día 1 (control): las señales B002 y B005 dieron negativas. ¿Funciona hacer lo contrario después de costos?
B006: desvanecer la ruptura del rango asiático en Londres (B002 invertida).
B007: desvanecer el impulso de la apertura de Wall Street (B005 invertida).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np, pandas as pd
from motor import usar, cargar, evaluar, registrar, resumen
usar('btc'); COD = 'btc/hipotesis/dia001_invertidas.py'
h1 = cargar('1h'); dia = h1.index.normalize(); m = h1.index.hour < 7
asia = h1[m].groupby(dia[m]).agg(ah=('h', 'max'), al=('l', 'min')); x = h1.join(asia, on=dia)
v = (x.index.hour >= 7) & (x.index.hour <= 11)
s = pd.Series(0, index=h1.index); s[v & (x.c > x.ah)] = -1; s[v & (x.c < x.al)] = 1
s = s.where(s.groupby(dia).cumsum().abs().le(1) & (s != 0), 0)
for hz in (4,):
    res = evaluar(s, h1, hz); print('B006', resumen(res))
registrar('B006', 'Desvanecer la ruptura asiática en Londres', 'Ir en contra del primer cierre de 1 h fuera del rango 00-07 UTC (07-11 UTC), 4 h.', res, COD)
s5 = pd.Series(0, index=h1.index)
for ts in h1.index[h1.index.hour == 14]:
    t0 = ts - pd.Timedelta(hours=1)
    if t0 in h1.index:
        mov = np.log(h1.c[ts] / h1.o[t0])
        if abs(mov) > 0.004: s5[ts] = -1 if mov > 0 else 1
res = evaluar(s5, h1, 6); print('B007', resumen(res))
registrar('B007', 'Desvanecer el impulso de la apertura de Wall Street', 'Si 13-15 UTC se mueve > 0,4 %, ir en contra de 15 a 21 UTC.', res, COD)
