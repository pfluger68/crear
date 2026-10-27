# Lista de compras detallada

Precios orientativos en USD (octubre 2026). Las medidas están pensadas para el sistema
de **48 V – 5 kW**. Antes de comprar, **revisar la hoja de datos (datasheet) del inversor
elegido**: algunos valores (tensión máxima de paneles, tamaño de bornes) cambian según
el modelo.

---

## Etapa 1 — Inversor + batería (fin de los cortes)

### Equipos principales

| # | Ítem | Especificación a pedir | Precio aprox. |
|---|---|---|---|
| 1 | **Inversor híbrido** | 48 V, 5 kW (5.000–5.500 W), **onda senoidal pura**, MPPT incluido, entrada de paneles hasta **≥ 450–500 V**, compatible con **LiFePO4** y con **comunicación BMS** (CAN o RS485). Que acepte entrada de red **y** de grupo electrógeno. | 600 – 1.000 |
| 2 | **Batería LiFePO4** | 48 V nominal (51,2 V, 16 celdas), **100 Ah (≈5 kWh)**, con BMS, en formato rack/gabinete, **apta para conectar en paralelo** y con protocolo compatible con el inversor (muchas usan el protocolo "Pylontech"). Si trae llave/breaker propio, mejor. | 900 – 1.500 |

> 💡 Pedirle al vendedor que confirme por escrito que **esa batería comunica con ese
> inversor**. Es la combinación que más problemas da.

### Lado batería (corriente continua, la parte más peligrosa)

Corriente máxima: 5.000 W ÷ 44 V ≈ **115–120 A**.

| # | Ítem | Especificación | Cantidad |
|---|---|---|---|
| 3 | Cable batería–inversor | Cobre flexible **35 mm²**, rojo y negro, lo más corto posible (**≤ 2 m**) | 2 m rojo + 2 m negro |
| 4 | Fusible de batería | **NH00 de 125 A** (tipo gG, 500 V) **con base portafusible NH00**, ubicado a menos de 30 cm del borne positivo. Alternativa: fusible **Clase T 150 A**. ❌ No usar fusibles ANL de auto (son para 32 V). | 1 base + 2 fusibles (uno de repuesto) |
| 5 | Seccionador DC de batería | Llave de corte DC **≥ 125 A, apta 80 V DC o más** (si la batería ya trae breaker propio, se puede omitir) | 1 |
| 6 | Terminales de cobre estañado | Para **35 mm²**, con agujero según bornes (**M8** es lo más común; verificar) | 8 (con repuestos) |
| 7 | Termocontraíble | Rojo y negro, para 35 mm² | 1 m de cada uno |

### Lado corriente alterna (220 V — lo conecta el electricista)

| # | Ítem | Especificación | Cantidad |
|---|---|---|---|
| 8 | Térmica entrada (red → inversor) | Bipolar **32 A**, curva C | 1 |
| 9 | Térmica salida (inversor → casa) | Bipolar **25 A**, curva C | 1 |
| 10 | Disyuntor diferencial (salida) | Bipolar **40 A – 30 mA** | 1 |
| 11 | **Llave conmutadora by-pass** | Bipolar **40 A, 3 posiciones (Red – 0 – Inversor)**. Si el inversor se rompe, con esta llave la casa vuelve a la red directa. **Muy recomendada.** | 1 |
| 12 | Cable AC | **6 mm²** para la entrada, **4 mm²** para la salida (unipolar o subterráneo según el tramo) + tierra verde-amarilla | según distancias |
| 13 | Gabinete / tablero | Estanco, con riel DIN, para las térmicas y el disyuntor | 1 |

### Puesta a tierra

| # | Ítem | Especificación |
|---|---|---|
| 14 | Jabalina | Cobre-acero **3/4" × 1,5 m** (o 2 m) con tomacable y caja de inspección |
| 15 | Cable de tierra | Verde-amarillo **6 mm²** (gabinetes, inversor y, en la etapa 2, la estructura de los paneles) |

### Herramientas

| Herramienta | Para qué | Precio aprox. |
|---|---|---|
| Multímetro digital (que mida DC hasta 600 V y tenga pinza amperométrica DC ideal) | Medir tensiones y polaridad **antes** de conectar | 20 – 60 |
| Crimpadora hidráulica o de impacto para 10–70 mm² | Terminales de batería | 25 – 50 |
| Pinza crimpadora MC4 + llaves MC4 | Conectores de paneles (etapa 2) | 15 – 25 |
| Destornilladores y llaves **aisladas 1000 V** | Trabajar cerca de la batería | 15 – 30 |
| Pelacables, cúter, pistola de calor | Preparar cables y termocontraíble | 15 – 25 |

**Subtotal Etapa 1: USD 1.700 – 2.700** (con herramientas y protecciones)

---

## Etapa 2 — Paneles solares

### Paneles y estructura

| # | Ítem | Especificación | Cantidad |
|---|---|---|---|
| 16 | **Paneles** | Monocristalinos **550 W** (aprox. Voc 49–50 V, Isc ~14 A, 2,28 × 1,13 m). Comprar **todos del mismo modelo** y, si se puede, del mismo lote. | **4 o 5** |
| 17 | Estructura al suelo | Aluminio o hierro galvanizado, **inclinación 45°**, mirando al **norte**. | para 5 paneles (dejar lugar para 8) |
| 18 | Base | Patas con dados de hormigón o tornillos de anclaje al suelo | según estructura |

**Conexión de paneles:** todos **en serie** (un solo "string"):

| Paneles en serie | Tensión de trabajo (Vmp) | Tensión máx. en invierno con frío (Voc a −5 °C) |
|---|---|---|
| 4 | ~168 V | ~215 V |
| 5 | ~210 V | ~270 V |
| 8 (ampliación futura) | ~335 V | ~430 V |

✅ Todo dentro del rango típico de un inversor de 5 kW (MPPT 120–450 V, máx. 500 V).
⚠️ **Verificar en el datasheet del inversor** la tensión máxima de entrada de paneles
antes de pasar de 6 paneles en serie.

### Cableado y protecciones de paneles

| # | Ítem | Especificación | Cantidad |
|---|---|---|---|
| 19 | Cable solar | **4 mm²** (si el tramo paneles → inversor supera los 40 m, usar **6 mm²**), rojo y negro, apto intemperie/UV | 2 × distancia + 10 % |
| 20 | Conectores MC4 | Pares macho/hembra, de buena marca | 4 pares (2 de repuesto) |
| 21 | Seccionador DC de paneles | **1000 V DC – 32 A**, en caja estanca, cerca del inversor | 1 |
| 22 | Descargador de sobretensión DC | Tipo 2, **600 V DC** (protege contra rayos) | 1 |
| 23 | Caño corrugado o caño enterrado | Para llevar el cable solar desde los paneles hasta la casa | según distancia |
| 24 | Tierra de la estructura | Verde-amarillo 6 mm² hasta la jabalina | según distancia |

> Con un solo string **no hacen falta fusibles en los paneles**. Si en el futuro se arman
> 2 strings en paralelo, ahí sí se agrega un fusible de 20 A DC por string.

**Subtotal Etapa 2: USD 800 – 1.300**

---

## Etapa 3 — Segunda batería

| # | Ítem | Especificación |
|---|---|---|
| 25 | Batería LiFePO4 | **Idéntica a la primera** (misma marca, modelo y capacidad) |
| 26 | Cables de paralelo | 35 mm², **mismo largo** para las dos baterías |
| 27 | Barras de cobre (busbar) | 2 barras (+ y −), **≥ 250 A** |
| 28 | Fusible por batería | Un fusible NH00 125 A (o Clase T) **por cada batería** |
| 29 | Cable de comunicación | El que indique el fabricante para encadenar las baterías (BMS maestro/esclavo) |

Cable del busbar al inversor: **35 mm²** (sigue siendo el mismo inversor de 5 kW).

**Subtotal Etapa 3: USD 900 – 1.500**

---

## Etapa 4 — Respaldo y autonomía total

| # | Ítem | Especificación | Precio aprox. |
|---|---|---|---|
| 30 | Grupo electrógeno | **2–3 kVA**, ideal tipo **inverter** (energía "limpia" que el inversor acepta mejor) | 300 – 600 |
| 31 | Bidones aptos combustible | 2–3 × 20 L | 20 – 40 |
| 32 | Estabilizador de nafta | Para que la nafta guardada dure 12 meses o más | 10 |
| 33 | Llave conmutadora Red / Grupo | Bipolar 40 A, antes de la entrada AC del inversor | 20 – 40 |
| 34 | (Opcional) 1–3 paneles más | Mismo modelo que los anteriores, se suman al string en serie | 100 – 150 c/u |

**Subtotal Etapa 4: USD 300 – 900**

---

## Repuestos que conviene tener siempre

- 2 fusibles NH00 125 A
- 2 pares de conectores MC4
- 4 terminales de 35 mm²
- 1 térmica bipolar de 25 A
- Cinta aisladora y termocontraíble

## Ahorro con cosas no eléctricas (muy recomendado)

| Ítem | Para qué |
|---|---|
| Termotanque solar o a gas | Calentar agua sin electricidad (lo que más gasta) |
| Cocina a garrafa + 2 garrafas | Cocinar sin vaciar la batería |
| Tanque de agua elevado | La bomba trabaja de día con el sol; de noche el agua baja por gravedad |
| Aire acondicionado **inverter** | Consume mucho menos y arranca suave |
| Lámparas LED en toda la casa | Iluminación casi sin consumo |
