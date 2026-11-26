"""Motor de pruebas de hipótesis sobre el oro.

Reglas (para no engañarnos):
1. Cada idea se convierte en una señal: +1 compra, -1 venta, 0 nada, decidida con datos hasta el cierre de la vela.
2. Se mide el resultado en las velas siguientes (horizonte fijo), sin operaciones solapadas.
3. Se descuenta un costo por operación (diferencial + comisión).
4. Se mide por separado en dos tramos:
   - Muestra (desarrollo): desde 2021 hasta CORTE.
   - Validación (fuera de muestra): desde CORTE hasta hoy. No se usa para inventar ideas, solo para validarlas.
5. Una idea es "prometedora" solo si funciona en los dos tramos, en el mismo sentido, con significancia y después de costos.
   Luego pasa a "seguimiento en vivo"; se confirma solo si sigue funcionando con datos que todavía no existían.

Uso desde un archivo de hipótesis:
    from motor import cargar, evaluar, registrar
    df = cargar('1h')
    senal = ...  # pd.Series alineada a df
    res = evaluar(senal, df, horizonte=4)
    registrar('H007', 'nombre corto', 'idea en una frase', res, codigo='hipotesis/h007.py')
"""
import json, math, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(BASE, 'datos')
REGISTRO = os.path.join(BASE, 'hipotesis.json')
INICIO = '2021-01-01'   # 2020 tuvo poca liquidez en PAXG: se excluye
CORTE = '2024-07-01'    # a partir de aquí es validación fuera de muestra
COSTO_PB = 3.0          # costo por operación ida y vuelta, en puntos básicos (≈ 1 USD por onza con oro a 3.500)


def cargar(intervalo='1h', fuente='PAXGUSDT'):
    nombre = f'{fuente}_{intervalo}.csv' if fuente == 'PAXGUSDT' else f'XAU_HL_{intervalo}.csv'
    df = pd.read_csv(os.path.join(DATOS, nombre))
    df['fecha'] = pd.to_datetime(df['t'], unit='s', utc=True)
    df = df.set_index('fecha').drop(columns='t')
    if fuente == 'PAXGUSDT':
        df = df[df.index >= INICIO]
    return df


def _p_valor(t):
    """Valor p bilateral aproximado (normal) para un estadístico t."""
    return math.erfc(abs(t) / math.sqrt(2))


def _no_solapar(idx_pos, horizonte):
    elegidos, siguiente = [], -1
    for i in idx_pos:
        if i >= siguiente:
            elegidos.append(i)
            siguiente = i + horizonte
    return np.array(elegidos, dtype=int)


def _stats(r):
    n = len(r)
    if n < 2:
        return {'n': int(n)}
    media, sd = float(np.mean(r)), float(np.std(r, ddof=1))
    t = media / (sd / math.sqrt(n)) if sd > 0 else 0.0
    return {
        'n': int(n),
        'media_pb': round(media * 1e4, 2),
        'aciertos_pct': round(float(np.mean(r > 0)) * 100, 1),
        'total_pct': round(float(np.sum(r)) * 100, 2),
        't': round(t, 2),
        'p': round(_p_valor(t), 4),
        'factor_beneficio': round(float(r[r > 0].sum() / -r[r < 0].sum()), 2) if (r < 0).any() else None,
    }


def evaluar(senal, df, horizonte, costo_pb=COSTO_PB, entrada='siguiente_apertura'):
    """Evalúa una señal direccional.

    senal: pd.Series (+1/-1/0) con el mismo índice que df, conocida al cierre de cada vela.
    horizonte: número de velas que se mantiene la operación.
    entrada: 'siguiente_apertura' (realista) o 'cierre'.
    Devuelve estadísticas en muestra, validación y total, más una referencia de azar.
    """
    senal = senal.reindex(df.index).fillna(0).astype(int).values
    o, c = df['o'].values, df['c'].values
    n = len(df)
    pos = np.flatnonzero(senal != 0)
    pos = pos[pos + horizonte + 1 < n]
    pos = _no_solapar(pos, horizonte)
    if entrada == 'siguiente_apertura':
        precio_in, precio_out = o[pos + 1], c[pos + horizonte]
    else:
        precio_in, precio_out = c[pos], c[pos + horizonte]
    r = senal[pos] * np.log(precio_out / precio_in) - costo_pb / 1e4
    fechas = df.index[pos]
    corte = pd.Timestamp(CORTE, tz='UTC')
    m_in, m_out = fechas < corte, fechas >= corte
    # Referencia: misma cantidad de operaciones al azar en la misma dirección
    rng = np.random.default_rng(7)
    todas = np.arange(0, n - horizonte - 2)
    azar = []
    for _ in range(200):
        s = rng.choice(todas, size=max(1, len(pos)), replace=False)
        lado = rng.choice(senal[pos], size=len(s)) if len(pos) else np.ones(len(s))
        azar.append(np.mean(lado * np.log(c[s + horizonte] / o[s + 1]) - costo_pb / 1e4))
    return {
        'horizonte': horizonte,
        'costo_pb': costo_pb,
        'muestra': _stats(r[m_in]),
        'validacion': _stats(r[m_out]),
        'total': _stats(r),
        'azar_media_pb_p95': round(float(np.percentile(azar, 95)) * 1e4, 2),
    }


def veredicto(res, n_min=30):
    a, b = res['muestra'], res['validacion']
    if a.get('n', 0) < n_min or b.get('n', 0) < n_min:
        return 'insuficiente'
    mismo_signo = a['media_pb'] > 0 and b['media_pb'] > 0
    if mismo_signo and a['p'] < 0.05 and b['p'] < 0.01:
        return 'prometedora'
    if mismo_signo and a['p'] < 0.1 and b['p'] < 0.1:
        return 'débil'
    return 'rechazada'


def descriptivo(nombre, tabla):
    """Para hallazgos descriptivos (no operables directamente): guarda una tabla breve."""
    return {'tipo': 'descriptivo', 'tabla': tabla}


def registrar(id_, nombre, idea, resultado, codigo=None, estado=None, nota=''):
    reg = json.load(open(REGISTRO)) if os.path.exists(REGISTRO) else {'hipotesis': []}
    if estado is None:
        estado = veredicto(resultado) if 'muestra' in resultado else 'descriptivo'
    entrada = {'id': id_, 'nombre': nombre, 'idea': idea, 'estado': estado, 'codigo': codigo,
               'fecha': datetime.now(timezone.utc).strftime('%Y-%m-%d'), 'resultado': resultado, 'nota': nota}
    reg['hipotesis'] = [h for h in reg['hipotesis'] if h['id'] != id_] + [entrada]
    reg['probadas'] = sum(1 for h in reg['hipotesis'] if h['estado'] not in ('pendiente',))
    json.dump(reg, open(REGISTRO, 'w'), ensure_ascii=False, indent=1)
    return estado


def resumen(res):
    a, b = res['muestra'], res['validacion']
    f = lambda s: f"n={s.get('n')} media={s.get('media_pb')}pb aciertos={s.get('aciertos_pct')}% t={s.get('t')} p={s.get('p')}"
    return f"MUESTRA {f(a)} | VALIDACIÓN {f(b)} | azar p95={res['azar_media_pb_p95']}pb"
