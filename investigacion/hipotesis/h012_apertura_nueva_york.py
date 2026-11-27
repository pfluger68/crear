"""H012: firma de la apertura de Nueva York.

Pregunta: ¿el movimiento de 13:30–14:30 UTC predice la dirección del resto de la sesión de EE. UU.?

Diseño (fijado antes de mirar la validación):
- Datos: PAXG/USDT de 15 m, solo de lunes a viernes.
- Movimiento de apertura: log(cierre 14:30 / apertura 13:30), es decir, velas de 13:30, 13:45, 14:00 y 14:15.
- Variante principal (A): continuación. Señal = signo del movimiento de apertura, conocida al cierre de
  la vela de 14:15. Entrada en la apertura de 14:30, salida al cierre de 20:00 UTC (22 velas de 15 m).
- Variante B (proxy de día de datos macro): igual que A pero solo si |movimiento| supera la mediana de
  los 60 días hábiles previos (solo datos pasados).
- Variante C (horario de NY con cambio de hora): la ventana se mueve a 9:30–10:30 hora de Nueva York
  (13:30 UTC en verano, 14:30 UTC en invierno) y la salida a las 16:00 hora de NY.
- Señal invertida de A y B: se prueba antes de concluir que "lo contrario funciona".
Costo 3 pb. Muestra 2021 → junio 2024; validación julio 2024 → hoy.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pandas as pd
import motor
from motor import cargar, evaluar, registrar, resumen

m15 = cargar('15m')
idx = m15.index
dia = idx.normalize()
laborable = idx.dayofweek < 5


def senal_ventana(df, ini, fin_ultima, umbral_rel=False, local=None):
    """ini: hora (h, m) de la primera vela; fin_ultima: hora de la última vela de la ventana."""
    t = df.index if local is None else df.index.tz_convert(local)
    hm = t.hour * 60 + t.minute
    d = pd.Index(t.normalize())
    a = ini[0] * 60 + ini[1]
    b = fin_ultima[0] * 60 + fin_ultima[1]
    ap = pd.Series(df.o.values, index=df.index)[(hm == a) & laborable]
    ci = pd.Series(df.c.values, index=df.index)[(hm == b) & laborable]
    ap.index = d[(hm == a) & laborable]
    ci_d = d[(hm == b) & laborable]
    mov = pd.Series(np.log(ci.values / ap.reindex(ci_d).values), index=ci.index)
    mov = mov.dropna()
    s = np.sign(mov)
    if umbral_rel:
        med = mov.abs().rolling(60).median().shift(1)
        s = s.where(mov.abs() > med, 0)
    out = pd.Series(0, index=df.index)
    out.loc[s.index] = s.values
    return out.astype(int), mov


# A: continuación, ventana fija UTC
sA, mov = senal_ventana(m15, (13, 30), (14, 15))
rA = evaluar(sA, m15, 22)
rA_inv = evaluar(-sA, m15, 22)
# B: solo movimientos grandes (proxy de datos macro)
sB, _ = senal_ventana(m15, (13, 30), (14, 15), umbral_rel=True)
rB = evaluar(sB, m15, 22)
rB_inv = evaluar(-sB, m15, 22)
# C: ventana en hora de Nueva York (9:30-10:30 local, salida 16:00 local = 22 velas)
sC, _ = senal_ventana(m15, (9, 30), (10, 15), local='America/New_York')
rC = evaluar(sC, m15, 22)

for nom, r in (('A cont', rA), ('A inv', rA_inv), ('B grande', rB), ('B inv', rB_inv), ('C NY local', rC)):
    print(nom, resumen(r))

# Descriptivo: correlación entre el movimiento de apertura y el resto (14:30 -> 20:00)
c = m15.c
resto = []
for ts, mv in mov.items():
    i = m15.index.get_loc(ts)
    if i + 22 < len(m15):
        resto.append((ts, mv, np.log(c.iloc[i + 22] / m15.o.iloc[i + 1])))
R = pd.DataFrame(resto, columns=['t', 'apertura', 'resto']).set_index('t')
corte = pd.Timestamp(motor.CORTE, tz='UTC')
corr = {k: round(float(g.apertura.corr(g.resto)), 3)
        for k, g in (('muestra', R[R.index < corte]), ('validacion', R[R.index >= corte]))}
print('correlación apertura→resto', corr)

nota = (f"Continuación (A) y su inversa, filtro de movimiento grande (B) y ventana en hora de NY (C). "
        f"Correlación apertura→resto: muestra {corr['muestra']}, validación {corr['validacion']}. "
        f"A: {resumen(rA)}. A invertida: {resumen(rA_inv)}. B: {resumen(rB)}. B invertida: {resumen(rB_inv)}. "
        f"C: {resumen(rC)}. 5 variantes probadas: exigir más por comparaciones múltiples.")
resultado = dict(rA)
resultado['variantes'] = {'A_invertida': rA_inv, 'B_movimiento_grande': rB, 'B_invertida': rB_inv,
                          'C_hora_NY': rC, 'correlacion_apertura_resto': corr}
est = registrar('H012', 'Firma de la apertura de Nueva York',
                '¿El movimiento de 13:30–14:30 UTC predice la dirección del resto de la sesión de EE. UU. (14:30–20:00)? '
                'Continuación por signo; variantes con filtro de movimiento grande, invertida y ventana en hora de NY.',
                resultado, codigo='hipotesis/h012_apertura_nueva_york.py', nota=nota)
print('estado H012:', est)
