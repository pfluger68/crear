# crear
La idea es crear cosas útiles

## Atalaya Terminal

Plataforma de gráficos en vivo para cripto (Binance), forex (Kraken) y oro, plata, petróleo WTI/Brent y USD/JPY (Hyperliquid). PAXG/USDT da historial de oro desde 2020.

- **Gráfico:** velas, Heikin Ashi, línea y área, de 1 minuto a 1 mes. Historial que se carga solo al desplazarte hacia atrás, e "Ir a fecha".
- **Indicadores:** EMA 20/50, Bollinger, pivotes diarios (P, R1/R2, S1/S2, máximo y mínimo del día anterior), volumen y RSI.
- **Dibujo:** tendencia, horizontal, zona de compra, zona de venta, Fibonacci y posición larga o corta con stop, objetivo, riesgo/beneficio y resultado. Se seleccionan, se mueven, se borran y quedan guardados por mercado en tu navegador.
- **Repetición:** eliges una vela del pasado, se oculta lo que vino después y avanzas vela por vela para practicar.
- **Zonas automáticas:** soportes y resistencias donde coinciden varios niveles de 1D, 4H y 1H (pivotes, máximo y mínimo de ayer, giros, EMA 50 de 4 h y nodos de volumen), para cualquier mercado.
- **Alertas:** por precio, por una línea, zona o posición dibujada, y al entrar en zonas automáticas o del Plan IA. Suenan, vibran y muestran una notificación mientras Atalaya esté abierta.
- **Análisis con Claude:** envía la imagen del gráfico, las velas de 1D, 4H y 1H, tus dibujos, las zonas y el plan. Claude responde con sesgo, zonas y operaciones, y un botón las dibuja. Con tu clave de API (se guarda solo en tu navegador y se cobra aparte, ~0,10 USD por análisis) analiza dentro de la página. Sin clave, copia el pedido para pegarlo en claude.ai.
- **Simulador:** cuenta ficticia de 10.000 USD, compras y ventas con stop loss y take profit, cálculo de cantidad según el riesgo, e historial con estadísticas. Funciona en vivo y en repetición.

Código: [`atalaya/index.html`](atalaya/index.html), un solo archivo, sin dependencias ni claves de API. Para verlo online: en GitHub, **Settings → Pages**, elige la rama y la carpeta `/ (root)`. Queda en `https://pfluger68.github.io/crear/atalaya/` (por ejemplo `.../atalaya/#XAUUSD`).

Solo informativo, no es asesoramiento financiero.
