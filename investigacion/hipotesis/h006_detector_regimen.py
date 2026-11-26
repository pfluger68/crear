"""H006: detector de régimen para la ruptura del rango asiático (H003).

Diseño (fijado antes de mirar la validación):
- Medida de régimen: ratio de varianzas VR(4) de los retornos de 1 h en los 30 días previos
  (varianza de retornos de 4 h / (4 x varianza de 1 h)), calculado solo con datos pasados.
  VR < 1 -> el mercado revierte; VR > 1 -> el mercado continúa.
- Variante principal (H006): operar la ruptura de H003 a favor si VR > 1 y en contra si VR < 1.
- Variante adaptativa (control): operar en la dirección que dio el signo de las últimas 20
  rupturas de H003 ya cerradas (mira solo resultados pasados).
Se compara también con H003 fija (a favor) para ver si el detector aporta algo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pandas as pd
import motor
from motor import cargar, evaluar, registrar, resumen

h1 = cargar('1h')
r1 = np.log(h1.c / h1.c.shift(1))

# --- señal base H003 (idéntica a dia001) ---
dia = h1.index.normalize()
m_asia = h1.index.hour < 7
asia = h1[m_asia].groupby(dia[m_asia]).agg(ah=('h', 'max'), al=('l', 'min'))
x = h1.join(asia, on=dia)
ventana = (x.index.hour >= 7) & (x.index.hour <= 11)
s3 = pd.Series(0, index=h1.index)
s3[ventana & (x.c > x.ah)] = 1
s3[ventana & (x.c < x.al)] = -1
s3 = s3.where(s3.groupby(dia).cumsum().abs().le(1) & (s3 != 0), 0)

# --- régimen: VR(4) en 720 h previas (conocido al cierre de la vela anterior) ---
W = 720
r4 = r1.rolling(4).sum()
vr = (r4.rolling(W).var() / (4 * r1.rolling(W).var())).shift(1)
reg = np.where(vr > 1, 1, -1)
s6 = (s3 * pd.Series(reg, index=h1.index)).where(vr.notna(), 0).astype(int)

# --- variante adaptativa: signo de la media de las últimas 20 rupturas cerradas (4 h) ---
pos = np.flatnonzero(s3.values != 0)
o, c = h1.o.values, h1.c.values
res_b = pd.Series(np.nan, index=h1.index)
for p in pos:
    if p + 4 < len(c):
        res_b.iloc[p + 4] = s3.values[p] * np.log(c[p + 4] / o[p + 1])  # conocido al cierre de p+4
media20 = res_b.dropna().rolling(20).mean().reindex(h1.index).ffill().shift(1)
sA = (s3 * np.sign(media20)).fillna(0).astype(int)

base = evaluar(s3, h1, horizonte=4)
r6 = evaluar(s6, h1, horizonte=4)
rA = evaluar(sA, h1, horizonte=4)
print('H003 fija  ', resumen(base))
print('H006 VR    ', resumen(r6))
print('Adaptativa ', resumen(rA))

# Diagnóstico: ¿VR distingue? Resultado bruto de H003 según régimen, por tramo
corte = pd.Timestamp(motor.CORTE, tz='UTC')
d = pd.DataFrame({'s': s3, 'vr': vr})
d = d[(d.s != 0) & d.vr.notna()]
idx = [h1.index.get_loc(t) for t in d.index]
d['ret'] = [d.s.iloc[i] * np.log(c[j + 4] / o[j + 1]) * 1e4 if j + 4 < len(c) else np.nan for i, j in enumerate(idx)]
d['tramo'] = np.where(d.index < corte, 'muestra', 'validacion')
d['regimen'] = np.where(d.vr > 1, 'VR>1', 'VR<1')
diag = d.groupby(['tramo', 'regimen']).ret.agg(['count', 'mean']).round(1)
print(diag)
frac = d.groupby('tramo').vr.apply(lambda v: round(float((v > 1).mean()), 2))
print('fracción de rupturas con VR>1:', frac.to_dict())

if __name__ == '__main__' and '--registrar' in sys.argv:
    nota = (f"VR(4) 30 d. Diagnóstico H003 bruto pb por régimen: {diag.reset_index().to_dict('records')}. "
            f"Adaptativa (últimas 20 rupturas): {resumen(rA)}")
    registrar('H006', 'Detector de régimen', 'Operar la ruptura del rango asiático a favor si el ratio de varianzas VR(4) de 30 días es > 1 (continuación) y en contra si es < 1 (reversión).',
              r6, 'hipotesis/h006_detector_regimen.py', nota=nota)
