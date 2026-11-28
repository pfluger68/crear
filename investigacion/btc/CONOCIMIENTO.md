# Conocimiento acumulado sobre BTC

Memoria de la investigación diaria de BTC. Cada sesión la lee antes de empezar y la actualiza al terminar.
Las reglas de método son las de `investigacion/README.md`.

**Datos base:** BTC/USDT de Binance, velas de 1 h desde 2019, diarias desde 2017.
**Muestra:** 2019-01-01 → 2024-06-30. **Validación (fuera de muestra):** 2024-07-01 → hoy.
**Costo supuesto:** 10 pb por operación. Es más de 3 veces el del oro: cualquier ventaja tiene que superar eso.

## Hallazgos firmes

1. **Los costos mandan en BTC.** Las ideas intradía de 4–6 horas dan ventajas brutas de 2–9 pb, por debajo de los 10 pb que cuesta operar. Hay que buscar en horizontes de días o en movimientos grandes (B006, B007).
   Pero alargar el horizonte **no basta por sí solo** (B008): con señales diarias de 3–5 días, el ruido crece más que la ventaja.
2. **En BTC, la ruptura del rango asiático durante Londres suele fallar** (B002), en ambos tramos, y en casi todos los años desde 2019. El oro hacía lo mismo hasta 2024. Hacer lo contrario no cubre los costos (B006), pero **sirve como filtro: no perseguir esas rupturas**.
3. **La volatilidad máxima está entre las 13 y las 16 UTC** (apertura de EE. UU.; ~50 pb por hora frente a ~31 pb a las 04 UTC). Sábado y domingo la volatilidad baja un tercio (B001).

## En seguimiento

- **B009 · Hora 20–22 UTC:** media positiva en el perfil horario. Pendiente de validar (puede ser ruido).

## Descartado

- **B003** · Reversión tras un día de rango extremo: sin ventaja.
- **B004** · "Gap de CME" del fin de semana: sin ventaja. Con 30 casos en la validación, ninguna dirección es significativa.
- **B005 y B007** · Seguir o desvanecer el impulso de la apertura de Wall Street: sin ventaja después de costos.
- **B008** · Horizonte de 3–5 días con velas diarias (tendencia EMA 20/50, ruptura del rango de 7 días, reversión tras caída > 1,5 ATR): ninguna pasa, ni invertida.
  - La tendencia EMA dio +80 pb brutos en la muestra (p = 0,07), pero +1 pb en la validación.
  - Lección: en BTC, la muestra 2019–2024 contiene la gran tendencia 2020–21, y eso infla cualquier regla de seguir la tendencia. Ojo con el azar de referencia (p95 ≈ 50 pb a 5 días): un umbral de "ventaja" en BTC diario tiene que ser alto.

## Cómo usar esto en el plan diario

- Zonas por coincidencia de niveles (`plan_diario.py btc`), con el sesgo de las medias diarias.
- No perseguir rupturas tempranas de Londres.
- Los objetivos deben estar lejos: con un stop razonable, el beneficio esperado tiene que superar con holgura los costos.

## Registro de sesiones

- **2026-11-26** · Día 1:
  - Datos desde 2017.
  - Probadas B001–B007.
  - Lección de método: mirar la media bruta y la señal invertida (añadido al motor).
- **2026-11-27** · Día 2: B008 (horizonte largo, 3 variantes) rechazada en ambos sentidos. Probadas: 8 hipótesis de BTC; con tantas pruebas, el umbral efectivo sube.
