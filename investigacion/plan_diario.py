"""Genera el plan diario del oro (XAU de Hyperliquid, el precio que muestra Atalaya).

Salidas:
- atalaya/plan-oro.json: lo lee Atalaya para dibujar zonas y operaciones sobre XAU/USD.
- investigacion/diario/AAAA-MM-DD.md: el plan en texto.

El plan es mecánico (niveles que coinciden). La tarea diaria puede ajustarlo con lo aprendido
en CONOCIMIENTO.md antes de publicarlo, y debe anotar los ajustes en "notas".
Uso: python3 investigacion/plan_diario.py
"""
import json, os
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from motor import cargar

BASE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(BASE)


def atr(df, n=14):
    tr = pd.concat([df.h - df.l, (df.h - df.c.shift()).abs(), (df.l - df.c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def giros(df, k):
    altos, bajos = [], []
    h, l = df.h.values, df.l.values
    for i in range(k, len(df) - k):
        if h[i] == h[i - k:i + k + 1].max():
            altos.append(h[i])
        if l[i] == l[i - k:i + k + 1].min():
            bajos.append(l[i])
    return altos, bajos


def main():
    d1, h4, h1, m15 = (cargar(iv, 'HL') for iv in ('1d', '4h', '1h', '15m'))
    precio = float(m15.c.iloc[-1])
    ahora = m15.index[-1]
    hoy = ahora.normalize()
    ayer = d1[d1.index < hoy].iloc[-1]
    P = (ayer.h + ayer.l + ayer.c) / 3
    atr_d = float(atr(d1).iloc[-1]); atr_h = float(atr(h1).iloc[-1])
    ema = lambda s, n: float(s.ewm(span=n, adjust=False).mean().iloc[-1])
    e20d, e50d = ema(d1.c, 20), ema(d1.c, 50)
    e50_4h = ema(h4.c, 50)

    niveles = [
        (ayer.h, 'máximo de ayer'), (ayer.l, 'mínimo de ayer'), (P, 'pivote'),
        (2 * P - ayer.l, 'R1'), (2 * P - ayer.h, 'S1'), (P + ayer.h - ayer.l, 'R2'), (P - (ayer.h - ayer.l), 'S2'),
        (e50_4h, 'EMA 50 de 4 h'),
    ]
    ga, gb = giros(h4[h4.index > ahora - pd.Timedelta(days=12)], 3)
    niveles += [(x, 'giro de 4 h') for x in ga + gb]
    ga, gb = giros(h1[h1.index > ahora - pd.Timedelta(days=4)], 4)
    niveles += [(x, 'giro de 1 h') for x in ga + gb]
    # nodos de volumen (1 h, últimos 5 días)
    rec = h1[h1.index > ahora - pd.Timedelta(days=5)]
    paso = max(1.0, round(atr_h / 5))
    nodos = ((rec.h + rec.l + rec.c) / 3 / paso).round() * paso
    vol = rec.v.groupby(nodos).sum().sort_values(ascending=False)
    niveles += [(float(x), 'nodo de volumen') for x in vol.index[:5]]

    # agrupar niveles cercanos
    ancho = 0.35 * atr_h
    niveles.sort()
    grupos = []
    for p, motivo in niveles:
        if grupos and p - grupos[-1]['hasta'] <= ancho:
            g = grupos[-1]; g['hasta'] = max(g['hasta'], p); g['motivos'].append(motivo)
        else:
            grupos.append({'desde': p, 'hasta': p, 'motivos': [motivo]})
    for g in grupos:
        g['peso'] = len(set(g['motivos'])) + 0.5 * (len(g['motivos']) - len(set(g['motivos'])))
        if g['hasta'] - g['desde'] < 0.3 * atr_h:  # dar un mínimo de grosor a la zona
            m = (g['desde'] + g['hasta']) / 2; g['desde'], g['hasta'] = m - 0.15 * atr_h, m + 0.15 * atr_h
    fuertes = [g for g in grupos if g['peso'] >= 2]
    arriba = sorted([g for g in fuertes if g['desde'] > precio + 0.2 * atr_h], key=lambda g: g['desde'])[:3]
    abajo = sorted([g for g in fuertes if g['hasta'] < precio - 0.2 * atr_h], key=lambda g: -g['hasta'])[:3]

    c = float(d1.c.iloc[-1])
    if c < e20d < e50d:
        sesgo = 'bajista'
    elif c > e20d > e50d:
        sesgo = 'alcista'
    else:
        sesgo = 'neutral'

    r2 = lambda x: round(float(x), 2)
    ops = []
    def op(lado, zona, objetivos, a_favor):
        if not zona:
            return
        if lado == 'venta':
            entrada = (zona['desde'] + zona['hasta']) / 2; sl = zona['hasta'] + 0.6 * atr_h; riesgo = sl - entrada
            tps = [(g['desde'] + g['hasta']) / 2 for g in objetivos if (g['desde'] + g['hasta']) / 2 < entrada - riesgo]
            tp1 = tps[0] if tps else entrada - 1.5 * riesgo; tp2 = tps[1] if len(tps) > 1 else entrada - 3 * riesgo
        else:
            entrada = (zona['desde'] + zona['hasta']) / 2; sl = zona['desde'] - 0.6 * atr_h; riesgo = entrada - sl
            tps = [(g['desde'] + g['hasta']) / 2 for g in objetivos if (g['desde'] + g['hasta']) / 2 > entrada + riesgo]
            tp1 = tps[0] if tps else entrada + 1.5 * riesgo; tp2 = tps[1] if len(tps) > 1 else entrada + 3 * riesgo
        ops.append({'lado': lado, 'entrada': r2(entrada), 'sl': r2(sl), 'tp1': r2(tp1), 'tp2': r2(tp2),
                    'rb1': r2(abs(tp1 - entrada) / riesgo), 'a_favor': a_favor,
                    'condicion': 'Entrar solo si en 15 m aparece rechazo dentro de la zona (mecha o vela envolvente). Si no, no hay operación.'})
    vende_favor = sesgo in ('bajista', 'neutral'); compra_favor = sesgo in ('alcista', 'neutral')
    op('venta', arriba[0] if arriba else None, abajo, vende_favor)
    op('compra', abajo[0] if abajo else None, arriba, compra_favor)

    zonas = [{'tipo': 'venta', 'desde': r2(g['desde']), 'hasta': r2(g['hasta']), 'peso': g['peso'], 'motivo': ', '.join(dict.fromkeys(g['motivos']))} for g in arriba] + \
            [{'tipo': 'compra', 'desde': r2(g['desde']), 'hasta': r2(g['hasta']), 'peso': g['peso'], 'motivo': ', '.join(dict.fromkeys(g['motivos']))} for g in abajo]
    plan = {
        'fecha': hoy.strftime('%Y-%m-%d'), 'generado': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ'),
        'mercado': 'XAUUSD', 'fuente': 'Hyperliquid xyz:GOLD', 'precio': r2(precio), 'sesgo': sesgo,
        'atr_diario': r2(atr_d), 'atr_1h': r2(atr_h),
        'contexto': {'ema20_d': r2(e20d), 'ema50_d': r2(e50d), 'ayer': {'max': r2(ayer.h), 'min': r2(ayer.l), 'cierre': r2(ayer.c)}, 'pivote': r2(P)},
        'zonas': zonas, 'operaciones': ops,
        'notas': [],
    }
    return plan


def escribir(plan):
    json.dump(plan, open(os.path.join(RAIZ, 'atalaya', 'plan-oro.json'), 'w'), ensure_ascii=False, indent=1)
    f = lambda x: f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    t = [f"# Plan del oro · {plan['fecha']}", '',
         f"Precio {f(plan['precio'])} · sesgo **{plan['sesgo']}** · ATR diario {f(plan['atr_diario'])} · ATR 1 h {f(plan['atr_1h'])}", '',
         '## Zonas', '']
    for z in plan['zonas']:
        t.append(f"- {z['tipo'].capitalize()}: {f(z['desde'])} – {f(z['hasta'])} ({z['motivo']})")
    t += ['', '## Operaciones', '']
    for o in plan['operaciones']:
        t.append(f"- **{o['lado'].capitalize()}** {'a favor' if o['a_favor'] else 'contra'} del sesgo: entrada {f(o['entrada'])}, SL {f(o['sl'])}, TP1 {f(o['tp1'])} (R:B {str(o['rb1']).replace('.', ',')}), TP2 {f(o['tp2'])}. {o['condicion']}")
    if plan['notas']:
        t += ['', '## Notas', ''] + [f'- {n}' for n in plan['notas']]
    t += ['', '_Análisis técnico automático, no es asesoramiento financiero._', '']
    open(os.path.join(BASE, 'diario', plan['fecha'] + '.md'), 'w').write('\n'.join(t))


if __name__ == '__main__':
    plan = main()
    escribir(plan)
    print(json.dumps(plan, ensure_ascii=False, indent=1))
