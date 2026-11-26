# Conocimiento acumulado sobre el oro

Memoria de la investigación diaria. Cada sesión la lee antes de empezar y la actualiza al terminar.
Solo se escribe aquí lo que los datos sostienen. Las ideas sin probar van en `hipotesis.json` como pendientes.

**Datos base:** PAXG/USDT de Binance (oro tokenizado), velas de 1 h desde 2021 (2020 se excluye por baja liquidez).
**Muestra:** 2021-01-01 → 2024-06-30. **Validación (fuera de muestra):** 2024-07-01 → hoy.
**Costo supuesto:** 3 pb por operación (≈ 1 USD por onza).

## Hallazgos firmes

1. **El oro cambió de régimen a mediados de 2024** (H003 y H004). Entre 2021 y mediados de 2024 los excesos se revertían:
   - Las rupturas del rango asiático durante Londres fallaban: −5,6 pb por operación antes de costos, t ≈ −3,1. (El t = −4,7 que se citó al principio incluía el costo; corregido el 26-11.)
   - Los días de rango extremo se corregían al día siguiente.

   Desde mediados de 2024 pasa lo contrario: las rupturas tienden a continuar (+6,7 pb antes de costos) y los días extremos también.
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

- **H006 · Detector de régimen por ratio de varianzas (VR(4), 30 días):** rechazado. En el oro de 1 h el VR está casi siempre por debajo de 1 (96 % de las rupturas en muestra, 83 % en validación), así que el umbral 1 no separa regímenes; en validación la regla pierde (−0,8 pb bruto). La variante adaptativa (dirección de las últimas 20 rupturas) tampoco es significativa.
  - Pista no confirmada: en ambos tramos las rupturas con VR > 1 rinden más que con VR < 1, pero con solo 22 casos en muestra. Un umbral relativo ya estaría contaminado por haber visto la validación: solo podría confirmarse en vivo.
- **H002 · Martillo diario tras caída:** sin ventaja. No usar un martillo diario como razón para comprar.
- **H003 y H004 como reglas fijas:** ver el cambio de régimen en "Hallazgos firmes".

## Lecciones de método

- Mirar siempre la media **bruta** (antes de costos), no solo la neta. Una señal "muy negativa" puede ser solo el costo.
- Si una señal sale negativa, probar la **invertida** antes de concluir que "lo contrario funciona".

## Cómo usar esto en el plan diario

- El plan mecánico (`plan_diario.py`) da zonas por coincidencia de niveles.
- Mientras no exista un detector de régimen validado (H006 falló el 26-11), se mantiene la regla prudente: **a favor del sesgo diario y con confirmación en 15 m**.
- Desde julio de 2024 el régimen premia la continuación. Los días de ruptura fuerte, no apostar contra el movimiento.

## Registro de sesiones

- **2026-11-26** · Día 1:
  - Infraestructura creada.
  - Probadas H001–H005.
  - Hallazgo principal: cambio de régimen a mediados de 2024.
  - Siguiente paso: H006 (detector de régimen).
- **2026-11-26** · Sesión 2:
  - Probada H006 (detector de régimen por ratio de varianzas): rechazada; el VR de 1 h del oro casi nunca supera 1.
  - Plan del día revisado: venta a favor del sesgo bajista pero contra el fuerte rebote de ayer; se exige confirmación. Acción de Gracias en EE. UU.
  - Seguimiento H005: sin datos nuevos (próxima medición el lunes 30-11, con el domingo 29-11).
  - Siguiente paso: H012 (firma de la apertura de Nueva York) o H010 (compresión antes de la expansión).
