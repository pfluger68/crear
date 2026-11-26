"""BTC · día 1: exploración base. Mismas ideas que el oro para comparar, más dos propias de BTC.

B001 (descriptivo): ritmo por hora UTC y día de la semana.
B002: ruptura del rango asiático (00-07 UTC) en Londres -> continuación 4 h (en oro cambió de régimen en 2024).
B003: día de rango extremo (> 1,8 x ATR) -> reversión al día siguiente.
B004: "gap de CME": si BTC se mueve > 2 % el fin de semana (vie 21 UTC -> dom 22 UTC), ¿revierte en las 24 h siguientes?
B005: apertura de Wall Street: el movimiento de 13-15 UTC predice la dirección de 15-21 UTC.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np, pandas as pd
from motor import usar, cargar, evaluar, registrar, resumen, descriptivo
usar('btc')
COD = 'btc/hipotesis/dia001_exploracion.py'
h1 = cargar('1h'); d1 = cargar('1d')
r1 = np.log(h1.c / h1.c.shift(1))

# B001
tab = pd.DataFrame({'r': r1, 'abs': r1.abs(), 'h': h1.index.hour, 'dow': h1.index.dayofweek})
ph = tab.groupby('h').agg(media_pb=('r', lambda x: round(x.mean() * 1e4, 2)), vol_pb=('abs', lambda x: round(x.mean() * 1e4, 1)))
pdw = tab.groupby('dow').agg(media_pb=('r', lambda x: round(x.mean() * 1e4, 2)), vol_pb=('abs', lambda x: round(x.mean() * 1e4, 1)))
print('B001 hora\n', ph.T.to_string()); print('B001 día\n', pdw.T.to_string())
registrar('B001', 'Ritmo horario y semanal de BTC', 'Movimiento medio y volatilidad por hora UTC y día.', descriptivo('B001', {'por_hora': ph.to_dict(), 'por_dia': pdw.to_dict()}), COD)

# B002
dia = h1.index.normalize()
m = h1.index.hour < 7
asia = h1[m].groupby(dia[m]).agg(ah=('h', 'max'), al=('l', 'min'))
x = h1.join(asia, on=dia)
v = (x.index.hour >= 7) & (x.index.hour <= 11)
s = pd.Series(0, index=h1.index); s[v & (x.c > x.ah)] = 1; s[v & (x.c < x.al)] = -1
s = s.where(s.groupby(dia).cumsum().abs().le(1) & (s != 0), 0)
res = evaluar(s, h1, 4); print('B002', resumen(res))
# por año, para ver régimen
r_ = evaluar(s, h1, 4)
fwd = np.log(h1.c.shift(-4) / h1.o.shift(-1)) * s
por_anio = (fwd[s != 0].groupby(fwd[s != 0].index.year).mean() * 1e4).round(1).to_dict()
print('B002 por año (pb, sin costos):', por_anio)
registrar('B002', 'Ruptura del rango asiático en Londres', 'Cierre de 1 h fuera del rango 00-07 UTC entre 07 y 11 UTC -> sigue 4 h.', res, COD, nota=f'Media por año sin costos (pb): {por_anio}')

# B003
rango = d1.h - d1.l
tr = pd.concat([rango, (d1.h - d1.c.shift()).abs(), (d1.l - d1.c.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean().shift(1)
ext = rango > 1.8 * atr
s3 = pd.Series(0, index=d1.index); s3[ext & (d1.c > d1.o)] = -1; s3[ext & (d1.c < d1.o)] = 1
res = evaluar(s3, d1, 1); print('B003', resumen(res))
registrar('B003', 'Reversión tras día de rango extremo', 'Tras un día con rango > 1,8 x ATR, el día siguiente va en contra.', res, COD)

# B004
c = h1.c; s4 = pd.Series(0, index=h1.index)
for ts in h1.index[(h1.index.dayofweek == 6) & (h1.index.hour == 22)]:
    vie = ts - pd.Timedelta(hours=49)
    if vie in c.index:
        mov = np.log(c[ts] / c[vie])
        if abs(mov) > 0.02:
            s4[ts] = -1 if mov > 0 else 1
for hz in (24, 6):
    res = evaluar(s4, h1, hz); print(f'B004 h={hz}', resumen(res))
registrar('B004', 'Reversión del fin de semana ("gap de CME")', 'Si BTC se mueve > 2 % entre el viernes 21 UTC y el domingo 22 UTC, revierte en las 6 h siguientes.', res, COD)

# B005
s5 = pd.Series(0, index=h1.index)
for ts in h1.index[h1.index.hour == 14]:
    t0 = ts - pd.Timedelta(hours=1)
    if t0 in h1.index:
        mov = np.log(h1.c[ts] / h1.o[t0])
        if abs(mov) > 0.004:
            s5[ts] = 1 if mov > 0 else -1
res = evaluar(s5, h1, 6); print('B005', resumen(res))
registrar('B005', 'Impulso de la apertura de Wall Street', 'Si 13-15 UTC se mueve > 0,4 %, 15-21 UTC sigue en esa dirección.', res, COD)
