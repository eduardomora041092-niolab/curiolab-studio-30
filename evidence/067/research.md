# 067 — ¿Cómo lee un escáner el código de barras? — investigación

## Hechos que se afirman
- Un código de barras lineal guarda un número como un patrón de barras oscuras y espacios claros de distintos anchos.
- El escáner ilumina el código con un láser o una fuente de luz roja.
- Los espacios blancos reflejan mucha luz; las barras negras absorben la mayor parte y reflejan muy poca.
- Un sensor de luz (fotodiodo o sensor de imagen) recibe la luz reflejada y la convierte en una señal eléctrica que sube y baja.
- El decodificador mide el ancho de los pulsos y traduce el patrón en dígitos; el ordenador de la tienda busca ese número en su base de datos (producto y precio).

## Fuentes
- https://scanbot.io/?p=8559 (How does a laser barcode scanner work?)
- https://barcoding.com/blog/how-barcodes-are-read
- https://www.shopify.com/blog/how-do-barcode-scanners-work

## Lo que NO se afirma
- Estándares concretos (EAN-13, UPC), número de dígitos, longitud de onda del láser ni velocidad de lectura.
- El número mostrado en pantalla es ficticio (1234567890128), no corresponde a ningún producto real.
