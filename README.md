# Glumtar: The Quest

# Título del juego y sinopsis: Glumtar
Glumtar es un juego arcade clásico. Embarcados en una nave espacial, vamos en busca del planeta Glumtar. Es el único lugar de la galaxia en el que el ser humano puede habitar, después de que la Tierra haya sido destruida.

Pero nadie sabe con exactitud dónde está Glumtar. Para encontrarlo, en un entorno distópico y desolado —faltaría más—, solo nos queda el viejo método que ha engrandecido a la raza humana: el ensayo y el error.

# Idioma inglés
He optado por escribir el código en inglés, para simular trabajar con una empresa internacional.

# Archivo game: el Gameloop
El Gameloop básico es:

Frontpage > play level > resolve level > records page.

Sin embargo, la fase "play level > resolve level" puede ser un bucle tan largo como se necesite.

A través del método set_up_play, podemos generar una partida automáticamente con el número de niveles que se indique en available_play_levels (especificar un número inmediatamente mayor al número de niveles deseado).

# Frontpage
Es la página de inicio. Incluye tres páginas con la historia de Glumtar, una breve indicación sobre lo que hay que hacer y un gráfico con los puntos que reparte cada meteorito.

Estas páginas se pueden recorrer hacia delante y atrás con las flechas derecha e izquierda.

# Playlevel
Actualmente solo hay dos niveles de juego diseñados. Se distinguen por el escenario, el indicador de nivel en la parte superior de la pantalla y la frecuencia con la que se disparan los meteoritos (se puede modificar en el archivo __init__). Recorrer cada nivel lleva 1 minuto y 30 segundos.

El nivel se supera cuando el "scroll" del fondo de la pantalla llega a cero. Eso supone que el extremo derecho de la imagen de fondo está colocado en el extremo derecho de la pantalla. En ese momento, se activa la resolución del nivel.

# Resolvelevel
Al activarse, la nave se mueve sola y se inicia el "aterrizaje". El fondo de la pantalla cambia con un fundido a un escenario diferente. Además, se muestran alertas para avisar de la aproximación a un nuevo planeta, su nombre e instrucciones para continuar.

Si el nivel que se resuelve es el último, al continuar llegaremos a la pantalla de records o, si no pulsamos las teclas indicadas, se reseteará la partida en un minuto y medio. Lo hará retornando una llamada a reset_game al Gameloop.

Actualmente, el último nivel es el 2. Si hubiese más, habría que especificar en el código de esta clase cuál es el nivel que resuelve el juego.

# Best scores
Muestra la tabla de máximmas puntuaciones. La clase BestPlayers es la que llama a DBManager para gestionar la base de datos SQLite.

Cuando hay un nuevo récord, se activa el modo de inserción. Permite escribir tres iniciales para el nombre del jugador. Se muestra un cursor parpadeante para hacer notar dónde se verán las letras que el usuario teclee. Solo se permite escribir letras y se puede borrar lo que se escriba antes de pulsar Enter.

# La nave
La nave se mueve verticalmente al pulsar las flechas arriba/abajo. Si se mantienen pulsadas, el sprite acelera su movimiento.

# Los meteoritos
Hay cinco familias de meteoritos, cada una con velocidades, puntos repartidos y tamaños diferentes. Su puntuación y velocidad se pueden editar en entities.py. Los del nivel 1 aparecen también en el nivel 2, pero los del nivel 2 no aparecen en el nivel 1.

* Nivel 1:

    - Familia 0.
    - Familia 1.
    - Familia 2.

* Nivel 2:

    - Familia 3.
    - Familia 4.

# El contador de vidas
Descuenta vidas además de corazones, para que sea más visual la evolución de la partida mientras se juega.

# El marcador
Únicamente gestiona los puntos. Consiste en un acumulador de puntos que se actualiza cuando un meteorito se pierde por el lado izquierdo de la pantalla. También muestra el título "Score". También supone la instancia desde la que BestPlayers leerá si hay un nuevo récord que mandar a la base de datos.

# La base de datos
Está creada en SQLite. Devuelve la consulta restringida a 5 entradas, ordenadas de mayor a menor por el índice "Score".

# La clase Reader
Una clase muy útil apra generar alertas y mensajes rápidamente en cualquier escena. Solo hay que escribir en un archivo .txt, generar una instancia Reader y pasarle el número de líneas, posición, color, tamaño de letra, fuente e incluso interlineado que se quiere usar. También permite renderizar y dibujar el resultado.

# Fundidos y animaciones
El juego dispone de varios eventos de usuario para controlar distintos temporizadores. Se utilizan para generar animaciones, como la explosión de la nave, los fundidos en los "aterrizajes" o el parpadeo del cursor al insertar un nuevo récord.

# Carpeta tools
En la carpeta tools encontrarás herramientas útiles para el diseño del juego:

* Paleta de colores creada con coolors: [Ver en la web](https://coolors.co/c0d6df-2e2d4d-d88373-bd1e1e-4ecdc4)

    - Versión en png.
    - Versión en scss.

* Archivo timers and countdowns:

    - ScrollBG: para controlar el movimiento del fondo.
    - Countdown: para congelar la partida y hacer una cuenta atrás antes de volver a empezar.

# Imágenes y música
Las imágenes las he creado yo en lugar de recurrir a librerías. La música es una maqueta propia que he rescatado. Todo ello me ha servido para controlar la estética del juego y la comunicación de los distintos eventos que suceden en cada partida. Además de poner en práctica otras facetas profesionales.

# Fuentes
He elegido la fuente Press Start 2P, por su aspecto de video juego antiguo. Se puede descargar de forma gratuita en [Google fonts: ](https://fonts.google.com/specimen/Press+Start+2P?query=press+start)
