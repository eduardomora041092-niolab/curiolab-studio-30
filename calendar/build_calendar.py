"""Builds the 90-video editorial calendar for CurioLab Studio 30.
Pattern per day: slot 1 and 2 = Mecanismo, slot 3 = Ciencia (60 + 30).
Day 1 = 2026-10-20. Run: python3 build_calendar.py
"""
import csv, datetime as dt, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
START = dt.date(2026, 10, 20)

# (titulo, gancho 0-3 s, concepto visual, dificultad)
MECH = [
 ("¿Cómo funciona una cremallera por dentro?", "Se cierra sin imanes ni pegamento.", "Vista frontal de dientes intercalados, corte del cursor con canal en Y y cuña.", "Media"),
 ("¿Por qué un termo mantiene el café caliente?", "Horas después, sigue caliente. ¿Cómo?", "Corte de doble pared con vacío; flechas de conducción, convección y radiación bloqueadas.", "Media"),
 ("¿Cómo abre una llave una cerradura?", "Sin la llave correcta, este cilindro no gira.", "Corte del cilindro con pernos de dos piezas alineándose en la línea de corte.", "Media"),
 ("¿Cómo escribe un bolígrafo?", "Todo depende de una bolita de apenas un milímetro.", "Punta en corte: bola que gira y arrastra tinta del depósito al papel.", "Baja"),
 ("¿Cómo funciona el clic de un bolígrafo?", "Un clic sale, otro clic entra. ¿Qué hay dentro?", "Leva giratoria con dientes y muelle; rotación por pasos entre dos posiciones.", "Alta"),
 ("¿Cómo funciona la cisterna del inodoro?", "Siempre se llena justo hasta el mismo nivel.", "Corte del tanque: válvula de descarga, flotador que cierra la entrada.", "Media"),
 ("¿Cómo enfría un refrigerador?", "Tu nevera no crea frío: saca el calor.", "Ciclo cerrado: compresor, condensador, válvula de expansión y evaporador con flechas de calor.", "Alta"),
 ("¿Cómo calienta un microondas?", "Calienta la comida sin calentar el aire.", "Ondas del magnetrón, moléculas de agua oscilando, plato giratorio.", "Media"),
 ("¿Cómo sabe la tostadora cuándo parar?", "Nadie la apaga, pero salta sola.", "Temporizador y pestillo electromagnético que libera el muelle de la bandeja.", "Media"),
 ("¿Cómo dobla una grapa la grapadora?", "La grapa entra recta y sale doblada.", "Corte: cuchilla empuja la grapa contra el yunque con dos ranuras curvas.", "Baja"),
 ("¿Cómo se abre un paraguas?", "Un solo empujón abre todas las varillas.", "Mecanismo de corredera, varillas articuladas y pestillo de bloqueo.", "Media"),
 ("¿Por qué la cinta métrica vuelve sola?", "Suéltala y regresa a toda velocidad.", "Muelle espiral que se carga al sacar la cinta; freno de bloqueo; cinta curvada.", "Baja"),
 ("¿Cómo funciona un candado de combinación?", "Tres números correctos… y se abre.", "Discos con muesca que se alinean bajo la barra de cierre.", "Alta"),
 ("¿Cómo mide el tiempo un reloj mecánico?", "Sin pilas, marca cada segundo.", "Muelle real, rueda de escape y volante oscilante liberando un diente cada vez.", "Alta"),
 ("¿Cómo suena una tecla de piano?", "Pulsas una tecla y un martillo golpea.", "Palanca de la tecla, martillo de fieltro, cuerda vibrando y apagador.", "Media"),
 ("¿Por qué el cinturón se bloquea en un frenazo?", "Tiras despacio, sale. Tiras rápido, se traba.", "Retractor con péndulo y trinquete que traba el carrete.", "Media"),
 ("¿Cómo se infla un airbag tan rápido?", "Se infla en menos tiempo que un parpadeo.", "Sensor de impacto, generador de gas, bolsa que se expande y desinfla por orificios.", "Media"),
 ("¿Cómo frena un coche con frenos de disco?", "Tu pie mueve un coche de una tonelada.", "Pedal, presión hidráulica, pinza apretando pastillas contra el disco.", "Media"),
 ("¿Cómo detecta el humo un detector?", "Ve el humo sin ojos.", "Cámara óptica: LED y fotodiodo; el humo dispersa la luz hacia el sensor.", "Media"),
 ("¿Cómo sabe la pantalla dónde la tocas?", "Funciona con tu dedo, pero no con un guante.", "Rejilla de electrodos; el dedo altera la carga eléctrica en un punto.", "Media"),
 ("¿Cómo convierte un altavoz electricidad en sonido?", "Un imán y una bobina hacen música.", "Bobina en campo magnético mueve el cono; ondas de aire.", "Baja"),
 ("¿Cómo convierte un micrófono tu voz en electricidad?", "Es un altavoz funcionando al revés.", "Diafragma mueve bobina en campo magnético generando corriente.", "Baja"),
 ("¿Cómo gira un motor eléctrico?", "Imanes que se persiguen sin alcanzarse.", "Rotor con bobinas, imanes, conmutador invirtiendo la corriente.", "Media"),
 ("¿Cómo genera luz la dinamo de una bicicleta?", "Pedaleas y se enciende la luz.", "Imán girando dentro de una bobina induce corriente.", "Media"),
 ("¿Cómo produce luz un LED?", "No tiene filamento y se calienta mucho menos que una bombilla clásica.", "Unión de semiconductores; electrones que liberan fotones.", "Media"),
 ("¿Cómo calienta una placa de inducción?", "La placa no quema, la sartén sí.", "Bobina con corriente alterna, campo magnético, corrientes en la base metálica.", "Media"),
 ("¿Por qué cocina más rápido una olla a presión?", "El agua hierve a más de 100 °C aquí dentro.", "Tapa sellada, presión creciente, punto de ebullición más alto, válvula de seguridad.", "Baja"),
 ("¿Cómo funciona una cafetera italiana?", "El agua sube sola hasta el café.", "Corte: depósito inferior, presión del vapor empuja agua por el filtro.", "Baja"),
 ("¿Cómo hace chispa un encendedor de clic?", "Sin pilas ni piedra: solo un golpe.", "Cristal piezoeléctrico golpeado por martillo genera alto voltaje.", "Media"),
 ("¿Cómo apaga el fuego un extintor?", "Aprietas y sale con mucha presión.", "Recipiente presurizado, tubo sifón, válvula; triángulo del fuego.", "Baja"),
 ("¿Cómo funciona el picaporte de una puerta?", "Gira la manilla y el pestillo se esconde.", "Cerradero, pestillo biselado y muelle de retorno.", "Baja"),
 ("¿Cómo funciona un pulverizador de gatillo?", "Cada apretón lanza una nube fina.", "Bomba de pistón, válvulas antirretorno y boquilla.", "Media"),
 ("¿Cómo sale el líquido de un aerosol?", "Presionas y sale solo.", "Gas propulsor a presión, tubo, válvula y boquilla.", "Baja"),
 ("¿Cómo mezcla agua fría y caliente un grifo monomando?", "Una sola palanca controla todo.", "Cartucho con discos cerámicos que alinean orificios.", "Media"),
 ("¿Por qué las tijeras cortan?", "Dos cuchillas que no se tocan… hasta el punto exacto.", "Palanca, eje y punto de corte que se desplaza.", "Baja"),
 ("¿Cómo funciona un cortaúñas?", "Dos palancas en un objeto diminuto.", "Palanca compuesta multiplicando la fuerza.", "Baja"),
 ("¿Cómo funciona un inflador de bicicleta?", "Bombeas y el aire no vuelve atrás.", "Pistón, cilindro y válvulas antirretorno.", "Baja"),
 ("¿Cómo funciona la válvula de un neumático?", "El aire entra, pero no sale.", "Válvula con muelle que la presión interna mantiene cerrada.", "Baja"),
 ("¿Cómo funciona una escalera mecánica?", "Los escalones aparecen y desaparecen.", "Cadena, ruedas en dos rieles que forman los escalones y los aplanan.", "Media"),
 ("¿Por qué gira el brazo del lavavajillas?", "No tiene motor propio, pero gira.", "Chorros inclinados empujan el brazo por reacción.", "Baja"),
 ("¿Cómo convierte un panel solar la luz en electricidad?", "La luz empuja electrones.", "Célula de silicio con dos capas, fotón liberando electrón, circuito.", "Media"),
 ("¿Cómo se recarga una batería de litio?", "Los iones viajan de un lado a otro.", "Ánodo, cátodo, electrolito; iones de litio moviéndose al cargar y descargar.", "Media"),
 ("¿Cómo carga el móvil sin cables?", "Lo apoyas y empieza a cargar.", "Dos bobinas; campo magnético variable induce corriente.", "Media"),
 ("¿Cómo sabe el GPS dónde estás?", "Satélites que no saben que existes.", "Distancias a varios satélites y círculos que se cruzan en un punto.", "Media"),
 ("¿Cómo lee un escáner el código de barras?", "Unas rayas guardan un número.", "Láser o luz que se refleja en barras blancas y negras, señal digital.", "Baja"),
 ("¿Cómo funciona un abrelatas?", "Corta el metal sin esfuerzo.", "Rueda de corte, rueda dentada de arrastre y palanca.", "Baja"),
 ("¿Cómo cambia de marcha una bicicleta?", "La cadena salta de piñón sin caerse.", "Desviador empujando la cadena entre piñones de distinto tamaño.", "Media"),
 ("¿Cómo sabe una puerta automática que llegas?", "Se abre antes de que la toques.", "Sensor de movimiento o infrarrojo, motor y correa.", "Baja"),
 ("¿Cómo imprime una impresora de tinta?", "Gotas más pequeñas que un cabello.", "Cabezal con cámaras que expulsan gotas por calor o vibración.", "Media"),
 ("¿Cómo cancelan el ruido unos auriculares?", "Silencio creado con más sonido.", "Micrófono, onda invertida que anula la onda del ruido.", "Media"),
 ("¿Cómo funciona un mando a distancia?", "Luz que tus ojos no ven.", "LED infrarrojo enviando pulsos codificados al receptor.", "Baja"),
 ("¿Por qué un ascensor necesita contrapeso?", "El motor no levanta todo el peso.", "Cabina, cables, polea y contrapeso equilibrando la carga.", "Baja"),
 ("¿Por qué la rueda de la bici gira sin pedalear?", "Dejas de pedalear y la rueda sigue.", "Rueda libre con trinquetes y muelles.", "Media"),
 ("¿Cómo funciona un sacacorchos de alas?", "Las alas suben solas.", "Engranajes de piñón y cremallera multiplicando la fuerza.", "Baja"),
 ("¿Cómo muele un molinillo de pimienta?", "Girar y moler en un solo gesto.", "Muela cónica girando dentro de un anillo dentado.", "Baja"),
 ("¿Cómo sube el agua una bomba manual?", "Subes la palanca y el agua sube contigo.", "Pistón, válvulas y vacío parcial que eleva el agua.", "Media"),
 ("¿Cómo funciona un secador de pelo?", "Aire caliente en segundos.", "Ventilador, resistencia eléctrica y protector térmico.", "Baja"),
 ("¿Cómo aspira una aspiradora?", "No absorbe la suciedad: la empuja el aire.", "Ventilador crea baja presión; aire exterior entra con la suciedad.", "Baja"),
 ("¿Cómo funciona una tecla de teclado mecánico?", "Cada tecla tiene su propio interruptor.", "Interruptor con muelle y contactos metálicos que cierran el circuito.", "Baja"),
 ("¿Cómo se ajusta una llave inglesa?", "Una llave para muchas tuercas.", "Tornillo sin fin que desplaza la mandíbula móvil.", "Baja"),
]

SCI = [
 ("¿Por qué el cielo es azul?", "La luz del Sol es blanca… pero el cielo no.", "Haz blanco que se separa en colores; moléculas dispersan el azul; atardecer con trayecto largo.", "Media"),
 ("¿Por qué el mar es salado?", "Los ríos son dulces, pero el mar no.", "Lluvia, rocas que liberan minerales, ríos al mar, evaporación que deja la sal.", "Baja"),
 ("¿Cómo se forma un arcoíris?", "Cada gota de lluvia es un pequeño prisma.", "Rayo que entra en la gota, se refracta, se refleja y sale separado en colores.", "Media"),
 ("¿Por qué vemos el rayo antes de oír el trueno?", "Cuenta los segundos y sabrás la distancia.", "Luz y sonido viajando a velocidades muy distintas.", "Baja"),
 ("¿Por qué el hielo flota?", "Casi todo sólido se hunde en su líquido. El hielo no.", "Moléculas de agua en red hexagonal con más espacio, menor densidad.", "Baja"),
 ("¿Qué causa las mareas?", "La Luna mueve océanos enteros.", "Tierra, Luna y dos abultamientos de agua por la gravedad.", "Media"),
 ("¿Por qué la Luna cambia de forma?", "La Luna no cambia: cambia lo que ves.", "Luna iluminada por el Sol y vista desde distintos ángulos.", "Baja"),
 ("¿Por qué existen las estaciones?", "No es por la distancia al Sol.", "Eje inclinado de la Tierra y ángulo de los rayos solares.", "Media"),
 ("¿Por qué los gatos suelen caer de pie?", "Giran en el aire sin apoyarse en nada.", "Reflejo de enderezamiento: rotación de la parte delantera y trasera.", "Media"),
 ("¿Por qué burbujea un refresco?", "Las burbujas estaban ahí, escondidas.", "CO2 disuelto a presión que escapa al abrir.", "Baja"),
 ("¿Por qué crece el pan?", "Seres diminutos inflan la masa.", "Levadura produciendo CO2 atrapado en la red de gluten.", "Baja"),
 ("¿Por qué se empaña el espejo del baño?", "El vapor está ahí, pero no lo ves.", "Vapor de agua que se condensa sobre la superficie fría.", "Baja"),
 ("¿Qué son las auroras boreales?", "Luces en el cielo causadas por el Sol.", "Partículas solares guiadas por el campo magnético excitando gases.", "Media"),
 ("¿Cómo brillan las luciérnagas?", "Luz fría fabricada por un insecto.", "Reacción de luciferina y luciferasa con oxígeno.", "Baja"),
 ("¿Cómo cambia de color un camaleón?", "No usa pigmentos nuevos.", "Capas de nanocristales en la piel que cambian de separación y reflejan otros colores.", "Media"),
 ("¿Cómo se forma el granizo?", "Hielo que cae en pleno verano.", "Corrientes ascendentes en la nube que suben y bajan la piedra, sumando capas.", "Media"),
 ("¿Por qué vemos siempre la misma cara de la Luna?", "La Luna sí gira… al mismo ritmo.", "Rotación sincronizada con la órbita.", "Baja"),
 ("¿Por qué erupciona un volcán?", "Roca fundida con gases a presión.", "Corte de volcán, cámara magmática, gases que empujan el magma.", "Media"),
 ("¿Por qué ocurren los terremotos?", "El suelo bajo tus pies se mueve.", "Placas tectónicas que acumulan tensión y la liberan de golpe.", "Media"),
 ("¿Por qué la sal derrite el hielo?", "La sal no calienta el hielo.", "Descenso del punto de congelación del agua con sal.", "Baja"),
 ("¿Por qué la cebolla te hace llorar?", "Es una defensa química de la cebolla.", "Células cortadas liberan un gas irritante que llega a los ojos.", "Baja"),
 ("¿Por qué brillan los ojos de los gatos en la oscuridad?", "Tienen un espejo dentro del ojo.", "Tapetum lucidum reflejando la luz de vuelta a la retina.", "Baja"),
 ("¿Por qué titilan las estrellas?", "Las estrellas no parpadean: es nuestro aire.", "Luz que atraviesa capas de aire en movimiento y se desvía.", "Baja"),
 ("¿Por qué los copos de nieve tienen seis puntas?", "Todos distintos, pero todos con seis brazos.", "Estructura hexagonal de las moléculas de agua al congelarse.", "Media"),
 ("¿Cómo se forma una nube?", "Una nube pesa toneladas y flota.", "Aire húmedo que sube, se enfría y condensa en gotitas.", "Baja"),
 ("¿Por qué cambian de color las hojas en otoño?", "El amarillo siempre estuvo ahí.", "Clorofila que se degrada y deja ver carotenoides.", "Baja"),
 ("¿Qué es el eco?", "Tu voz vuelve a ti.", "Onda sonora que rebota en una superficie lejana.", "Baja"),
 ("¿Por qué el agua hierve antes en la montaña?", "En la cima, el agua hierve por debajo de 100 °C.", "Menor presión atmosférica, menor punto de ebullición.", "Baja"),
 ("¿Cómo flota un barco de acero?", "Una bola de acero se hunde; un barco no.", "Principio de Arquímedes: agua desplazada y empuje.", "Baja"),
 ("¿Cómo trepa un gecko por el cristal?", "Sin ventosas ni pegamento.", "Millones de pelos microscópicos con fuerzas de atracción entre moléculas.", "Media"),
]
assert len(MECH) == 60 and len(SCI) == 30
titles = [t[0] for t in MECH + SCI]
assert len(set(titles)) == 90, "duplicate titles"

DUR = {"Baja": "25-30 s", "Media": "28-32 s", "Alta": "30-35 s"}
rows = []
mi = si = 0
for n in range(1, 91):
    day = (n - 1) // 3 + 1; slot = (n - 1) % 3 + 1
    if slot < 3:
        t, hook, vis, diff = MECH[mi]; mi += 1; cat = "Mecanismo"
    else:
        t, hook, vis, diff = SCI[si]; si += 1; cat = "Ciencia"
    rows.append({
        "id": f"{n:03d}", "dia": day, "fecha": (START + dt.timedelta(days=day - 1)).isoformat(), "slot": slot,
        "categoria": cat, "titulo": t, "gancho": hook, "concepto_visual": vis,
        "duracion_objetivo": DUR[diff], "dificultad": diff, "estado": "PLANNED",
        "youtube_url": "", "tiktok_url": "", "buffer_post_ids": "", "archivo": "", "notas": "",
    })

# Known states (verified in this project)
rows[0].update(estado="PUBLISHED", archivo="/home/claude/v001/CurioLab_001_FINAL.mp4",
               buffer_post_ids="youtube:6ad753635008aca7fa263030; tiktok:6ad753635008aca7fa26302f",
               notas="Buffer status=sent (YT 2026-10-20 11:41:25Z, TT 11:42:04Z). URL pública no expuesta por Buffer.")
for idx, vid in ((1, "002"), (2, "003")):
    f, q = f"/home/claude/curiolab/out/CurioLab_{vid}.mp4", f"/home/claude/curiolab/work/{vid}/qa.json"
    if os.path.exists(f) and os.path.exists(q) and json.load(open(q))["all_pass"]:
        rows[idx].update(estado="PRODUCED", archivo=f, notas="QA técnico PASS. Pendiente de aprobación.")

with open(os.path.join(HERE, "CurioLab_calendario_90.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(rows, open(os.path.join(HERE, "calendar.json"), "w"), ensure_ascii=False, indent=1)
print("rows", len(rows), "mech", mi, "sci", si)
