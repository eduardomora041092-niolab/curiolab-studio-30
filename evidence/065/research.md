# 065 — ¿Cómo sabe el GPS dónde estás? — investigación

## Hechos que se afirman
- Los satélites GPS llevan relojes muy precisos y emiten continuamente señales de radio con la hora de envío (y su posición).
- El receptor GPS del móvil solo recibe: no envía nada a los satélites.
- El receptor mide cuánto tardó cada señal en llegar y, como viaja a la velocidad de la luz, lo convierte en distancia.
- Cada distancia sitúa al receptor en una esfera centrada en ese satélite; con varios satélites, las esferas se cruzan en un punto: la posición (trilateración).
- Como el reloj del móvil no es tan preciso, hace falta un cuarto satélite para resolver también el error del reloj.

## Fuentes
- https://gisgeography.com/trilateration-triangulation-gps/
- https://www.gim-international.com/content/article/gps-position-time-and-distance
- https://oemgnss.trimble.com/blog/oemgnss/en-US/article/starting-with-gps-basics

## Lo que NO se afirma
- Número de satélites de la constelación, altitudes, órbitas, precisión en metros ni velocidades.
- Correcciones relativistas o asistencia por redes móviles (A-GPS).
- La hora "12:00:00.000" de la escena 2 es solo ilustrativa.
