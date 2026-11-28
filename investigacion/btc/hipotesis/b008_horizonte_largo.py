"""B008 · Horizonte largo (1-5 días) para cubrir los 10 pb de costo de BTC.

Tres variantes diseñadas ANTES de mirar la validación, con parámetros fijos (sin optimizar):
  a) Tendencia diaria: EMA 20 > EMA 50 → compra, < → venta. Se mantiene 5 días.
  b) Ruptura del rango de 7 días: cierre diario por encima del máximo de los 7 días previos → compra
     (por debajo del mínimo → venta). Se mantiene 5 días.
  c) Reversión tras una caída grande: vela diaria con cuerpo bajista > 1,5 ATR(14) → compra 3 días.
     (la idea original decía 3 ATR, pero en velas diarias casi no hay casos; 1,5 se fija antes de evaluar).
Para cada una se mira media bruta y neta, y la señal invertida.
Se prueban 3 ideas a la vez: se exige más que el umbral normal (corrección de Bonferroni, p muestra < 0,017).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import pandas as pd
from motor import usar, cargar, evaluar, registrar, resumen, veredicto

usar('btc')
COD = 'btc/hipotesis/b008_horizonte_largo.py'
d = cargar('1d')
c = d['c']

# a) tendencia EMA 20/50
e20, e50 = c.ewm(span=20, adjust=False).mean(), c.ewm(span=50, adjust=False).mean()
sa = pd.Series((e20 > e50).astype(int) * 2 - 1, index=d.index)
sa.iloc[:60] = 0

# b) ruptura del rango de 7 días
hi7, lo7 = d['h'].rolling(7).max().shift(1), d['l'].rolling(7).min().shift(1)
sb = pd.Series(0, index=d.index)
sb[c > hi7] = 1
sb[c < lo7] = -1

# c) reversión tras día bajista grande (cuerpo < -1,5 ATR 14)
tr = pd.concat([d['h'] - d['l'], (d['h'] - c.shift()).abs(), (d['l'] - c.shift()).abs()], axis=1).max(axis=1)
atr = tr.rolling(14).mean().shift(1)
sc = pd.Series(0, index=d.index)
sc[(c - d['o']) < -1.5 * atr] = 1

resultados = {}
for nombre, s, hz in (('a_tendencia_ema', sa, 5), ('b_ruptura_7d', sb, 5), ('c_reversion_caida', sc, 3)):
    r = evaluar(s, d, hz)
    ri = evaluar(-s, d, hz)
    print(nombre, veredicto(r), resumen(r))
    print('  invertida', veredicto(ri), resumen(ri))
    resultados[nombre] = {'directa': r, 'invertida': ri}

if __name__ == '__main__' and '--registrar' in sys.argv:
    est = [veredicto(v['directa']) for v in resultados.values()]
    estado = 'prometedora' if 'prometedora' in est else ('débil' if 'débil' in est else 'rechazada')
    registrar('B008', 'Horizonte largo para cubrir costos',
              'Señales diarias de 3-5 días: tendencia EMA 20/50, ruptura del rango de 7 días y reversión tras una caída > 1,5 ATR.',
              resultados, COD, estado=estado, nota=sys.argv[-1] if len(sys.argv) > 2 else '')
