# CurioLab — registro de decisiones editoriales (generado por `daily.py editorial`)

## 2026-10-22T16:26:59-04:00 — aplica desde el vídeo 013
- **target_max_s**: None → 28.0
- **hook_max_words**: None → 9
- **caption_cta**: None → True
- Motivos:
  - R1: retención mediana TikTok 36% en 5 vídeos (umbral 40 %/50 %) → duración máx 28 s, gancho ≤ 9 palabras
  - R2: 0 comentarios en 10 publicaciones medidas → pregunta en el texto: sí
  - R3: menos de 3 vídeos medidos en alguna categoría: sin cambio (Mecanismo=4, Ciencia=1)
- Datos: 001 ret 0.429 vis 12.38 s com 0; 002 ret 0.371 vis 11.97 s com 0; 003 ret 0.262 vis 8.26 s com 0; 004 ret 0.365 vis 11.41 s com 0; 005 ret 0.359 vis 10.66 s com 0

## 2026-10-24T06:40:26-04:00 — aplica desde el vídeo 016
- **weak_category**: None → Ciencia
- Motivos:
  - R1: retención mediana TikTok 36% en 9 vídeos (umbral 40 %/50 %) → duración máx 28 s, gancho ≤ 9 palabras
  - R2: 0 comentarios en 18 publicaciones medidas → pregunta en el texto: sí
  - R3: visionado medio TikTok Mecanismo 10.9 s, Ciencia 8.3 s → categoría débil: Ciencia
- Datos: 001 ret 0.426 vis 12.28 s com 0; 002 ret 0.369 vis 11.88 s com 0; 003 ret 0.264 vis 8.33 s com 0; 004 ret 0.352 vis 11.02 s com 0; 005 ret 0.36 vis 10.69 s com 0; 006 ret 0.36 vis 10.35 s com 0; 007 ret 0.244 vis 7.23 s com 0; 008 ret 0.383 vis 10.27 s com 0; 009 ret 0.206 vis 5.62 s com 0

## 2026-10-24T07:30:00-04:00 — Revisión del dueño (checkpoint) y experimento único desde el vídeo 019
- **Estado**: 001–012 publicados en YouTube y TikTok (24 posts `sent`, 1 por canal). Programados: 013–015 (24-oct),
  016 YT+TT y 017 YT (25-oct). En espera por cola llena de Buffer (10 − 1 de margen): 017 TT, 018 YT, 018 TT. Se
  programan solos en las ejecuciones de las 13:37 y 18:37, a su hora de calendario.
- **Incidencia**: la ejecución del 23-oct 18:37 no hizo nada porque el control de seguridad denegó `setup.sh` y
  `daily.py` ("Code from External"). La ejecución del 24-oct 06:37 sí funcionó. Riesgo intermitente sin resolver.
- **Reglas 013+ verificadas**: 013–018 ≤ 28 s, gancho ≤ 9 palabras, pregunta en el texto; R3 (Ciencia) desde 016.
  Ningún gancho de 013–018 es una pregunta.
- **Experimento `gancho_en_accion` (019–027)**: escena 1 con el objeto o fenómeno ya en acción desde 0 s y primera
  frase = una sola pregunta clara (≤ 9 palabras). R1–R3 congeladas 019–027 para aislar el cambio. Base: 013–018.
  QA automático: la primera frase debe empezar por ¿ y terminar en ?; la escena 1 se revisa visualmente.
- **Comparación prevista**: `daily.py compare 24h` (cuando 019–027 tengan captura 21–45 h, ~29-oct) y `compare 72h`
  (~31-oct). Mediana del visionado medio y de la retención en TikTok, y de las vistas en YouTube, frente a 013–018.
  Con 6–9 vídeos por grupo la diferencia puede deberse al azar, al tema, al día o a la franja: se informará como
  observación, no como causa.
- **Métricas**: capturas en franjas ~24 h y ~72 h (`metrics-due`) con `sentAt` real en `logs/sent_at.json`.
- **Portadas TikTok**: desde 017 TT, `thumbnailOffset` = fotograma donde ya se lee la pregunta completa del gancho.
  Sin verificar hasta que salga 017 TT (25-oct 13:00). No se modifican posts ya programados ni publicados.

## 2026-10-27T13:40:21-04:00 — aplica desde el vídeo 028
- **weak_category**: Ciencia → None
- Motivos:
  - R1: proporción media vista (visionado medio / duración) mediana TikTok 29% en 20 vídeos (umbral 40 %/50 %) → duración máx 28 s, gancho ≤ 9 palabras
  - R2: 0 comentarios en 40 publicaciones medidas → pregunta en el texto: sí
  - R3: visionado medio TikTok Mecanismo 8.3 s, Ciencia 8.6 s → categoría débil: ninguna
- Datos: 001 ret 0.417 vis 12.02 s com 0; 002 ret 0.366 vis 11.81 s com 0; 003 ret 0.263 vis 8.28 s com 0; 004 ret 0.35 vis 10.93 s com 0; 005 ret 0.348 vis 10.34 s com 0; 006 ret 0.313 vis 9.01 s com 0; 007 ret 0.237 vis 7.04 s com 0; 008 ret 0.356 vis 9.55 s com 0; 009 ret 0.199 vis 5.43 s com 0; 010 ret 0.271 vis 7.94 s com 0; 011 ret 0.24 vis 7.2 s com 0; 012 ret 0.337 vis 9.5 s com 0; 013 ret 0.248 vis 6.87 s com 0; 014 ret 0.35 vis 9.35 s com 0; 015 ret 0.223 vis 5.94 s com 0; 016 ret 0.273 vis 7.44 s com 0; 017 ret 0.237 vis 6.57 s com 0; 018 ret 0.347 vis 9.23 s com 0; 019 ret 0.27 vis 7.18 s com 0; 020 ret 0.333 vis 8.7 s com 0

## 2026-10-29T07:11:59-04:00 — aplica desde el vídeo 034
- **caption_cta**: True → False
- Motivos:
  - R1: proporción media vista (visionado medio / duración) mediana TikTok 32% en 25 vídeos (umbral 40 %/50 %) → duración máx 28 s, gancho ≤ 9 palabras
  - R2: 1 comentarios en 50 publicaciones medidas → pregunta en el texto: no
  - R3: visionado medio TikTok Mecanismo 8.6 s, Ciencia 8.6 s → categoría débil: ninguna
- Datos: 001 ret 0.417 vis 12.02 s com 0; 002 ret 0.366 vis 11.81 s com 0; 003 ret 0.263 vis 8.28 s com 0; 004 ret 0.35 vis 10.93 s com 0; 005 ret 0.348 vis 10.34 s com 0; 006 ret 0.313 vis 9.01 s com 0; 007 ret 0.237 vis 7.04 s com 0; 008 ret 0.356 vis 9.55 s com 0; 009 ret 0.199 vis 5.43 s com 0; 010 ret 0.271 vis 7.94 s com 0; 011 ret 0.24 vis 7.19 s com 0; 012 ret 0.337 vis 9.5 s com 0; 013 ret 0.255 vis 7.05 s com 0; 014 ret 0.332 vis 8.87 s com 0; 015 ret 0.223 vis 5.92 s com 0; 016 ret 0.274 vis 7.47 s com 0; 017 ret 0.236 vis 6.56 s com 0; 018 ret 0.344 vis 9.15 s com 0; 019 ret 0.265 vis 7.05 s com 0; 020 ret 0.327 vis 8.55 s com 0; 021 ret 0.305 vis 8.0 s com 0; 022 ret 0.325 vis 8.36 s com 0; 023 ret 0.428 vis 10.89 s com 0; 024 ret 0.394 vis 10.08 s com 0; 025 ret 0.452 vis 12.23 s com 1
