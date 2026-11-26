# Investigación diaria del oro

Programa de investigación continua para encontrar patrones del oro que se sostengan con datos, y para producir cada mañana un plan operativo que Atalaya dibuja en el gráfico (botón **Plan IA** en XAU/USD).

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `CONOCIMIENTO.md` | Memoria: hallazgos firmes, ideas en seguimiento, descartes y registro de sesiones. **Se lee primero.** |
| `hipotesis.json` | Registro de todas las hipótesis (pendientes, probadas y su resultado). |
| `seguimiento.json` | Resultados en vivo de las hipótesis en seguimiento (datos que no existían al probarlas). |
| `motor.py` | Carga de datos y prueba de hipótesis con validación fuera de muestra. |
| `datos.py` | Descarga y actualiza las velas: PAXG de Binance desde 2020 y XAU de Hyperliquid. |
| `plan_diario.py` | Genera `atalaya/plan-oro.json` y `diario/AAAA-MM-DD.md`. |
| `hipotesis/` | El código de cada prueba, para poder repetirla. |
| `diario/` | Un plan por día. |

## Rutina de cada sesión (≈ 25 minutos)

1. Leer `CONOCIMIENTO.md` y las hipótesis pendientes de `hipotesis.json`.
2. Ejecutar `python3 investigacion/datos.py` para actualizar los datos (la primera vez tarda ~5 min).
3. Ejecutar `python3 investigacion/plan_diario.py`. Revisar el plan con lo aprendido; si se ajusta algo, añadirlo en `notas` del JSON y en el diario.
4. Actualizar `seguimiento.json`: el resultado de las señales en seguimiento que ya se puedan medir.
5. Investigar **una o dos hipótesis** (la pendiente más prometedora o una nueva que surja de los datos):
   - Escribir el código en `hipotesis/hNNN_nombre.py`.
   - Usar `motor.evaluar` y `motor.registrar`.
   - Contar los fallos igual que los aciertos.
6. Actualizar `CONOCIMIENTO.md` (hallazgos, seguimiento, descartes y una línea en el registro de sesiones).
7. Hacer commit y push.

## Reglas para no engañarse

- Una idea se diseña mirando solo la **muestra** (2021 → junio 2024). La **validación** (julio 2024 → hoy) se mira una vez, al final.
- "Prometedora" exige el mismo sentido en ambos tramos: p < 0,05 en la muestra y p < 0,01 en la validación, después de costos, con al menos 30 operaciones en cada tramo.
- Ninguna idea pasa a "hallazgo firme" sin al menos 30 casos nuevos en `seguimiento.json`.
- Cuantas más ideas se prueban, más probable es encontrar una que funcione por azar: llevar la cuenta en `hipotesis.json` y ser más exigente a medida que crece.
- Nada de esto es asesoramiento financiero.
