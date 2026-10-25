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
2. `./setup.sh`: instala SOLO las dependencias de `requirements.txt` (PyPI, versión y hash SHA-256 fijados, `--require-hashes`) y los modelos
   Kokoro v1.0 del release oficial, comprobando su SHA-256. Está autorizado por el dueño; ver `DEPENDENCIAS.md`.
   Si el control de seguridad lo deniega o falla, NO lo intentes de otra forma: registra el motivo exacto con
   `daily.py log ERROR`, sáltate la producción (5a–5e), sigue con la publicación de lo ya alojado y termina con ❌.

## 0b. Bloqueo de ejecución
`python3 pipeline/daily.py lock acquire`. Si devuelve `BUSY`, hay otra ejecución en curso: termina sin
hacer nada, con el mensaje "⏸ CurioLab: otra ejecución en curso" (no liberes nada: el candado no es tuyo).
Cómo funciona: el candado es `pipeline/lock.json` en `main` (commit + push). `acquire` guarda un token aleatorio en el
candado y una copia en `.git/curiolab_lock_token` de este clon (nunca se sube). `lock check` responde `OWNER`,
`NOT_OWNER` o `NONE` comparando con el candado remoto; `lock release` solo borra el candado si el token es el de
esta ejecución, y exige que todo lo demás ya esté commiteado y subido. Un candado de más de 2 h se considera
caducado y la siguiente ejecución lo retoma (queda un WARN en `run_log.csv`). La liberación se hace al FINAL del
paso 7 (después del push y de comprobar la copia en Drive), también si la ejecución falla; ver 7.

## 1. Guarda de fechas
`python3 pipeline/daily.py guard`
- `ENDED`: haz antes los pasos 2 y 3 (conciliación y métricas finales), desactiva la tarea programada
  "CurioLab — producción diaria" con `update_trigger` (enabled=false), registra `daily.py log INFO "experimento finalizado"`, exporta, haz push, ejecuta `lock release` y termina con
  el mensaje "✅ CurioLab: experimento finalizado".
- `WAITING`: no hagas nada más que `lock release` y termina.
- `ACTIVE`: continúa.

## 2. Instantánea de Buffer y conciliación (verifica lo publicado)
1. `python3 pipeline/daily.py snapshot-query reconcile` → imprime `query`, `variables` y un `nonce` de un solo uso
   (la consulta lleva el alias `req_<nonce>`, que Buffer devuelve en la respuesta). Llama a `execute_query` de Buffer
   con `query` y `variables` tal cual (solo lectura) y guarda la salida COMPLETA de la herramienta, sin editar ni
   recortar (incluido el objeto `rateLimit` final), en `/tmp/snap.json` con la herramienta Write. Nunca reconstruyas,
   combines ni completes a mano una respuesta, ni reutilices un archivo de una consulta anterior.
2. `python3 pipeline/daily.py queue /tmp/snap.json` → valida la instantánea (claves y organización), la archiva byte a
   byte en `evidence/buffer/` (con SHA-256 en `evidence/buffer/index.csv`), concilia `state.json` con Buffer (estado
   real, `externalLink` público, PUBLISHED cuando ambos canales están en `sent`), calcula la capacidad y escribe
   `pipeline/queue_plan.json`. Este plan es solo informativo (`for_create: false`): `create-next` lo rechaza.
   Registra solo; no crees nada todavía. Avisos que imprime:
   - `RETRASO`: un post sigue `scheduled` 45 min después de su hora → repórtalo en el mensaje final (no lo edites).
   - `SIN ENLACE`: `sent` sin enlace público → se reintenta en la siguiente ejecución.
   - `DUPLICADO`: dos posts vivos del mismo vídeo y canal → ❌ en el mensaje final; no borres nada.
   - `blocked`: un post falló dos veces → ❌; no se vuelve a crear.

## 3. Métricas y ajuste editorial (antes de producir)
1. `python3 pipeline/daily.py metrics-due /tmp/snap.json` → lista de posts a capturar ahora: la primera captura dentro
   de la franja ~24 h (21–45 h desde `sentAt`), la primera dentro de ~72 h (69–93 h) y, si no, una al día a partir de
   21 h. Cada elemento trae `video_id` como texto de 3 cifras (p. ej. "008"). Para cada uno llama a `get_post` con
   `includeMetrics: true`, guarda `[{video_id, platform, post_id, metrics:[{type,value}]}]` (copiando `video_id`,
   `platform` y `post_id` tal cual de metrics-due) en `/tmp/m.json` y ejecuta `python3 pipeline/daily.py metrics /tmp/m.json`.
   `metrics` valida todas las filas antes de escribir: si alguna tiene un `video_id`, plataforma o `post_id` no válidos,
   no escribe nada y sale con código 2 (corrige el archivo; no edites `metrics.csv` a mano).
   Comparación a igual antigüedad: `python3 pipeline/daily.py compare 24h` y `compare 72h`.
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
- **Experimento `gancho_en_accion` (desde 019, ver `editorial.json` → `experiment`)**: la primera frase es UNA
  pregunta clara (empieza por ¿, termina en ?, ≤ `hook_max_words` palabras) y la escena 1 muestra el objeto o
  fenómeno YA en acción desde el fotograma 0 (moviéndose, funcionando u ocurriendo), sin pantalla de título ni
  objeto quieto que tarde en arrancar. Las demás reglas no cambian. Base de comparación: 016–018 (mismas reglas);
  013–015 (sin R3) se informa aparte. En `visual_review.md` escribe la línea
  `Escena 1 en acción desde 0 s: sí` (o `no` y por qué) tras mirar el primer fotograma de `preview_sheet.png`
  y un fotograma a 0,0 s del MP4 final.
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
1. Instantánea NUEVA justo antes de crear (obligatoria aunque la del paso 2 sea de hace un momento):
   `snapshot-query pre-create` → `execute_query` → Write de la salida completa en `/tmp/snap_pre.json` →
   `python3 pipeline/daily.py queue /tmp/snap_pre.json --for-create`. Se rechaza (`REFUSED`, código 5) si la respuesta
   no contiene el `req_<nonce>` de una consulta emitida hace ≤ 10 min, si esa instantánea ya se usó antes o si está
   incompleta: en ese caso repite este punto con una consulta nueva (no edites el archivo). El plan concilia por vídeo
   y canal con lo que hay realmente en Buffer: un (vídeo, canal) que ya tiene un post vivo no entra en `create`,
   aunque `state.json` no lo tenga registrado (p. ej. una ejecución anterior se cortó entre `create_post` y `record`).
   `create` solo incluye lo que cabe: límite de la organización (`limits.scheduledPosts`, hoy 10) − 1 de margen −
   posts `scheduled`/`sending`, en orden de hora de calendario (YouTube y luego TikTok). Lo demás queda en `waiting`
   con su motivo: no es un error, el vídeo queda producido y alojado y la siguiente ejecución lo programa. Un post en
   `error` se recrea una sola vez. El plan autoriza crear durante 10 min (`valid_until`).
2. Bucle, un post cada vez: `python3 pipeline/daily.py create-next`.
   - Si imprime un elemento (JSON): `create_post` con `channelId`, `schedulingType: automatic`, `mode`, `dueAt` (si
     no es null), `text`, `assets: [{video:{url: asset.url, metadata:{title: asset.title}}}]` y `metadata` tal cual
     vienen. Si `asset.thumbnailOffset` existe (solo TikTok), añádelo en `metadata.thumbnailOffset` del vídeo: es el
     fotograma de portada donde ya se lee la pregunta completa del gancho. No cambies el modo ni la hora para esquivar
     un control de seguridad. Inmediatamente después, `python3 pipeline/daily.py record NNN <youtube|tiktok> <post_id> <status>`.
     Si `create_post` falla (p. ej. `LimitReachedError`), `record NNN <plataforma> - failed "<mensaje>"`: el plan se
     detiene y no se crea nada más en esta ejecución (los restantes quedan en espera).
   - `NONE` o `STOP` (código 3): no hay más que crear; sigue al punto 3.
   - `PENDING_RECORD` (código 6): falta el `record` del elemento anterior; regístralo (no lo vuelvas a crear).
   - `STALE`/`REFUSED` (código 5): el plan caducó o no autoriza crear; vuelve al punto 1 con una consulta nueva.
     Si no sabes si un `create_post` llegó a hacerse, NO lo repitas: la nueva instantánea lo mostrará y lo conciliará.
3. Confirmación: `snapshot-query confirm` → `execute_query` → Write → `queue /tmp/snap_conf.json` (sin `--for-create`).
   Debe salir `create: []` (o solo lo que siga sin capacidad); si aparece un `DUPLICADO`, ❌.
   Todas las instantáneas quedan archivadas tal cual en `evidence/buffer/` y se suben con el commit del paso 7.

## 7. Ciclo y cierre
1. `python3 pipeline/daily.py cycle` → PASS/PENDING de cada etapa (vídeo A: producido, alojado, programado,
   publicado con enlace, métricas, usado por la regla editorial; vídeo B: producido con reglas que ya incluyen las
   métricas de A, EDITORIAL PASS, programado). Copia el veredicto al resumen.
2. `python3 pipeline/daily.py export`.
3. `python3 pipeline/daily.py lock check` → debe ser `OWNER`. Si es `NOT_OWNER`/`NONE` (otra ejecución retomó el
   candado caducado), NO hagas push: sube `pipeline/state.json` a Drive como `CurioLab_state_<fecha>_<hora>.json`,
   no ejecutes `lock release` y termina con ❌ explicando el solapamiento.
4. `git add -A && git commit -m "run <fecha> <hora>" && git push origin main` (el candado sigue puesto: aún no se libera).
   Si el push falla, sube `pipeline/state.json` a Drive como `CurioLab_state_<fecha>_<hora>.json` y trata la ejecución como ❌.
5. Copia de seguridad en Google Drive, carpeta `1TBANuVlSLiGgyTtx3yWWSwSuGtfKIVGV`: crea
   `CurioLab_run_<AAAA-MM-DD>_<HHMM>.txt` con el resumen (vídeos procesados, IDs de publicación, enlaces, capacidad de la
   cola, en espera, cambios editoriales, veredicto del ciclo, errores) y confírmalo con `get_file_metadata` (que exista,
   esté en esa carpeta y su propietario sea eduardomora0317@gmail.com). Si no se confirma, ❌ (y crea el
   `CurioLab_ERROR_<fecha>.txt` si Drive lo permite), pero continúa con el punto 6: el candado se libera igualmente.
6. `python3 pipeline/daily.py lock release` (siempre al final, también tras un ❌). Respuestas:
   - `OK`: liberado. `OK (sin candado)`: no había candado.
   - `NOT_OWNER` (código 7): el candado es de otra ejecución; no se toca. Repórtalo.
   - `ERROR` (código 8): quedan cambios sin commit (haz el commit/push del punto 4 y reintenta una vez) o falló el
     push. Si no se puede liberar, repórtalo con ❌: el candado caduca solo a las 2 h y la siguiente ejecución lo retoma.
   Si la sesión se interrumpe en cualquier punto, el candado queda en `main` como máximo 2 h; nadie más puede
   liberarlo antes (no tiene el token), y una ejecución tardía que vuelva después ya no podrá liberar el de la nueva.
7. Mensaje final:
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
