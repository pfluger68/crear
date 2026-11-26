# Conocimiento acumulado sobre el oro

Memoria de la investigación diaria. Cada sesión la lee antes de empezar y la actualiza al terminar.
Solo se escribe aquí lo que los datos sostienen. Las ideas sin probar van en `hipotesis.json` como pendientes.

**Datos base:** PAXG/USDT de Binance (oro tokenizado), velas de 1 h desde 2021 (2020 se excluye por baja liquidez).
**Muestra:** 2021-01-01 → 2024-06-30. **Validación (fuera de muestra):** 2024-07-01 → hoy.
**Costo supuesto:** 3 pb por operación (≈ 1 USD por onza).

## Hallazgos firmes

1. **El oro cambió de régimen a mediados de 2024** (H003 y H004). Entre 2021 y mediados de 2024 los excesos se revertían:
   - Las rupturas del rango asiático durante Londres fallaban (t = −4,7).
   - Los días de rango extremo se corregían al día siguiente.

   Desde mediados de 2024 pasa lo contrario: las rupturas tienden a continuar y los días extremos también.
   **Consecuencia:** ninguna regla fija de "ruptura" o "reversión" es estable. Primero hay que saber en qué régimen está el mercado (ver H006).
2. **La volatilidad se concentra entre las 12 y las 15 UTC** (H001). Es la apertura de Nueva York y los datos de EE. UU.: el movimiento medio por hora es ~19 pb, frente a 10–13 pb en Asia.
   - Sábado y domingo la volatilidad cae a la mitad (~9 pb), porque solo cotiza el oro tokenizado.
   - Las medias horarias de retorno son pequeñas y no se usan como señal: serían ruido.

## En seguimiento (prometedoras o débiles, se verifican con datos nuevos)

- **H005 · Reversión del fin de semana de PAXG.** Si PAXG se mueve más de 0,4 % entre el viernes 21 UTC y el domingo 21 UTC, a la reapertura del oro físico revierte en las 3 h siguientes.
  - Muestra: +21,6 pb por operación, 70 % de aciertos, t = 2,35.
  - Validación: +16,1 pb, 55 % de aciertos, t = 1,15 (no significativo).
  - Con 12 h no funciona.
  - **Cada domingo:** anotar en `seguimiento.json` si hubo señal y el resultado.

## Descartado

- **H002 · Martillo diario tras caída:** sin ventaja. No usar un martillo diario como razón para comprar.
- **H003 y H004 como reglas fijas:** ver el cambio de régimen en "Hallazgos firmes".

## Cómo usar esto en el plan diario

- El plan mecánico (`plan_diario.py`) da zonas por coincidencia de niveles.
- Mientras no exista un detector de régimen validado, se mantiene la regla prudente: **a favor del sesgo diario y con confirmación en 15 m**.
- Desde julio de 2024 el régimen premia la continuación. Los días de ruptura fuerte, no apostar contra el movimiento.

## Registro de sesiones

- **2026-11-26** · Día 1:
  - Infraestructura creada.
  - Probadas H001–H005.
  - Hallazgo principal: cambio de régimen a mediados de 2024.
  - Siguiente paso: H006 (detector de régimen).
