# CurioLab Studio 30 — RUNBOOK de la ejecución diaria

Lo ejecuta una sesión programada de Claude en la nube, dos veces al día (06:37 y 12:37, America/New_York).
La segunda ejecución solo recupera lo que haya fallado en la primera. Todo es idempotente: repetir la
ejecución nunca debe crear publicaciones duplicadas.

## Alcance y prohibiciones
- Proyecto exclusivo: CurioLab Studio 30. Organización de Buffer `6ad737f3bb7377f2534a518d`.
  Canales: YouTube `6ad73b1a778b240e2f677dbf` y TikTok `6ad739bd778b240e2f677654`.
- PROHIBIDO: usar Metricool; tocar NIO LAB u otras marcas; editar o borrar publicaciones existentes;
  activar planes o funciones de pago; usar créditos de vidIQ para generar audio o vídeo; publicar fuera
  del calendario; publicar dos veces el mismo vídeo en un mismo canal.
- Ventana del experimento: del 2026-10-20 al 2026-11-18 (America/New_York).

## 0. Preparación
1. `git clone <REPO_URL> curiolab && cd curiolab` (la URL está en `pipeline/config.json` → `repo_url`).
   Para hacer push, adjunta el repositorio con la herramienta `add_repo` (access "push").
2. `./setup.sh` (instala kokoro-onnx y descarga los modelos de voz desde GitHub; todo gratuito).

## 1. Guarda de fechas
`python3 pipeline/daily.py guard`
- `ENDED`: desactiva la tarea programada "CurioLab — producción diaria" con `update_trigger`
  (enabled=false), registra `daily.py log INFO "experimento finalizado"`, exporta, haz push y termina con
  el mensaje "✅ CurioLab: experimento finalizado".
- `WAITING`: termina sin hacer nada.
- `ACTIVE`: continúa.

## 2. Lista de trabajo
`python3 pipeline/daily.py status` → vídeos con fecha ≤ hoy a los que les falta alguna plataforma.
Procésalos del más antiguo al más reciente, con un máximo de 6 por ejecución.

## 3. Por cada vídeo pendiente
### 3a. Guion y escenas (solo si `needs` contiene `spec`)
Crea `template/videos/vNNN.py` siguiendo el formato de `v002.py`–`v006.py`:
- Docstring con la **ficha científica**: el mecanismo o fenómeno explicado en 3–6 frases. Solo
  conocimiento consolidado de libro de texto. Sin cifras salvo que sean seguras; si dudas, generaliza.
- `LINES`: 8 frases en español, una escena por frase, la última "Sígueme para…". Narración total
  de 25–33 s (≈ 70–85 palabras). Gancho en la primera frase.
- `scene()`: dibujos originales y específicos del tema, con las primitivas de `engine.py`. Cada escena
  debe mostrar exactamente lo que dice su frase. Etiquetas que no tapen el mecanismo. Nada de logotipos,
  marcas, personajes conocidos ni personas reales.
- `KEYWORDS`: palabras clave en minúscula que se resaltan en los subtítulos.

### 3b. Previsualización y revisión visual
`python3 template/build.py template/videos/vNNN.py --preview` y **mira** `work/NNN/preview_sheet.png`
con la herramienta Read. Comprueba en cada fotograma:
- (a) la imagen corresponde a la frase del subtítulo;
- (b) la física o el mecanismo dibujado es correcto, sin flechas que contradigan la ficha;
- (c) ninguna etiqueta tapa el mecanismo ni invade la cabecera (y < 260) o la zona de subtítulos (y > 1190);
- (d) los textos se leen y no hay glifos vacíos (□).
Corrige y repite, como máximo 3 veces.

### 3c. Render y QA automático
`python3 pipeline/daily.py render NNN` (código de salida 0 = QA PASS). Si falla, corrige y reintenta una vez;
si vuelve a fallar, registra el error y pasa al siguiente vídeo. Después mira `work/NNN/final_sheet.png`
(un fotograma por frase, extraído del MP4 final) para confirmar la sincronía.

### 3d. Alojamiento público
`python3 pipeline/daily.py host NNN` → imprime la URL pública verificada (HTTP 200 y tamaño correcto).

### 3e. Publicación (sin duplicados)
1. Comprueba si ya existe: `execute_query` en Buffer:
   `posts(first:100, input:{organizationId:"6ad737f3bb7377f2534a518d", filter:{channelIds:[<canal>]}})`
   pidiendo `id status externalLink assets{... on VideoAsset{video{title}}}`. Si hay un post cuyo
   `video.title` sea `CurioLab_NNN.mp4` y su estado no sea `error`, **no publiques**: regístralo con
   `daily.py record` y continúa.
2. `python3 pipeline/daily.py caption NNN` → texto, título, modo y `dueAt`.
3. `create_post` por canal con `schedulingType: automatic`, `mode` y `dueAt` del paso anterior, y
   `assets: [{video:{url:<media_url>, metadata:{title:"CurioLab_NNN.mp4"}}}]`.
   - YouTube: `metadata.youtube = {title, categoryId:"27", privacy:"public", madeForKids:false, isAiGenerated:true}`.
   - TikTok: `metadata.tiktok = {isAiGenerated:true}`.
4. `python3 pipeline/daily.py record NNN <youtube|tiktok> <post_id> <status> [externalLink]`.

## 4. Conciliación
Para cada post registrado como `scheduled` o `sending`, consulta su estado actual y su `externalLink`
(`get_post` o `execute_query`) y vuelve a registrarlo. Un vídeo pasa a PUBLISHED cuando ambos canales
están en `sent`. Si un post está en `error`, registra el mensaje y vuelve a crearlo una sola vez.

## 5. Métricas
Para los posts `sent` hace más de 24 h, llama a `get_post` con `includeMetrics: true`, guarda la lista
`[{video_id, platform, post_id, metrics:[{type,value}]}]` en `/tmp/m.json` y ejecuta
`python3 pipeline/daily.py metrics /tmp/m.json`. Como mucho una captura por post y día.

## 6. Cierre
1. `python3 pipeline/daily.py export`.
2. `git add -A && git commit -m "run <fecha> <hora>" && git push`.
3. Copia de seguridad en Google Drive, carpeta `1TBANuVlSLiGgyTtx3yWWSwSuGtfKIVGV`: crea
   `CurioLab_run_<fecha>_<hora>.txt` con el resumen (vídeos procesados, IDs de publicación, enlaces,
   errores).
4. Mensaje final:
   - Si todo fue bien: `✅ CurioLab <fecha>: NNN, NNN, NNN publicados/programados (YT y TT)`.
   - Si algo falló: `❌ CurioLab ERROR <fecha>: <qué falló>`, y además crea en Drive
     `CurioLab_ERROR_<fecha>.txt` con el detalle. El aviso llega al teléfono y al correo del dueño.

## Lo que este proceso NO puede comprobar automáticamente
- Cómo suena la voz: pronunciación, entonación y naturalidad. Solo se mide la sonoridad (LUFS) y la duración.
- La exactitud científica más allá del conocimiento del propio modelo: no hay revisión externa.
- El juicio estético final y cómo reacciona la audiencia.
- Si las plataformas limitan el alcance o etiquetan el contenido.
