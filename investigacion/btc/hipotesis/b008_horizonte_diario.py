"""B008 · Horizonte largo para cubrir costos (velas diarias, mantener 5 días).
Diseño fijado antes de mirar la validación:
  A) Tendencia: EMA20 > EMA50 -> largo; < -> corto. Evaluado cada 5 días sin solapar.
  B) Reversión tras caída fuerte: retorno diario < -3 ATR14 (en % del cierre) -> largo 5 días.
Se reportan bruta y neta (10 pb) y la señal invertida.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np, pandas as pd
import motor
from motor import usar, cargar, evaluar, registrar, resumen
usar('btc'); COD = 'btc/hipotesis/b008_horizonte_diario.py'
d = cargar('1d'); d = d[d.index >= '2019-01-01']
HZ = 5
e20, e50 = d.c.ewm(span=20).mean(), d.c.ewm(span=50).mean()
sA = pd.Series(np.where(e20 > e50, 1, -1), index=d.index); sA.iloc[:60] = 0
resA = evaluar(sA, d, HZ); print('A tendencia     ', resumen(resA))
resAi = evaluar(-sA, d, HZ); print('A invertida     ', resumen(resAi))
# solo largos de la tendencia (BTC tiene deriva alcista: separar deriva de señal)
resAl = evaluar(sA.clip(lower=0), d, HZ); print('A solo largos   ', resumen(resAl))
resBH = evaluar(pd.Series(1, index=d.index), d, HZ); print('Comprar siempre ', resumen(resBH))
tr = pd.concat([d.h - d.l, (d.h - d.c.shift()).abs(), (d.l - d.c.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean().shift(1)
ret = d.c - d.c.shift()
sB = pd.Series(np.where(ret < -3 * atr, 1, 0), index=d.index)
resB = evaluar(sB, d, HZ); print('B rebote -3ATR  ', resumen(resB))
resBi = evaluar(-sB, d, HZ); print('B invertida     ', resumen(resBi))
nota = (f"A invertida: muestra {resAi['muestra'].get('media_pb')} pb, validación {resAi['validacion'].get('media_pb')} pb. "
        f"Solo largos: muestra {resAl['muestra'].get('media_pb')} / val {resAl['validacion'].get('media_pb')} pb; "
        f"comprar siempre 5 d: muestra {resBH['muestra'].get('media_pb')} / val {resBH['validacion'].get('media_pb')} pb.")
eA = registrar('B008', 'Horizonte largo: tendencia EMA 20/50 diaria (5 días)',
               'Largo si EMA20>EMA50 diaria, corto si no; mantener 5 días, sin solapar.', resA, COD, nota=nota)
notaB = f"Invertida: muestra {resBi['muestra'].get('media_pb')} pb, validación {resBi['validacion'].get('media_pb')} pb."
eB = registrar('B015', 'Rebote tras caída diaria de más de 3 ATR (5 días)',
               'Si el cierre diario cae más de 3 ATR14 respecto al anterior, largo 5 días.', resB, COD, nota=notaB)
print('Veredictos:', eA, eB)
