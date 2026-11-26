"""Descarga y actualiza las velas del oro y de BTC.

- PAXG/USDT (Binance): oro tokenizado, historial desde agosto de 2020. Es la base de la investigación.
- XAU (Hyperliquid, contrato xyz:GOLD): el precio que muestra Atalaya. Sirve para el plan del día.

Los CSV quedan en investigacion/datos/ (no se suben al repositorio; se regeneran en cada ejecución).
- BTC/USDT (Binance): 1d desde 2017, 4h y 1h desde 2019, 15m desde 2023.

Uso: python3 investigacion/datos.py [oro|btc|todo]
"""
import csv, json, os, time, urllib.request

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos')
os.makedirs(DIR, exist_ok=True)
CAMPOS = ['t', 'o', 'h', 'l', 'c', 'v']


def _get(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={'content-type': 'application/json'} if body else {})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception:
            if intento == 3:
                raise
            time.sleep(2 * (intento + 1))


def _leer(path):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [[float(x) for x in row] for row in csv.reader(f) if row and row[0] != 't']


def _escribir(path, filas):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(CAMPOS)
        w.writerows(filas)


def binance(symbol='PAXGUSDT', intervalo='1h', desde='2020-08-01'):
    path = os.path.join(DIR, f'{symbol}_{intervalo}.csv')
    filas = _leer(path)
    inicio = int(filas[-1][0] * 1000) + 1 if filas else int(time.mktime(time.strptime(desde, '%Y-%m-%d')) * 1000)
    ahora = int(time.time() * 1000)
    while True:
        datos = _get(f'https://data-api.binance.vision/api/v3/klines?symbol={symbol}&interval={intervalo}&startTime={inicio}&limit=1000')
        if not datos:
            break
        for k in datos:
            if k[6] < ahora:  # solo velas cerradas
                filas.append([k[0] / 1000, float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5])])
        inicio = datos[-1][0] + 1
        if len(datos) < 1000:
            break
    _escribir(path, filas)
    return path, len(filas)


def hyperliquid(coin='xyz:GOLD', intervalo='1h', velas=5000):
    path = os.path.join(DIR, f'XAU_HL_{intervalo}.csv')
    seg = {'15m': 900, '1h': 3600, '4h': 14400, '1d': 86400}[intervalo]
    fin = int(time.time() * 1000)
    datos = _get('https://api.hyperliquid.xyz/info', {'type': 'candleSnapshot', 'req': {
        'coin': coin, 'interval': intervalo, 'startTime': fin - seg * 1000 * velas, 'endTime': fin}})
    filas = [[d['t'] / 1000, float(d['o']), float(d['h']), float(d['l']), float(d['c']), float(d['v'])]
             for d in datos if d['T'] < fin]
    _escribir(path, filas)
    return path, len(filas)


if __name__ == '__main__':
    import sys
    que = sys.argv[1] if len(sys.argv) > 1 else 'todo'   # oro | btc | todo
    if que in ('oro', 'todo'):
        for iv in ('1h', '15m', '1d'):
            print(*binance('PAXGUSDT', iv, '2020-08-01' if iv != '15m' else '2023-01-01'))
        for iv in ('15m', '1h', '4h', '1d'):
            print(*hyperliquid('xyz:GOLD', iv))
    if que in ('btc', 'todo'):
        for iv, desde in (('1d', '2017-09-01'), ('4h', '2019-01-01'), ('1h', '2019-01-01'), ('15m', '2023-01-01')):
            print(*binance('BTCUSDT', iv, desde))
