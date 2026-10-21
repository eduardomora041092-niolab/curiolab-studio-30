# Plantilla CurioLab Studio 30

Motor reutilizable extraído del flujo aprobado del Video 001.

## Producir un vídeo nuevo
1. Copia `videos/v003.py` como `videos/vNNN.py`.
2. Rellena `ID`, `TITLE`, `SUBTITLE`, `LINES` (una frase = una escena) y `KEYWORDS`.
3. Escribe `scene(i, u, L, E, im, d)` con las primitivas de `engine.py`
   (`rrect`, `circle`, `poly`, `line`, `arrow`, `wave`, `label`, `pill`, `cross`, `outro`).
4. Opcional: `sfx(segs)` con efectos ("zip", "click", "whoosh", "pop").
5. `python3 build.py videos/vNNN.py --preview`: narración y hoja de previsualización.
6. `python3 build.py videos/vNNN.py`: MP4 final en `../out/` y `../work/NNN/qa.json`.

## Lo que hace el motor
- Formato 1080×1920, 30 fps, H.264 + AAC, sonoridad normalizada.
- Narración local con Kokoro (voz `em_alex`, español).
- Subtítulos sincronizados en la zona segura.
- Cabecera de marca, acercamiento suave por escena y fundidos de 0,25 s.
- QA automático, más una hoja con un fotograma por frase extraído del MP4 final.

`v001_render_archived.py` es el script original del Video 001, conservado sin cambios como referencia.
