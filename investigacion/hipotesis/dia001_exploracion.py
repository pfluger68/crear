"""Día 1: exploración base y primeras 4 hipótesis.

H001 (descriptivo): comportamiento por hora UTC y por día de la semana.
H002: martillo diario tras caída -> compra al día siguiente.
H003: ruptura del rango asiático (00-07 UTC) durante Londres -> continuación 4 h.
H004: día de rango extremo (> 1,8 x ATR) -> reversión al día siguiente.
H005: fin de semana de PAXG (spot cerrado) -> reversión del movimiento del finde al reabrir el oro físico.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pandas as pd
from motor import cargar, evaluar, registrar, resumen, descriptivo

h1 = cargar('1h'); d1 = cargar('1d')
r1 = np.log(h1.c / h1.c.shift(1))

# ---------- H001 descriptivo ----------
tab = pd.DataFrame({'r': r1, 'abs': r1.abs(), 'h': h1.index.hour, 'dow': h1.index.dayofweek})
por_hora = tab.groupby('h').agg(media_pb=('r', lambda x: round(x.mean() * 1e4, 2)), vol_pb=('abs', lambda x: round(x.mean() * 1e4, 1)))
por_dia = tab.groupby('dow').agg(media_pb=('r', lambda x: round(x.mean() * 1e4, 2)), vol_pb=('abs', lambda x: round(x.mean() * 1e4, 1)))
print('H001 por hora UTC\n', por_hora.T.to_string())
print('H001 por día (0=lunes)\n', por_dia.T.to_string())
registrar('H001', 'Ritmo horario y semanal', 'Cómo cambian el movimiento medio y la volatilidad según la hora UTC y el día.',
          descriptivo('H001', {'por_hora': por_hora.to_dict(), 'por_dia': por_dia.to_dict()}), codigo='hipotesis/dia001_exploracion.py')

# ---------- H002 martillo diario ----------
rango = d1.h - d1.l
cuerpo = (d1.c - d1.o).abs()
mecha_inf = d1[['o', 'c']].min(axis=1) - d1.l
caida5 = d1.c / d1.c.shift(5) - 1
martillo = (mecha_inf >= 2 * cuerpo) & ((d1.c - d1.l) >= 0.67 * rango) & (caida5 < 0) & (rango > 0)
s2 = martillo.astype(int)
res2 = evaluar(s2, d1, horizonte=1)
print('H002', resumen(res2))
registrar('H002', 'Martillo diario tras caída', 'Tras 5 días de caída, una vela diaria con mecha inferior larga anticipa subida al día siguiente.', res2, 'hipotesis/dia001_exploracion.py')

# ---------- H003 ruptura rango asiático ----------
dia = h1.index.normalize()
asia = h1[h1.index.hour < 7].groupby(dia[h1.index.hour < 7]).agg(ah=('h', 'max'), al=('l', 'min'))
x = h1.join(asia, on=dia)
ventana = (x.index.hour >= 7) & (x.index.hour <= 11)
s3 = pd.Series(0, index=h1.index)
s3[ventana & (x.c > x.ah)] = 1
s3[ventana & (x.c < x.al)] = -1
# solo la primera ruptura del día
s3 = s3.where(s3.groupby(dia).cumsum().abs().le(1) & (s3 != 0), 0)
res3 = evaluar(s3, h1, horizonte=4)
print('H003', resumen(res3))
registrar('H003', 'Ruptura del rango asiático en Londres', 'Si entre las 07 y 11 UTC el precio cierra fuera del rango 00-07 UTC, sigue en esa dirección 4 horas.', res3, 'hipotesis/dia001_exploracion.py',
          estado='rechazada', nota='Cambio de régimen: en 2021-mediados de 2024 la ruptura FALLABA (t=-4,7); desde entonces tiende a continuar (t=+1,6). Ninguna dirección es estable. Ver H006.')

# ---------- H004 reversión tras día extremo ----------
tr = pd.concat([d1.h - d1.l, (d1.h - d1.c.shift()).abs(), (d1.l - d1.c.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean().shift(1)
extremo = rango > 1.8 * atr
s4 = pd.Series(0, index=d1.index)
s4[extremo & (d1.c > d1.o)] = -1
s4[extremo & (d1.c < d1.o)] = 1
res4 = evaluar(s4, d1, horizonte=1)
print('H004', resumen(res4))
registrar('H004', 'Reversión tras día de rango extremo', 'Tras un día con rango mayor a 1,8 veces el ATR, el día siguiente va en contra.', res4, 'hipotesis/dia001_exploracion.py',
          estado='rechazada', nota='Mismo cambio de régimen que H003: revertía antes de 2024 y en validación continúa (t=-1,96).')

# ---------- H005 fin de semana PAXG ----------
# viernes 21 UTC (cierre spot) -> domingo 22 UTC (reapertura). Señal al cierre de la vela de domingo 21h: contra el movimiento del finde.
c = h1.c
s5 = pd.Series(0, index=h1.index)
for ts in h1.index[(h1.index.dayofweek == 6) & (h1.index.hour == 21)]:
    vie = ts - pd.Timedelta(hours=48)
    if vie in c.index:
        mov = np.log(c[ts] / c[vie])
        if abs(mov) > 0.004:  # finde con movimiento > 0,4 %
            s5[ts] = -1 if mov > 0 else 1
for hz in (12, 3):
    res5 = evaluar(s5, h1, horizonte=hz)
    print(f'H005 h={hz}', resumen(res5))
registrar('H005', 'Reversión del fin de semana de PAXG', 'Cuando el oro tokenizado se mueve > 0,4 % con el mercado físico cerrado, al reabrir el oro (dom 22 UTC) se revierte en las 3 h siguientes.', res5, 'hipotesis/dia001_exploracion.py',
          estado='en seguimiento', nota='Significativa en muestra (t=2,35), positiva pero no significativa en validación (n=44). A 12 h no funciona. Seguir en vivo cada domingo.')
