# Primer año: alquilando en Guernica

Situación: 1 año en una casa alquilada, con **cortes frecuentes**, sin poder hacer
cambios en la instalación ni en el terreno.

Idea central: **armar la Etapa 1 como un equipo móvil ("carrito UPS")** que se enchufa a
un tomacorriente común. No se toca el tablero ni se perfora nada. Cuando te mudes a tu
terreno, ese mismo equipo pasa a ser el corazón del sistema definitivo: **no se pierde
un peso**.

---

## Cómo funciona

```
 Tomacorriente de la casa (con tierra)
          │  cable con ficha, 2,5 mm²
          ▼
 ┌─────────────────────── CARRITO ───────────────────────┐
 │                                                       │
 │   INVERSOR HÍBRIDO 48 V – 5 kW  ◄──►  BATERÍA LiFePO4  │
 │          │                            48 V – 5 kWh     │
 │          ▼                                             │
 │   Cajita: térmica 16 A + diferencial 30 mA             │
 │          │                                             │
 │   2–3 tomacorrientes / zapatillas                      │
 └──────────┼────────────────────────────────────────────┘
            ▼
   Heladera · router · lámparas · TV · cargadores · (bomba si es enchufable)
```

- **Con luz:** el inversor deja pasar la red a los aparatos y mantiene la batería llena.
- **Corte de luz:** en ~10 milisegundos pasa a batería. La heladera y el router ni se
  enteran.
- **Vuelve la luz:** recarga la batería solo.

---

## Qué comprar

| Ítem | Especificación | Precio aprox. (USD) |
|---|---|---|
| Inversor híbrido | El **mismo** de la guía: 48 V – 5 kW, senoidal pura, MPPT, LiFePO4 con BMS | 600 – 1.000 |
| Batería LiFePO4 | La **misma** de la guía: 48 V – 100 Ah (5 kWh), apta para paralelo | 900 – 1.500 |
| Carrito o rack con ruedas | Metálico, que aguante ~60 kg (batería ~45 kg + inversor ~12 kg) | 50 – 100 |
| Lado batería | Cable 35 mm², fusible NH00 125 A con base, terminales (igual que la guía) | 60 – 100 |
| Cable de entrada | **2,5 mm²** tripolar (con tierra), ficha **10 A** (o 20 A si hay tomacorriente de 20 A), máx. 5 m | 15 – 25 |
| Cajita de salida | Gabinete chico con **térmica bipolar 16 A + diferencial 25 A / 30 mA** y 2–3 tomacorrientes | 40 – 80 |
| Lámparas LED recargables | Se enroscan en los portalámparas de siempre y **siguen alumbrando en un corte** (sin tocar la instalación) | 5 – 10 c/u |
| Herramientas | Multímetro, crimpadora, llaves aisladas | 50 – 100 |

**Total: ~USD 1.700 – 2.900**, y **todo** se reutiliza en tu terreno.

> Pedile a un electricista que revise una sola vez el carrito armado (puesta a tierra a
> través de la ficha, conexión de la cajita de salida y neutro–tierra en modo isla).
> Es un trabajo chico y no toca la casa.

### Opcional: grupo electrógeno inverter (2–3 kVA)

Para cortes de varios días (tormentas, olas de calor). Es portátil y sirve igual en el
terreno propio (es la Etapa 4).

### Opcional: 2–4 paneles en una estructura apoyada en el patio

Solo **con permiso del dueño**: estructura con contrapeso (bloques), sin anclar ni
perforar. Ayuda en cortes largos y baja algo la factura. Si no hay permiso, se deja
para el terreno propio: el primer año el carrito se recarga de la red.

---

## Configuración del inversor para este año (sin paneles)

| Parámetro | Valor | Por qué |
|---|---|---|
| Prioridad de salida | **Red primero** ("UTI" / "USB" / "SUB", según la marca) | La batería queda **siempre llena**, esperando el corte |
| Corriente de carga desde la red | **10 A** (≈550 W) | Para no exceder lo que da un tomacorriente común |
| Corte por batería baja | 46 – 48 V | Protege la batería |
| Resto | Igual que en [instalacion-paso-a-paso.md](instalacion-paso-a-paso.md) | |

---

## Qué enchufar (y qué no)

Un tomacorriente común da **como máximo ~2.200 W** en total (lo que consumen los aparatos
más la carga de la batería).

| ✅ Sí | ❌ No |
|---|---|
| Heladera / freezer | Aire acondicionado |
| Router, módem, celulares, notebook | Termotanque o calefactor eléctrico |
| TV, ventilador | Horno eléctrico, pava eléctrica, plancha |
| Lámparas de pie / LED | Lavarropas con calentamiento de agua |
| Bomba de agua **si es enchufable** | Cualquier cosa conectada fija al tablero |

Las **luces de techo** dependen del tablero, así que en un corte no van a encender
desde el carrito: para eso son las **lámparas LED recargables**.

Con solo lo esencial (~2,5–3 kWh/día), la batería de 5 kWh aguanta **entre 1,5 y 2
días** de corte.

---

## ⚠️ Prohibido

- **Nunca** usar un cable "macho-macho" para meter energía del carrito o del grupo
  electrógeno en un tomacorriente de la casa. Energiza la red y puede **matar a un
  operario** de Edesur o a alguien de tu casa, además de quemar el equipo.
- El grupo electrógeno **siempre afuera**, nunca en un lugar cerrado (monóxido de carbono).

---

## Cuando te mudes a tu terreno

1. El carrito pasa a ser la **Etapa 1** completa: el electricista lo conecta fijo al
   tablero (térmicas, llave by-pass), como dice la guía.
2. Se suman los paneles (**Etapa 2**) y se cambia la prioridad a **SBU** (solar primero).
3. Se sigue con la **Etapa 3** (2.ª batería) y la **Etapa 4**.

Mientras alquilás, podés usar el año para **elegir bien el terreno**
(ver [emergencia-y-terreno.md](emergencia-y-terreno.md)).
