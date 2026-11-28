"""B009 · ¿La subida media de las 20-22 UTC es estable o ruido?
Diseño fijo: largo al cierre de la vela de 19 UTC (entrada en la apertura de 20 UTC), mantener 3 h (20, 21, 22).
Se reporta por año, bruto y neto, y la invertida. Con 10 pb de costo se espera que no cubra.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np, pandas as pd
from motor import usar, cargar, evaluar, registrar, resumen
usar('btc'); COD = 'btc/hipotesis/b009_hora_20_22.py'
h = cargar('1h')
s = pd.Series(np.where(h.index.hour == 19, 1, 0), index=h.index)
res = evaluar(s, h, 3); print('B009      ', resumen(res))
resi = evaluar(-s, h, 3); print('invertida ', resumen(resi))
r = np.log(h.c / h.o); v = r[h.index.hour.isin([20, 21, 22])]
anual = (v.groupby(v.index.year).sum() / v.groupby(v.index.year).count() * 3 * 1e4).round(1)
print('bruto pb por año (20-22 UTC, 3 h):', anual.to_dict())
nota = f"Bruto por año (pb, bloque 3 h): {anual.to_dict()}. Invertida: muestra {resi['muestra'].get('media_pb')} / val {resi['validacion'].get('media_pb')} pb."
print(registrar('B009', 'Hora 20-22 UTC', 'Largo de 20 a 23 UTC cada día (3 h).', res, COD, nota=nota))
