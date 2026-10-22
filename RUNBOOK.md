# CurioLab Studio 30 — RUNBOOK de la ejecución diaria

Lo ejecuta una sesión programada de Claude en la nube tres veces al día (06:37, 13:37 y 18:37, America/New_York),
siempre después de una hora de publicación (09:00, 13:00, 18:00) para verificarla. Todas las ejecuciones siguen el
mismo RUNBOOK; producen solo lo que falte y programan solo lo que quepa en la cola. Todo es idempotente: repetir la
ejecución nunca debe crear publicaciones duplicadas.

## Alcance y prohibiciones
- Proyecto exclusivo: CurioLab Studio 30. Organización de Buffer `6ad737f3bb7377f2534a518d`.
  Canales: YouTube `6ad73b1a778b240e2f677dbf` y TikTok `6ad739bd778b240e2f677654`.
- PROHIBIDO: usar Metricool; tocar NIO LAB u otras marcas; editar o borrar publicaciones existentes;
  activar planes o funciones de pago; usar créditos de vidIQ para generar audio o vídeo; publicar fuera
  del calendario; publicar dos veces el mismo vídeo en un mismo canal.
- Ventana del experimento: del 2026-10-20 al 2026-11-18 (America/New_York).

## 0. Preparación
1. `git clone --depth 1 --single-branch -b main https://github.com/eduardomora041092-niolab/curiolab-studio-30 curiolab && cd curiolab`.
   Si existe la herramienta `add_repo`, úsala antes con owner `eduardomora041092-niolab`, repo `curiolab-studio-30`
   y access "push". Comprueba la escritura con `git push --dry-run origin main`. Si falla, anota el error exacto:
   sin push no se pueden alojar vídeos nuevos (paso 5e), pero sí publicar los que ya tengan `media_url`.
2. `./setup.sh`: instala SOLO las dependencias de `requirements.txt` (PyPI, versiones fijadas) y los modelos
   Kokoro v1.0 del release oficial, comprobando su SHA-256. Está autorizado por el dueño; ver `DEPENDENCIAS.md`.
   Si el control de seguridad lo deniega o falla, NO lo intentes de otra forma: registra el motivo exacto con
   `daily.py log ERROR`, sáltate la producción (5a–5e), sigue con la publicación de lo ya alojado y termina con ❌.

## 0b. Bloqueo de ejecución
`python3 pipeline/daily.py lock acquire`. Si devuelve `BUSY`, hay otra ejecución en curso: termina sin
hacer nada, con el mensaje "⏸ CurioLab: otra ejecución en curso". Al final de TODA ejecución, también si falla,
ejecuta `python3 pipeline/daily.py lock release`.

## 1. Guarda de fechas
`python3 pipeline/daily.py guard`
- `ENDED`: haz antes los pasos 2 y 3 (conciliación y métricas finales), desactiva la tarea programada
  "CurioLab — producción diaria" con `update_trigger` (enabled=false), registra `daily.py log INFO "experimento finalizado"`, exporta, haz push y termina con
  el mensaje "✅ CurioLab: experimento finalizado".
- `WAITING`: termina sin hacer nada.
- `ACTIVE`: continúa.

## 2. Instantánea de Buffer y conciliación (verifica lo publicado)
1. `python3 pipeline/daily.py snapshot-query` → imprime `query` y `variables`. Llama a `execute_query` de Buffer con
   ellos tal cual (solo lectura) y guarda la respuesta completa, sin editar, en `/tmp/snap.json` con la herramienta Write.
2. `python3 pipeline/daily.py queue /tmp/snap.json` → concilia `state.json` con Buffer (estado real, `externalLink`
   público, PUBLISHED cuando ambos canales están en `sent`), calcula la capacidad y escribe `pipeline/queue_plan.json`.
   Registra solo; no crees nada todavía. Avisos que imprime:
   - `RETRASO`: un post sigue `scheduled` 45 min después de su hora → repórtalo en el mensaje final (no lo edites).
   - `SIN ENLACE`: `sent` sin enlace público → se reintenta en la siguiente ejecución.
   - `DUPLICADO`: dos posts vivos del mismo vídeo y canal → ❌ en el mensaje final; no borres nada.
   - `blocked`: un post falló dos veces → ❌; no se vuelve a crear.

## 3. Métricas y ajuste editorial (antes de producir)
1. Para los posts `sent` hace más de 24 h y sin captura hoy en `logs/metrics.csv`, llama a `get_post` con
   `includeMetrics: true`, guarda `[{video_id, platform, post_id, metrics:[{type,value}]}]` en `/tmp/m.json` y ejecuta
   `python3 pipeline/daily.py metrics /tmp/m.json`. Como mucho una captura por post y día.
2. `python3 pipeline/daily.py editorial` → recalcula `pipeline/editorial.json` con reglas deterministas (R1 retención →
   duración máxima y longitud del gancho; R2 sin comentarios → pregunta en el texto; R3 categoría con menos visionado →
   gancho más concreto) y, si algo cambia, lo anota con datos y motivo en `logs/editorial_log.md`. Las reglas se
   aplican desde el siguiente vídeo sin guion (`applies_from`), nunca retroactivamente. Tras 6 vídeos con la regla R1
   se compara la retención antes/después y, si no mejora al menos 3 puntos, se revierte sola.

## 4. Lista de trabajo
`python3 pipeline/daily.py status` → vídeos con fecha ≤ MAÑANA a los que les falta alguna plataforma, más
`editorial_rules` y `editorial_reasons`, que son obligatorias para los guiones nuevos.
Si el mensaje de la ejecución pide adelantar la producción, usa `status --through AAAA-MM-DD`. Los vídeos
futuros se programan para su hora con `customScheduled`; nunca se publican antes.
Procésalos del más antiguo al más reciente. `status` limita a 3 los vídeos NUEVOS (sin guion) por ejecución:
se produce como mucho un día de calendario por ejecución, y cada ID se publica una sola vez por canal.

## 5. Por cada vídeo pendiente
### 5a. Investigación (solo si `needs` contiene `spec`)
Verifica el mecanismo o fenómeno con 1–2 búsquedas web y guarda `evidence/NNN/research.md` con: los hechos
que vas a afirmar, las fuentes (URL) y lo que decidiste NO afirmar por dudoso. No uses créditos de vidIQ.

### 5b. Guion y escenas
Crea `template/videos/vNNN.py` siguiendo el formato de `v002.py`–`v012.py`:
- Docstring con la **ficha científica**: el mecanismo o fenómeno explicado en 3–6 frases. Solo
  conocimiento consolidado de libro de texto. Sin cifras salvo que sean seguras; si dudas, generaliza.
- `LINES`: 8 frases en español, una escena por frase, la última "Sígueme para…". Gancho en la primera frase.
  Respeta `editorial_rules`: vídeo final ≤ `target_max_s` (y ≥ 25 s del QA) y primera frase ≤ `hook_max_words`
  palabras. Referencia: ≈ 2,9 palabras por segundo de vídeo (28 s ≈ 70–74 palabras). Si `weak_category` es la
  categoría del vídeo, la primera frase y la primera escena muestran un objeto o situación cotidiana concreta.
- `scene()`: dibujos originales y específicos del tema, con las primitivas de `engine.py`. Cada escena
  debe mostrar exactamente lo que dice su frase. Etiquetas que no tapen el mecanismo. Nada de logotipos,
  marcas, personajes conocidos ni personas reales. Poppins no tiene "→" ni "✓": no los uses.
- `KEYWORDS`: palabras clave en minúscula que se resaltan en los subtítulos.

### 5c. Previsualización y revisión visual
`python3 template/build.py template/videos/vNNN.py --preview` y **mira** `work/NNN/preview_sheet.png`
con la herramienta Read. Comprueba en cada fotograma:
- (a) la imagen corresponde a la frase del subtítulo;
- (b) la física o el mecanismo dibujado es correcto, sin flechas que contradigan la ficha;
- (c) ninguna etiqueta tapa el mecanismo ni invade la cabecera (y < 260) o la zona de subtítulos (y > 1190);
- (d) los textos se leen y no hay glifos vacíos (□).
Corrige y repite, como máximo 3 veces.

### 5d. Render y QA automático
`python3 pipeline/daily.py render NNN` (código de salida 0 = QA PASS, que ahora incluye `EDITORIAL PASS` cuando
las reglas aplican). Un render tarda 5–7 min: lánzalos en segundo plano (`nohup … &`) con registro en el
directorio temporal y espera a que terminen; si se ejecutan en paralelo, no ejecutes otros comandos que escriban
`state.json` hasta que acaben. Si falla (QA o EDITORIAL), corrige (p. ej. acorta frases) y reintenta una vez; si
vuelve a fallar, registra el error y pasa al siguiente vídeo. Después mira `work/NNN/final_sheet.png`.

Al terminar el QA, `evidence/NNN/` debe contener qa.json, segs.json, preview_sheet.png, final_sheet.png y
research.md. Escribe en `evidence/NNN/visual_review.md` qué comprobaste en cada fotograma, qué corregiste y qué
reglas editoriales aplicaste.

### 5e. Alojamiento público
`python3 pipeline/daily.py host NNN` → imprime la URL pública verificada (HTTP 200 y tamaño correcto).

## 6. Programación según la capacidad real de Buffer (sin duplicados)
1. Repite el paso 2 (nueva instantánea → `queue`). El plan solo incluye en `create` lo que cabe:
   límite de la organización (`limits.scheduledPosts`, hoy 10) − 1 de margen − posts `scheduled`/`sending`, en orden
   de hora de calendario (YouTube y luego TikTok). Lo demás queda en `waiting` con su motivo: no es un error, el
   vídeo queda producido y alojado y la siguiente ejecución lo programa. Un post en `error` se recrea una sola vez.
2. Por cada elemento de `create`: `create_post` con `channelId`, `schedulingType: automatic`, `mode`, `dueAt` (si no
   es null), `text`, `assets: [{video:{url: asset.url, metadata:{title: asset.title}}}]` y `metadata` tal cual vienen
   en el plan. No cambies el modo ni la hora para esquivar un control de seguridad.
   Si Buffer responde `LimitReachedError`, para: no crees más y continúa (los restantes quedan en espera).
3. `python3 pipeline/daily.py record NNN <youtube|tiktok> <post_id> <status>` por cada post creado.
4. Confirmación: nueva instantánea → `queue`. Debe salir `create: []` (o solo lo que siga sin capacidad); si
   aparece un `DUPLICADO`, ❌.

## 7. Ciclo y cierre
1. `python3 pipeline/daily.py cycle` → PASS/PENDING de cada etapa (vídeo A: producido, alojado, programado,
   publicado con enlace, métricas, usado por la regla editorial; vídeo B: producido con reglas que ya incluyen las
   métricas de A, EDITORIAL PASS, programado). Copia el veredicto al resumen.
2. `python3 pipeline/daily.py export`.
3. `git add -A && git commit -m "run <fecha> <hora>" && git push origin main`. Si el push falla, sube
   `pipeline/state.json` a Drive como `CurioLab_state_<fecha>_<hora>.json` y trata la ejecución como ❌.
4. Copia de seguridad en Google Drive, carpeta `1TBANuVlSLiGgyTtx3yWWSwSuGtfKIVGV`: crea
   `CurioLab_run_<AAAA-MM-DD>_<HHMM>.txt` con el resumen (vídeos procesados, IDs de publicación, enlaces, capacidad de la
   cola, en espera, cambios editoriales, veredicto del ciclo, errores) y confírmalo con `get_file_metadata` (que exista,
   esté en esa carpeta y su propietario sea eduardomora0317@gmail.com). Si no se confirma, ❌.
5. `python3 pipeline/daily.py lock release`.
6. Mensaje final:
   - Si todo fue bien: `✅ CurioLab <fecha> <hora>: NNN, NNN programados (YT y TT); NNN publicados; en espera: …; ciclo: PASS|PENDING`.
   - Si una acción la bloquea el control de seguridad de la sesión, no intentes rodearlo: regístrala y repórtala.
   - Si algo falló: `❌ CurioLab ERROR <fecha>: <qué falló>`, y además crea en Drive
     `CurioLab_ERROR_<fecha>.txt` con el detalle. El aviso llega al teléfono y al correo del dueño.

## Lo que este proceso NO puede comprobar automáticamente
- Cómo suena la voz: pronunciación, entonación y naturalidad. Solo se mide la sonoridad (LUFS) y la duración.
- La exactitud científica más allá del conocimiento del propio modelo: no hay revisión externa.
- El juicio estético final y cómo reacciona la audiencia.
- Si las reglas editoriales causan la mejora: con 3 vídeos al día y pocas visualizaciones, las diferencias pueden
  deberse al azar o al tema. `editorial_log.md` registra cada decisión con sus datos para revisarla.
- Si las plataformas limitan el alcance o etiquetan el contenido.
