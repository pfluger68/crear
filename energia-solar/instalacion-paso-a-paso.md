# Instalación paso a paso

> ⚠️ Leer completo antes de empezar. Trabajar **sin apuro**, de día y, si se puede,
> acompañado.

## Antes de empezar

- [ ] Leer el **manual del inversor** y el de la **batería** (especialmente las tablas de
      configuración).
- [ ] Sacarse anillos, reloj, pulseras y cadenas.
- [ ] Usar **herramientas aisladas**.
- [ ] Tener un **matafuegos ABC** a mano.
- [ ] Elegir el lugar: interior, **seco, ventilado, a la sombra**, entre 5 y 35 °C,
      lejos de dormitorios y de cosas que se prendan fuego. Inversor y batería **lo más
      cerca posible** entre sí (cable de batería ≤ 2 m).

---

## Etapa 1: inversor + batería

### 1. Montaje
1. Fijar el inversor a la pared (vertical, con **20–30 cm libres** arriba y abajo para
   ventilación).
2. Ubicar la batería en el piso o rack, cerca del inversor.
3. Clavar la **jabalina** y conectar la tierra al inversor y a los gabinetes.

### 2. Preparar los cables de batería
1. Cortar los cables de 35 mm² a medida (rojo = positivo, negro = negativo).
2. Pelar solo lo justo para que el cobre entre en el terminal.
3. Crimpar el terminal **bien firme** (tirar fuerte: no tiene que moverse).
4. Cubrir con termocontraíble.

### 3. Conectar la batería (inversor APAGADO, batería APAGADA)
1. Verificar que el inversor está **apagado** y el seccionador DC **abierto**.
2. Instalar la base NH00 con el fusible **pegada al positivo de la batería**.
3. Conectar primero el cable **negativo** (batería − → inversor BAT −).
4. Conectar el **positivo** pasando por el fusible y el seccionador (batería + → fusible
   → seccionador → inversor BAT +).
5. **Medir con el multímetro** en los bornes del inversor: tiene que dar **~51–53 V
   positivo**. Si da negativo → **polaridad invertida: NO encender**, corregir.
6. Ajustar todos los tornillos con firmeza (sin pasarse).
7. Conectar el **cable de comunicación BMS** entre batería e inversor.

### 4. Primer encendido
1. Encender la batería (su botón o breaker).
2. Cerrar el seccionador DC.
3. Encender el inversor.
4. Configurar (ver tabla de abajo).
5. Probar: enchufar algo chico (una lámpara) en la salida y ver que funcione.

### 5. Conexión a la casa (CON ELECTRICISTA)
1. Red → térmica 32 A → inversor **AC IN**.
2. Inversor **AC OUT** → térmica 25 A → diferencial → llave by-pass → tablero.
3. **Prueba de corte:** bajar la térmica de la red y verificar que la casa sigue con luz.

> 🟢 **Opción sin tocar el tablero:** arrancar enchufando solo la heladera, el router y
> algunas luces a la salida del inversor con una zapatilla. Así se aprende sin riesgo
> y después se pasa toda la casa con el electricista.

---

## Configuración del inversor (valores típicos LiFePO4 48 V)

Los nombres de los menús cambian según la marca: buscar el equivalente en el manual.
**Si la batería comunica por BMS, usar el modo de comunicación** (tipo "PYL" / "LIB") y el
inversor toma casi todos estos valores solo.

| Parámetro | Valor sugerido | Comentario |
|---|---|---|
| Tipo de batería | LiFePO4 / "LIB" / "PYL" / "USER" | Según compatibilidad |
| Tensión de carga (bulk/absorción) | **56,0 – 56,8 V** | 3,50–3,55 V por celda |
| Tensión de flotación | **54,0 V** | |
| Corte por batería baja | **46 – 48 V** | Protege la batería |
| Corriente máx. de carga total | **50 A** (≈0,5 C para 100 Ah) | Con 2 baterías se puede subir a 100 A |
| Corriente de carga desde red/grupo | **30 A** | Para no sobrecargar el grupo electrógeno |
| Prioridad de salida | **SBU** (Solar → Batería → Red) | Máxima independencia |
| Volver a la red cuando la batería baje a | **~50 V (≈50 %)** | Así **siempre queda reserva para un corte** |
| Volver a batería cuando suba a | **~54 V** | |
| Prioridad de carga | **Solar primero** | La red solo carga si hace falta |
| Rango de entrada AC | **APL / "Generador"** cuando se use grupo electrógeno | Acepta energía menos "limpia" |

---

## Etapa 2: paneles

### 1. Estructura
1. Ubicarla mirando al **norte**, con **45° de inclinación** (prioriza el invierno).
2. Que **no haya sombra entre las 9 y las 16 h**, ni siquiera de un poste o una rama: la
   sombra en **un** panel baja la producción de **todo** el string.
3. Fijar firme (el viento en Guernica puede ser fuerte): dados de hormigón o anclajes.
4. Conectar la estructura a **tierra**.

### 2. Paneles (tapados o de noche: un panel al sol SIEMPRE tiene tensión)
1. Montar los paneles en la estructura.
2. Conectarlos **en serie**: el **+** de uno con el **−** del siguiente, usando sus propios
   cables MC4.
3. Queda libre un **+** en el primero y un **−** en el último.
4. **Medir la tensión** en esos dos extremos con el multímetro (rango DC 600 V):
   - Tiene que dar aprox. **50 V × cantidad de paneles** (≈200 V con 4, ≈250 V con 5).
   - Si da mucho menos → algún panel está mal conectado.
5. Llevar el cable solar por caño hasta el **seccionador DC** (abierto) y de ahí al
   inversor **PV+ / PV−**.
6. Instalar el **descargador de sobretensión** y conectarlo a tierra.
7. Verificar polaridad otra vez con el multímetro **antes** de cerrar el seccionador.
8. Cerrar el seccionador: en la pantalla del inversor tiene que aparecer la potencia
   solar.

---

## Orden para ENCENDER y APAGAR todo

| Encender | Apagar (orden inverso) |
|---|---|
| 1. Batería | 1. Paneles (seccionador DC) |
| 2. Seccionador de batería | 2. Red / grupo (térmica AC IN) |
| 3. Inversor | 3. Salida (térmica AC OUT) |
| 4. Red / grupo (AC IN) | 4. Inversor |
| 5. Paneles (seccionador DC) | 5. Seccionador de batería |
| 6. Salida a la casa (AC OUT) | 6. Batería |

**Regla de oro:** la batería es lo **primero en conectarse** y lo **último en
desconectarse**. Los paneles, al revés.

---

## Mantenimiento

| Cada | Qué hacer |
|---|---|
| **Primer mes** | Reajustar todos los tornillos de batería e inversor (se aflojan con el calor) |
| **Mensual** | Limpiar paneles con agua y trapo suave (sin detergentes fuertes) en épocas de polvo |
| **Mensual** | Mirar la app/pantalla: producción diaria y estado de carga de la batería |
| **Cada 3 meses** | Revisar que no haya cables calientes, terminales oscurecidos ni olor a quemado |
| **Cada 6 meses** | Arrancar el grupo electrógeno y hacerlo funcionar 20–30 min con carga |
| **Anual** | Revisar la estructura (óxido, tornillos) y la puesta a tierra |
