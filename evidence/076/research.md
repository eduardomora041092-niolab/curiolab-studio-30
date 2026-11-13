# 076 — ¿Cómo funciona un mando a distancia? — investigación

## Hechos que se afirman
- El mando lleva en la punta un LED que emite luz infrarroja, invisible para el ojo humano.
- Muchas cámaras de móvil captan esa luz infrarroja (se ve como un punto de luz al pulsar).
- Al pulsar un botón, un chip del mando enciende y apaga el LED muy rápido: los pulsos forman un código distinto para cada botón.
- En el aparato, un receptor (fotodiodo) detecta los pulsos de luz y los convierte en señal eléctrica.
- Un microcontrolador descodifica la señal y ejecuta la orden (volumen, canal…).

## Fuentes
- https://electronics.howstuffworks.com/remote-control.htm
- https://electronics.howstuffworks.com/remote-control1.htm
- https://electronics.howstuffworks.com/remote-control2.htm

## Lo que NO se afirma
- Frecuencias de portadora (p. ej. 38 kHz), longitudes de onda ni protocolos concretos (NEC, RC5).
- Que todas las cámaras de móvil vean el infrarrojo (algunas lo filtran): se dice "muchas".
