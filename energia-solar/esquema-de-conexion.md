# Esquema de conexión

## Sistema completo

```
                     PANELES (5 × 550 W en serie)
                     ┌────┬────┬────┬────┬────┐
                     │ +  │    │    │    │  − │
                     └─┬──┴────┴────┴────┴──┬─┘
                       │   cable solar 4 mm² │
                       ▼                     ▼
              ┌──────────────────────────────────┐
              │ Seccionador DC 1000 V / 32 A     │
              │ + Descargador sobretensión DC    │──── tierra
              └────────────────┬─────────────────┘
                               │ (PV+ / PV−)
                               ▼
 RED EDESUR                ┌────────────────────┐                 TABLERO
     │                     │                    │                 DE LA CASA
     ▼                     │     INVERSOR       │
 [Llave Red/Grupo] ──►     │     HÍBRIDO        │
     ▲            [Térm.   │   48 V – 5 kW      │──► [Térm. 25 A] ──► [Diferencial] ──┐
     │             32 A] ─►│ AC IN       AC OUT │                    40 A / 30 mA    │
 GRUPO ELECTRÓGENO         │                    │                                    │
                           │    BAT+    BAT−    │                                    │
                           └─────┬───────┬──────┘                                    │
                                 │       │  cable 35 mm²                             │
                   [Seccionador DC 125 A]│                                           │
                                 │       │                                           │
                 [Fusible NH00 125 A]    │                                           │
                                 │       │                                           │
                           ┌─────▼───────▼──────┐                                    │
                           │  BATERÍA LiFePO4   │                                    │
                           │  48 V – 5 kWh      │                                    │
                           └────────────────────┘                                    │
                                                                                     │
 ┌───────────────────────────────────────────────────────────────────────────────────┘
 │
 ▼
 LLAVE BY-PASS (3 posiciones):
   Posición "Inversor" → la casa se alimenta desde el inversor (uso normal)
   Posición "0"        → todo cortado (para mantenimiento)
   Posición "Red"      → la casa va directo a la red (si el inversor falla)
```

## Las 6 conexiones (de a una)

| # | Desde | Hasta | Cable | Protección |
|---|---|---|---|---|
| 1 | Batería (+ y −) | Inversor BAT | 35 mm² | Fusible NH00 125 A + seccionador DC |
| 2 | Paneles | Inversor PV | Solar 4 mm² | Seccionador DC 1000 V + descargador |
| 3 | Red / grupo | Inversor AC IN | 6 mm² | Térmica 32 A |
| 4 | Inversor AC OUT | Llave by-pass → tablero | 4 mm² | Térmica 25 A + diferencial 30 mA |
| 5 | Inversor, gabinetes, estructura | Jabalina | Verde-amarillo 6 mm² | — |
| 6 | Batería (puerto BMS) | Inversor (puerto BMS) | Cable de comunicación | — |

## Etapa 3: dos baterías en paralelo

```
       BATERÍA 1                 BATERÍA 2
      +        −                +        −
      │        │                │        │
   [Fus.]      │             [Fus.]      │
      │        │                │        │
  ════╪════════│════════════════╪════════│═══  Busbar (+)
               │                         │
  ═════════════╪═════════════════════════╪═══  Busbar (−)
      │                    │
      └─── al inversor ────┘   (cables 35 mm²)

  Regla: los cables de cada batería al busbar deben tener EL MISMO LARGO,
  para que las dos baterías se carguen y descarguen parejo.
```

## Notas para el electricista

- Revisar en el manual del inversor la conexión **neutro–tierra en modo isla**
  (cuando no hay red, algunos inversores necesitan unir neutro y tierra a la salida para
  que funcione el disyuntor diferencial).
- **Nunca** unir la salida del inversor (AC OUT) con la red. La llave by-pass tiene que
  ser de **tipo conmutadora** (corta una antes de conectar la otra).
- La entrada de red y la del grupo electrógeno también van por una llave conmutadora:
  **nunca** las dos conectadas a la vez.
