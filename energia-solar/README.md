# Proyecto: casa con energía solar (Guernica)

Objetivo: tener electricidad propia en el terreno de Guernica, primero para no sufrir
los cortes y, a futuro, **no depender de la red eléctrica**.

El proyecto se arma **por etapas**, comprando de a una pieza según el presupuesto.
Cada compra sirve sola o se suma a la anterior: nada se tira.

## Documentos

| Archivo | Para qué sirve |
|---|---|
| [primer-anio-alquilando.md](primer-anio-alquilando.md) | **Empezar acá:** equipo móvil contra los cortes mientras alquilo, sin tocar la casa |
| [lista-de-compras.md](lista-de-compras.md) | Qué comprar en cada etapa, con medidas exactas (cables, fusibles, térmicas) |
| [esquema-de-conexion.md](esquema-de-conexion.md) | Cómo se conecta todo |
| [instalacion-paso-a-paso.md](instalacion-paso-a-paso.md) | Orden de armado, configuración del inversor y controles de seguridad |
| [emergencia-y-terreno.md](emergencia-y-terreno.md) | Cómo aguantar un apagón largo y qué mirar al comprar el terreno |

## Consumo de referencia (factura Edesur actual)

| Mes | kWh/mes | kWh/día |
|---|---|---|
| Enero 2026 | 278 | ~9,0 |
| Febrero 2026 | 235 | ~8,4 |
| Marzo 2026 | 217 | ~7,0 |
| Abril 2026 | 137 | ~4,6 |
| Mayo 2026 | 115 | ~3,7 |
| Junio 2026 | 97 | ~3,2 |

- El consumo alto es en **verano** (aire acondicionado / ventiladores), que coincide con
  la época de más sol: buena noticia.
- Sol en Guernica (horas de sol pico): **~6 en verano**, **~2,5 a 3 en invierno**.
- ⚠️ Si la casa nueva **no tiene gas de red** y se calienta agua o ambientes con
  electricidad, el consumo sube mucho (un termotanque eléctrico suma 100–150 kWh/mes).
  Para eso conviene garrafa o **termotanque solar**, no más paneles.

## El sistema completo (meta final)

| Componente | Medida | Por qué |
|---|---|---|
| Inversor híbrido | **48 V – 5 kW**, onda senoidal pura, con MPPT | Cerebro del sistema: maneja sol, batería, red y grupo electrógeno |
| Paneles | **5 × 550 W** (≈2,75 kWp), ampliable a 8 | Cubren enero (9 kWh/día) con margen |
| Baterías | **LiFePO4 48 V**, 2 × 5 kWh = **10 kWh** | ~2 días de invierno sin sol, o noches de verano con aire |
| Respaldo | Grupo electrógeno **2–3 kVA** (ideal tipo *inverter*) | Para rachas de varios días nublados |

## Plan por etapas (resumen)

| Etapa | Qué se compra | Qué se logra | Costo aprox. |
|---|---|---|---|
| **1** | Inversor + 1 batería 5 kWh + protecciones | Funciona como **UPS**: los cortes dejan de notarse | USD 1.700 – 2.700 |
| **2** | 4–5 paneles + estructura + cableado | Generás tu energía; la factura baja 70–90 % | USD 800 – 1.300 |
| **3** | 2.ª batería 5 kWh | Casi independiente | USD 900 – 1.500 |
| **4** | Grupo electrógeno + (opcional) 1–3 paneles más | Listo para desconectarte de la red | USD 300 – 900 |

> Los precios son orientativos (octubre 2026) y en Argentina cambian mucho: pedir
> siempre 2–3 presupuestos.

**Consejo:** aun cuando el sistema ya alcance, mantener la conexión a la red como respaldo
**hasta pasar un invierno completo** y ver cómo rinde. Recién ahí decidir la desconexión.

## Seguridad (leer siempre)

1. **Batería:** un cortocircuito de 48 V larga cientos de amperes al instante. Herramientas
   aisladas, sin anillos ni reloj, fusible pegado a la batería.
2. **220 V:** la conexión al tablero de la casa la hace un **electricista matriculado**.
3. **Altura:** preferir los paneles **en el suelo**, sobre estructura, en el terreno.
