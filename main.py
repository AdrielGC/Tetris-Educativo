import flet as ft # Importa la librería Flet para crear la interfaz
import flet_audio as fta
import asyncio # Librería para tareas asíncronas
import random # Para elegir piezas aleatorias

"""
Configuración general del tamaño de la cuadricula
"""
WIDTH, HEIGHT = 380, 720 # Tamaño de la ventana
CELL_SIZE = 20 # Tamaño de cada celda del tablero

# row: fila, col: columna
GRID_COLS, GRID_ROWS = 10, 20 # Número de columnas y filas del tablero

"""
Tamaño de las celdas
"""
GRID_PX_W = GRID_COLS * CELL_SIZE # Ancho del tablero 10 columnas * 22 px = 220 px
GRID_PX_H = GRID_ROWS * CELL_SIZE # Alto del tablero 20 columnas * 22 px = 440 px

"""
Colores que se ocupan en el juego.
"""
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAY = "#464646"
SKY_BLUE = "#7dbae6"
BLUE = "#0000c8"
YELLOW = "#ffd700"
DARK_BLUE = "#00001e"
RED = "#ff453a"
GREEN = "#006400"

# Colores asignados a cada tipo de pieza
piece_colors = {
    "I": "#ff0000",
    "O": "#00ff80",
    "T": "#ffff00",
    "J": "#ff8000",
    "L": "#ff1493",
    "S": "#9400d3",
    "Z": "#00ffff",
}

"""
Formas de las piezas del Tetris
"""
#Formas de las figuras
Shapes = {
    "I": [[1,1,1,1]],#Pieza en forma de línea
    "O": [[1,1],     #Pieza cuadrada
          [1,1]],
    "T": [[1,1,1],   #Pieza en forma de T
          [0,1,0]],
    "J": [[1,0,0],   #Pieza J
          [1,1,1]],
    "L": [[0,0,1],   #Pieza L
          [1,1,1]],
    "S": [[0,1,1],   #Pieza S
          [1,1,0]],
    "Z": [[1,1,0],   #Pieza Z
          [0,1,1]],
}

# Lista con las claves de las piezas para elegirlas aleatoriamente
# Convierte las claves del diccionario en una lista
SHAPE_KEYS = list(Shapes.keys())

def show_instructions(page, on_back):
    page.controls.clear()
    page.add(
        ft.Container(
            width=WIDTH, height=HEIGHT, bgcolor="#1a1a1a", padding=40,
            content=ft.Column([
                ft.Text("INSTRUCCIONES", size=14, weight="bold", color=WHITE, font_family="Fuente", text_align=ft.TextAlign.CENTER),
                ft.Container(height=40),
                
                # Sección Controles
                ft.Text("CONTROLES", size=12, weight="bold", color=YELLOW, font_family="Fuente"),
                ft.Container(height=30),
                ft.Text("◀  ▶  : Mover", size=16, color=WHITE, font_family="Arial"),
                ft.Text("▲ : Rotar pieza", size=16, color=WHITE, font_family="Arial"),
                ft.Text("▼ : Bajar pieza", size=16, color=WHITE, font_family="Arial"),
                ft.Text("Espacio : Drop", size=16, color=WHITE, font_family="Arial"),
                ft.Text("ESC / Botón || : Pausar juego", size=16, color=WHITE, font_family="Arial"),
                
                ft.Container(height=10),
                
                # Sección Niveles
                ft.Text("NIVELES", size=12, weight="bold", color=YELLOW, font_family="Fuente"),
                ft.Container(height=10),
                ft.Text("Nivel 1: Sumas (+)", size=16, color=WHITE, font_family="Arial"),
                ft.Text("Nivel 2: Restas (-)", size=16, color=WHITE, font_family="Arial"),
                ft.Text("Nivel 3: Multiplicaciones (x)", size=16, color=WHITE, font_family="Arial"),
                ft.Text("Nivel 4: Divisiones (/)", size=16, color=WHITE, font_family="Arial"),
                
                ft.Container(height=10),
                
                ft.Button(
                    "VOLVER", width=180, height=55,
                    # Solución: Usar el callback que ya le estás pasando a la función
                    on_click=lambda e: on_back(), 
                    style=ft.ButtonStyle(bgcolor=GRAY, color=WHITE, text_style=ft.TextStyle(size=14, font_family="Fuente", weight="bold"))
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )
    page.update()
#  PANTALLAS
def show_main_menu(page, on_start): #Pantalla del menu principal
    page.controls.clear()
    page.add(
        ft.Stack(
            [
                # Imagen de fondo
                ft.Image(
                    src="menu.png",
                    width=WIDTH,
                    height=HEIGHT,
                    fit="cover",
                ),
                # Botón encima del fondo
                ft.Container(
                    width=WIDTH,
                    height=HEIGHT,
                    content=ft.Column(
                        [
                            ft.Container(height=350),  # ← sube/baja el botón 
                            ft.Button(
                                "JUGAR",
                                width=180,
                                height=55,
                                on_click=lambda e: on_start(),
                                style=ft.ButtonStyle(
                                    bgcolor=GREEN,
                                    color=WHITE,
                                    text_style=ft.TextStyle(
                                        size=11,
                                        font_family="Fuente",
                                        weight="bold"
                                    )
                                )
                            ),
                            ft.Container(height=10),
                            # Botón INSTRUCCIONES
                            ft.Button(
                                "INSTRUCCIONES",
                                width=250, height=55,
                                on_click=lambda e: show_instructions(page, lambda: show_main_menu(page, on_start)),
                                style=ft.ButtonStyle(
                                    bgcolor=GREEN, color=WHITE,
                                    text_style=ft.TextStyle(size=10, font_family="Fuente", weight="bold")
                                )
                            ),
                            
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
            ],
            width=WIDTH,
            height=HEIGHT,
        )
    )
    page.update()


def show_question_screen(page, game, on_correct, on_wrong):# Pantalla de pregunta
     
    a, b, oper, correct = game.ask_math_question()# Obtiene los dos numeros, el operador y la respuesta correcta segun el nivel actual

    answer_field = ft.TextField( #Donde el jugador escribe la respuesta
        label="Tu respuesta",
        width=180,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        color=BLACK,
        label_style=ft.TextStyle(color=BLACK),
        border_color=BLACK,
        focused_border_color=BLACK,
    )
    result_text = ft.Text("", size=12)#Muestra si la respuesta fue correcta o no

    async def _delay_then(callback):# Espera 1 segundo para cambiar de pantalla, para que el jugador pueda ver el resultado antes de que cambie la pantalla
        await asyncio.sleep(1)
        callback()

    async def check_answer(e):#Verifica la respuesta del jugador cuando presiona el boton confirmar
#Si es correcto espera y llama a on_correct(), sino llama a on_wrong()
        try:
            ans = int(answer_field.value)
            if ans == correct:
                result_text.value = "¡Correcto!"
                result_text.color = GREEN
                page.update()
                await asyncio.sleep(1)
                on_correct()
            else:
                result_text.value = f"Incorrecto. La respuesta era {correct}"
                result_text.color = RED
                page.update()
                await asyncio.sleep(1)
                on_wrong()
        except ValueError:
            result_text.value = "Escribe un número"
            result_text.color = WHITE
            page.update()

    page.controls.clear()
    page.add(
        ft.Stack(
            [
                # Imagen de fondo
                ft.Image(
                    src="pregunta.png",
                    width=WIDTH,
                    height=HEIGHT,
                    fit="cover",
                ),
                # Contenido encima
                ft.Container(
                    width=WIDTH,
                    height=HEIGHT,
                    content=ft.Column(
                        [
                            ft.Container(height=80),  # sube/baja el contenido
                            ft.Text(
                                f"Nivel {game.level} completado",
                                size=19,
                                color=WHITE,
                                font_family="Fuente",
                                weight="bold",
                            ),
                            ft.Container(height=15),
                            ft.Text("Responde para continuar:", size=17, color=WHITE),
                            ft.Container(height=10),
                            ft.Text(
                                f"{a}  {oper}  {b}  =  ?",
                                size=20,
                                color=WHITE,
                                weight="bold",
                                font_family="Arial",
                            ),
                            ft.Container(height=200),
                            answer_field,
                            ft.Container(height=10),
                            ft.Button(
                                "Confirmar",
                                width=160,
                                height=48,
                                on_click=check_answer,
                                style=ft.ButtonStyle(
                                    bgcolor=BLUE,
                                    color=WHITE,
                                    text_style=ft.TextStyle(size=18, font_family="Arial")
                                )
                            ),
                            ft.Container(height=15),
                            result_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
            ],
            width=WIDTH,
            height=HEIGHT,
        )
    )
    page.update()


def show_victory_screen(page, game, on_continue):#Pantalla de victoria
    
    page.controls.clear()
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="victoria.png",
                    width=WIDTH,
                    height=HEIGHT,
                    fit="cover",
                ),
                ft.Container(
                    width=WIDTH,
                    height=HEIGHT,
                    content=ft.Column(
                        [
                            ft.Container(height=520),  # sube/baja el botón
                            ft.Button(
                                "Siguiente nivel",
                                width=200,
                                height=52,
                                on_click=lambda e: on_continue(),
                                style=ft.ButtonStyle(
                                    bgcolor=GREEN,
                                    color=WHITE,
                                    text_style=ft.TextStyle(size=15, font_family="Fuente")
                                )
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
            ],
            width=WIDTH,
            height=HEIGHT,
        )
    )
    page.update()


def show_game_over_screen(page, on_retry, on_menu):#Pantalla de game over
   
    page.controls.clear()
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="gameover.png",
                    width=WIDTH,
                    height=HEIGHT,
                    fit="cover",
                ),
                ft.Container(
                    width=WIDTH,
                    height=HEIGHT,
                    content=ft.Column(
                        [
                            ft.Container(height=490),  #sube/baja los botones
                            ft.Button(
                                "Reintentar",
                                width=180,
                                height=52,
                                on_click=lambda e: on_retry(),
                                style=ft.ButtonStyle(
                                    bgcolor=YELLOW,
                                    color=BLACK,
                                    text_style=ft.TextStyle(size=15, font_family="Fuente")
                                )
                            ),
                            ft.Container(height=12),
                            ft.Button(
                                "Menú principal",
                                width=180,
                                height=52,
                                on_click=lambda e: on_menu(),
                                style=ft.ButtonStyle(
                                    bgcolor=GRAY,
                                    color=WHITE,
                                    text_style=ft.TextStyle(size=15, font_family="Fuente")
                                )
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
            ],
            width=WIDTH,
            height=HEIGHT,
        )
    )
    page.update()


def show_game_complete_screen(page, on_menu):#Pantalla juego completado
    
    page.controls.clear()
    page.add(
        ft.Stack(
            [
                ft.Image(
                    src="completado.png",
                    width=WIDTH,
                    height=HEIGHT,
                    fit="cover",
                ),
                ft.Container(
                    width=WIDTH,
                    height=HEIGHT,
                    content=ft.Column(
                        [
                            ft.Container(height=530),  # sube/baja el botón
                            ft.ElevatedButton(
                                "Volver al menú",
                                width=200,
                                height=52,
                                on_click=lambda e: on_menu(),
                                style=ft.ButtonStyle(
                                    bgcolor=GREEN,
                                    color=WHITE,
                                    text_style=ft.TextStyle(size=15, font_family="Fuente")
                                )
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.alignment.Alignment(0, 0),
                ),
            ],
            width=WIDTH,
            height=HEIGHT,
        )
    )
    page.update()


#  FUNCIONES DEL TABLERO
def create_grid():
    """
    Crea la cuadrícula visual del tablero usando contenedores de Flet.
    Cada celda es un Container que representa un bloque del juego.
    """
    grid = [] # Lista que contendrá todas las filas
    for row in range(GRID_ROWS):  # Recorre cada fila
        row_cells = []            # Lista de celdas de una fila
        for col in range(GRID_COLS):  # Recorre cada columna
            cell = ft.Container(
                width=CELL_SIZE - 1,    # ancho de la celda
                height=CELL_SIZE - 1,   # alto de la celda
                bgcolor="black",         # color inicial (negro)
                border_radius=3,        # esquinas redondeadas
                alignment=ft.alignment.Alignment(0, 0),
            )
             # contenedor externo para centrar y simular margen
            wrapper = ft.Container(
                width=CELL_SIZE,
                height=CELL_SIZE,
                content=cell,
                alignment=ft.alignment.Alignment(0, 0)
            )
            row_cells.append(wrapper) # Agrega la celda a la fila
        grid.append(ft.Row(row_cells, spacing=0)) # Agrega la fila al grid
    return ft.Column(grid, spacing=0)  # Devuelve todo el tablero como columna


"""
Dibuja un bloque individual
"""
def draw_block(grid_ui, row, col, color):
    # Verifica que la posición esté dentro del tablero
    if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
        cell = grid_ui.controls[row].controls[col].content
        cell.bgcolor = color

""" 
Nos ayudará a crear una pieza completa en pantalla 
"""
def draw_tetromino(grid_ui, shape, gx, gy, color):
    # Recorre la matriz de la pieza
    for r, row in enumerate(shape): # r = fila de la pieza
        for c, v in enumerate(row): # c = columna de la pieza
            if v:                   # si hay un bloque (1)
                 # Dibuja el bloque en el grid
                draw_block(grid_ui, gy + r, gx + c, color)

"""
Rota una pieza 90 grados
"""
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

"""
Nos permite que la pieza se pueda girar varias veces
"""
def rot(shape, times=1):
    out = shape # copia la forma original
    # Limita rotaciones a 4 (360°)   
    for _ in range(times % 4):
        out = rotate_shape(out) # rota la pieza
    return out # devuelve la pieza rotada


def draw_ghost(grid_ui, shape, gx, gy, color):
    """
    Dibuja el ghost con el mismo color de la pieza,
    pero solo como borde (sin relleno).
    """
    for r, row in enumerate(shape):
        for c, v in enumerate(row):
            if not v:
                continue
            x = gx + c
            y = gy + r
            if 0 <= y < GRID_ROWS and 0 <= x < GRID_COLS:
                cell = grid_ui.controls[y].controls[x].content
                # Solo si está vacío
                if cell.bgcolor == BLACK:
                    cell.border = ft.Border.all(1, color)

# Funciones faltantes del código original: draw_static_showcase(), def _ui_safe_start_row(),
# draw_start_screen(), show_instrucionts(), start_game(), exit_game(), 

"""
Representa una pieza del juego Tetris.
Contiene su forma, color y posición dentro del tablero.
"""
class Tetromino:

    #En este caso crea la pieza con su color, forma y posición
    def __init__(self, key=None):
        """
        Inicializa una nueva pieza.
        Si no se especifica el tipo de pieza, se elige una al azar.
        """
        if key is None: # Si no se recibe una clave de pieza
            key = random.choice(SHAPE_KEYS) # Se selecciona una pieza aleatoria
        self.key = key  # Guarda el tipo de pieza
        self.shape = [row[:] for row in Shapes[key]] # Copia la forma original
        self.color = piece_colors[key] # Asigna el color correspondiente
        self.x = GRID_COLS // 2 - len(self.shape[0]) // 2 # Coloca la pieza centrada
        self.y = 0  # La pieza inicia desde la parte superior

    #Nos ayuda a crear una copia de la pieza actual si es que la rotan
    def rotated(self):
        """
        Devuelve una copia de la pieza rotada 90 grados,
        sin modificar la pieza original.
        """
        t = Tetromino(self.key)            # Crea una nueva pieza del mismo tipo
        t.shape = rotate_shape(self.shape) # Aplica la rotación
        t.color = self.color               # Conserva el mismo color
        t.x, t.y = self.x, self.y          # Mantiene la misma posición
        return t                           # Regresa la nueva pieza

"""
Controla toda la lógica principal del juego:
movimientos, niveles, puntuación, preguntas y pantallas.
"""
class Game:

    #Contiene la lógica principal del juego
    def __init__(self):
        """
        Inicializa las variables principales del juego.
        """
        self.level = 1 # Nivel inicial
        self.lines_cleared = 0 #Lineas eliminadas
        self.lines_for_level = 1 # Lineas necesarias para pasar de nivel
        self.base_speed = 650 # Velocidad base de caída
        self.fall_interval_ms = self.base_speed # Intervalo de caída
        self.level_complete = False
        self.paused = False
        self.reset_game(self.level)  # Inicializa el estado del juego

 #Reinicia el juego con un nivel dado
    def reset_game(self, level=1):
        """
            Reinicia todas las variables del juego para comenzar
        desde un nivel específico.
        """
        self.level = level
        self.grid = [[None for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)] # Tablero vacío
        self.current = Tetromino() # Pieza actual
        self.next_piece = Tetromino() # Siguiente pieza
        self.score = 0 # Puntaje
        self.fall_timer = 0 # Temporizador de caída
        self.game_over = False # Estado de fin de juego
        self.lines_cleared = 0 # Reinicia líneas eliminadas
        self.level_complete = False

        # Velocidad base por nivel: cada nivel reduce el intervalo de caída para que las piezas bajen más rápido
        self.fall_interval_ms = self.base_speed - (self.level - 1) * 150
        
        # En el nivel 4 para agregar un extra de velocidad para agregarle más dificultad,
        # se le restan algunos milisegundos adicionales
        if self.level == 4:
            self.fall_interval_ms -= 60
            
        # Aseguramos que el intervalo nunca baje de 130 ms, porque si es menos
        # el juego se vuelve demasiado rápido y prácticamente injugable
        self.fall_interval_ms = max(130, self.fall_interval_ms)

    #Verifica si la pieza esta dentro del tablero, aparte verifica si se puede seguir creando piezas
    def valid(self, t):
        """
        Comprueba si una pieza puede colocarse en el tablero.
        Verifica límites del tablero y colisiones con piezas ya fijadas.
        """
        for r, row in enumerate(t.shape): #Recorre las filas de la forma
            for c, v in enumerate(row): # Recorre las columnas
                if not v: #Si no hay bloque, se ignora
                    continue
                gx, gy, = t.x + c, t.y + r # Calcula la posición real en la cuadrícula
                if gx < 0 or gx >= GRID_COLS or gy >= GRID_ROWS: #Fuera del tabler
                    return False
                if gy >= 0 and self.grid[gy][gx] is not None: #Colisión con otra pieza
                    return False
        return True #La posición es válida

    #Fija la pieza actual en el tablero
    def lock_piece(self):
        """
        Coloca la pieza actual de forma permanente en la cuadrícula,
        revisa líneas completas y gestiona cambios de nivel.
        """
        for r, row in enumerate(self.current.shape): # Recorre la forma de la pieza
            for c, v in enumerate(row):
                if not v:
                    continue
                gx, gy = self.current.x + c, self.current.y + r
                if gy < 0: # Si la pieza queda fuera por arriba
                    self.game_over = True
                    return
                self.grid[gy][gx] = self.current.color # Guarda el color en la cuadrícula

        cleared = self.clear_lines() # Elimina líneas completas
        if cleared:
            self.score += 100 * cleared # Aumenta el puntaje
            self.lines_cleared += cleared # Actualiza contador

        if self.lines_cleared >= self.lines_for_level:
            self.level_complete = True  # activa la pregunta
            return

        self.current = self.next_piece # Actualiza la pieza actual
        self.next_piece = Tetromino() # Genera la siguiente
        if not self.valid(self.current): # Si no puede colocarse
            self.game_over = True

#Detecta si se completaron las lineas y las elimina
     #Detecta si se completaron las lineas y las elimina 
    def clear_lines(self):
        """
        Revisa el tablero, elimina filas llenas
        y desplaza el resto hacia abajo.
        """
        full = [i for i in range(GRID_ROWS)
            if all(self.grid[i][c] is not None for c in range(GRID_COLS))]
        for i in full: 
            del self.grid[i] # Elimina la fila completa
            self.grid.insert(0, [None for _ in range(GRID_COLS)]) # Inserta fila vacía arriba
        return len(full) # Regresa cuántas filas se eliminaron

    #Ayuda a que las piezas bajen con un click del usuario
    def soft_drop(self):
        """
        Baja la pieza una posición cuando el jugador presiona el botón abajo.
        """
        test = Tetromino(self.current.key) # Crea una copia de la pieza
        test.shape = [row[:] for row in self.current.shape]
        test.color = self.current.color
        test.x, test.y = self.current.x, self.current.y + 1

        if self.valid(test): # Si la posición es válida
            self.current.y += 1   # Baja la pieza
        else:
            self.lock_piece()  # Fija la pieza

    def hard_drop(self):
        """
        Baja la pieza hasta el fondo cuando el jugador presiona el botón drop.
        """
        while True:
            test = Tetromino(self.current.key)
            test.shape = [row[:] for row in self.current.shape]
            test.color = self.current.color
            test.x, test.y = self.current.x, self.current.y + 1

            if self.valid(test):
                self.current.y += 1
            else:
                self.lock_piece()
                break


    #Es la que controla la caída automática de la pieza según el tiempo
    def update(self, dt):
        """
        Actualiza la posición de la pieza automáticamente
        según el tiempo transcurrido.
        """
        self.fall_timer += dt # Acumula el tiempo transcurrido desde la última actualización
        if self.fall_timer >= self.fall_interval_ms: # Si ya pasó el tiempo necesario para que caiga
            self.fall_timer = 0 # Reinicia el contador de tiempo
                
            test = Tetromino(self.current.key) # Crea una pieza de prueba con la misma forma
            test.shape = [row[:] for row in self.current.shape]  # Copia la forma actual
            test.color = self.current.color # Copia el color
            test.x, test.y = self.current.x, self.current.y + 1 # Mantiene la misma posición en X e intenta moverla una posición hacia abajo
                
            if self.valid(test):  # Verifica si la nueva posición es válida
                self.current.y += 1 # Baja la pieza actual
            else:
                self.lock_piece() # Fija la pieza si ya no puede bajar

    # Mueve la pieza actual una posición a la izquierda
    def move_left(self):
        t = self.current # Referencia a la pieza actual
        # Creamos una copia de la pieza para probar el movimiento
        test = Tetromino(t.key) 
        test.shape = [r[:] for r in t.shape] # Copiamos la forma
        test.color = t.color                 # Copiamos el color
        test.x, test.y = t.x - 1, t.y        # Intentamos moverla a la izquierda

        # Solo movemos la pieza real si la posición es válida
        if self.valid(test):
            t.x -= 1

    # Mueve la pieza actual una posición a la derecha
    def move_right(self):
        t = self.current                     # Referencia a la pieza actual
        # Creamos una copia para probar el movimiento
        test = Tetromino(t.key)
        test.shape = [r[:] for r in t.shape]
        test.color = t.color
        test.x, test.y = t.x + 1, t.y        # Intentamos moverla a la derecha

        # Si no hay colisión ni se sale del tablero, aplicamos el movimiento
        if self.valid(test):
            t.x += 1

    # Rota la pieza actual 90 grados
    def rotate(self):
        # Generamos una copia rotada de la pieza actual
        rot = self.current.rotated()

        # Caso 1: la rotación es válida en la misma posición
        if self.valid(rot):
            self.current = rot
        else:
            # Caso 2: intentamos ajustar la pieza a la izquierda
            rot.x -= 1
            if self.valid(rot):
                self.current = rot
            else:
                # Caso 3: intentamos moverla a la derecha
                rot.x += 2
                if self.valid(rot):
                    self.current = rot
    # Si ninguna opción funciona, no rota (se queda igual)

    def get_ghost(self):
        """
        Calcula la posición final donde caería la pieza actual (ghost piece).
        NO modifica la pieza real.
        """

        # Crear copia de la pieza actual
        ghost = Tetromino(self.current.key)
        ghost.shape = [r[:] for r in self.current.shape]
        ghost.color = self.current.color
        ghost.x = self.current.x
        ghost.y = self.current.y

        # Bajamos la pieza hasta que choque
        while True:
            test = Tetromino(ghost.key)
            test.shape = [r[:] for r in ghost.shape]
            test.color = ghost.color
            test.x = ghost.x
            test.y = ghost.y + 1  # probar una posición abajo
            
            if self.valid(test):
                ghost.y += 1  # sí puede bajar
            else:
                break  # ya no puede bajar más
        return ghost  # posición final válida

    # Controla las preguntas hechas por nivel completado
    def ask_math_question(self):
        """
        Muestra una pregunta matemática según el nivel actual
        y evalúa la respuesta del jugador.
        """

        # Nivel 1: suma
        if self.level == 1:
            oper = "+" # Operador suma
            a = random.randint(1, 9) # Primer número aleatorio
            b = random.randint(1, 9) # Segundo número aleatorio
            correct = a + b # Resultado correcto

        # Nivel 2: resta
        elif self.level == 2:
            oper = "-" # Operador resta
            a = random.randint(1, 9) # Primer número aleatorio
            b = random.randint(1, a) # Sustraendo (no mayor que a)
            correct = a - b # Resultado correcto

        # Nivel 3: multiplicación
        elif self.level == 3:
            oper = "x" # Operador multiplicación
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            correct = a * b # Resultado correcto
        
        # Nivel 4: división exacta
        elif self.level == 4:
            oper = "/" # Operador división
            b = random.randint(1, 9)     # Divisor
            c = random.randint(1, 9)     # Resultado esperado
            # Para asegurar que la división salga exacta (sin decimales),
            # se calcula el dividendo multiplicando divisor * resultado.
            # Así, a / b siempre dará exactamente c
            a = b * c
            # Esta es la respuesta correcta que el jugador debe escribir                 
            correct = c                  # a / b = c

        # Regresamos los datos
        return a, b, oper, correct
    
    # Falta pantallas de preguntas, victoria, game over y juego terminado
    # Funciones faltantes del código original: check_level_progress()
    # draw() y loop(), no funcionan 

def main(page: ft.Page):

    page.title = "Tetris Educativo" # Título de la ventana
    page.bgcolor = "black"
    page.window.width = WIDTH       # Ancho de ventana
    page.window.height = HEIGHT     # Alto de ventana
    page.window.resizable = False   # Evita que se redimensione
    page.assets_dir = "assets"
    page.fonts = {"Fuente": "Pixelmania.ttf"}

    musica_fondo = fta.Audio(
        src="musica.mp3",
        autoplay=True,         
        volume=0.5,            
        release_mode=fta.ReleaseMode.LOOP 
    )
    
    page.services.append(musica_fondo)

    game = Game()

    # Reinicia el juego desde el nivel indicado
    def start_game(level=1):
        game.reset_game(level)
        build_game_ui()
        page.update()

    # Decide qué pantalla mostrar al responder correctamente
    def handle_correct():
        if game.level >= 4:
            show_game_complete_screen(
                page,
                on_menu=lambda: show_main_menu(page, lambda: start_game(1))
            )
        else:
            show_victory_screen(
                page, game,
                on_continue=lambda: start_game(game.level + 1)
            )

    # Construye la interfaz del juego
    def build_game_ui():
        grid_ui = create_grid()

        # PANEL SUPERIOR (HEADER)
        # Configuración de la mini vista previa (siguiente pieza)
        PREVIEW_CELL = 14       # Tamaño de cada celda en preview
        PREVIEW_COLS = 4        # Columnas del preview
        PREVIEW_ROWS = 4        # Filas del preview
        preview_cells = []      # Matriz visual del preview
        
        for pr in range(PREVIEW_ROWS):
            preview_row = []
            for pc in range(PREVIEW_COLS):
                # Celda interna (el color real)
                pcell = ft.Container(
                    width=PREVIEW_CELL - 1,
                    height=PREVIEW_CELL - 1,
                    bgcolor=BLACK,
                    border_radius=2,
                )

                # Wrapper para centrar y dar espacio
                preview_row.append(
                    ft.Container(
                        width=PREVIEW_CELL,
                        height=PREVIEW_CELL,
                        content=pcell,
                        alignment=ft.alignment.Alignment(0, 0),
                        )
                    )
            preview_cells.append(ft.Row(preview_row, spacing=0))
        
        preview_grid = ft.Column(preview_cells, spacing=0)  # Grid completo del preview
            
        # Textos dinámicos (se actualizan en tiempo real)
        score_value = ft.Text("0", size=18, color=YELLOW, weight="bold", font_family="Fuente")
        level_value = ft.Text("1", size=18, color=YELLOW, weight="bold", font_family="Fuente")
            
        # Etiquetas pequeñas
        lbl_score = ft.Text("PUNTAJE", size=8, color="#aaaaaa", font_family="Fuente")
        lbl_level = ft.Text("NIVEL", size=8, color="#aaaaaa", font_family="Fuente")
        lbl_next  = ft.Text("SIGUIENTE", size=7, color="#aaaaaa", font_family="Fuente")
            
        # Sección de puntaje
        sec_score = ft.Container(
            expand=True,
            content=ft.Column(
                [lbl_score, score_value],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                ),
            )
            
        # Línea divisora vertical
        def vline():
            return ft.Container(width=1, height=52, bgcolor="#333333")

        # Sección de nivel
        sec_level = ft.Container(
            expand=True,
            content=ft.Column(
                [lbl_level, level_value],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                ),
            )
        
        # Sección de siguiente pieza
        sec_next = ft.Container(
            expand=True,
            content=ft.Column(
                [
                    lbl_next,
                    ft.Container(
                        content=preview_grid,
                        width=PREVIEW_COLS * PREVIEW_CELL,   # ancho exacto
                        height=PREVIEW_ROWS * PREVIEW_CELL,  # alto exacto
                        alignment=ft.alignment.Alignment(0, 0),  # centra el grid
                        bgcolor="#1a1a1a",
                        border_radius=4,
                        padding=0,  # quita padding para que no se vea corrido
                        ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,  #  centra verticalmente también
                spacing=4,
            ),
        )

        # Contenedor principal del header (barra superior)
        header = ft.Container(
            width=WIDTH,
            height=79,
            bgcolor="#111111",
            border=ft.Border(bottom=ft.BorderSide(2, "#333333")),
            padding=ft.Padding.symmetric(horizontal=8, vertical=6),
            content=ft.Row(
                [sec_score, vline(), sec_level, vline(), sec_next],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
        )

    # Actualiza la mini vista previa con la siguiente pieza
        def update_preview():
            # Limpiar preview
            for pr in range(PREVIEW_ROWS):
                for pc in range(PREVIEW_COLS):
                    preview_cells[pr].controls[pc].content.bgcolor = BLACK

            nxt = game.next_piece
            shape = nxt.shape
            color = nxt.color

            # Centrar la pieza
            start_r = (PREVIEW_ROWS - len(shape)) // 2
            start_c = (PREVIEW_COLS - len(shape[0])) // 2

            # Dibujar pieza
            for r, row in enumerate(shape):
                for c, v in enumerate(row):
                    if v:
                        preview_cells[start_r + r].controls[start_c + c].content.bgcolor = color

        def render():
            # Limpiar el tablero
            for r in range(GRID_ROWS):
                for c in range(GRID_COLS):
                    cell = grid_ui.controls[r].controls[c].content
                    cell.bgcolor = BLACK
                    cell.border = None
            #Dibujar piezas fijas
            for r in range(GRID_ROWS):
                for c in range(GRID_COLS):
                    if game.grid[r][c] is not None:
                        draw_block(grid_ui, r, c, game.grid[r][c])

            #Dibujar ghost (ANTES de la pieza real)
            ghost = game.get_ghost()
            draw_ghost(grid_ui, ghost.shape, ghost.x, ghost.y, game.current.color)

            #Dibuja la pieza actual encima del ghost
            draw_tetromino(grid_ui, game.current.shape,
                           game.current.x, game.current.y, game.current.color)
            
            # Actualizar datos del header
            score_value.value = str(game.score)
            level_value.value = str(game.level)
            update_preview()

        def on_left():
            if not game.paused: game.move_left();  render(); page.update()
        def on_right():
            if not game.paused: game.move_right(); render(); page.update()
        def on_down():
            if not game.paused: game.soft_drop();  render(); page.update()
        def on_rotate():
            if not game.paused:game.rotate();     render(); page.update()
        def on_drop():
            if not game.paused: game.hard_drop();  render(); page.update()
        def manejo_teclado(e: ft.KeyboardEvent):
            if e.key == "Escape":
                toggle_game_pause()
                return

            if not game.paused:
                if e.key == "Arrow Left": on_left()
                elif e.key == "Arrow Right": on_right()
                elif e.key == "Arrow Down": on_down()
                elif e.key == "Arrow Up": on_rotate()
                elif e.key == " ": on_drop()
            
            page.update()

        page.on_keyboard_event = manejo_teclado

        # Contenedor del tablero
        board = ft.Container(
            content=grid_ui,     # Contenido: el grid
            width=GRID_PX_W,     # ancho total
            height=GRID_PX_H,    # alto total
            bgcolor="#2e2e2d",   # fondo gris oscuro
            margin=ft.Margin.only(bottom=10) # espacio abajo
        )

        def boton_redondo(texto, on_click, size=40, color=YELLOW):
            return ft.Container(
                width=size, height=size,
                bgcolor=color,
                border_radius=size / 2,
                alignment=ft.Alignment(0, 0),
                content=ft.Text(texto, color="white", size=25, weight="bold"),
                on_click=on_click
            )
        
        btn_izq   = boton_redondo("◀", lambda e: on_left())
        btn_der   = boton_redondo("▶", lambda e: on_right())
        btn_abajo = boton_redondo("▼", lambda e: on_down())
        btn_rotar = boton_redondo("⟳", lambda e: on_rotate())
        # Botón grande y clickeable DROP
        btn_drop  = ft.GestureDetector(
            content=ft.Text("DROP", size=16, weight="w900",
                            color="RED", font_family="Fuente"),
            on_tap=lambda e: on_drop()
        )

        centro = ft.Container(width=30, height=30)
        def toggle_game_pause(e=None):
            game.paused = not game.paused
            # Cambiamos el texto del botón en lugar del icono
            btn_pausa.content.value = "▶" if game.paused else "||"
            page.update()

        btn_pausa = ft.Container(
            content=ft.Text("||", size=20, weight="bold", color=YELLOW), # Texto en vez de icono
            on_click=toggle_game_pause,
            bgcolor="#222222",
            padding=5,
            border_radius=5
        )

        dpad = ft.Column(
            [
                ft.Row([btn_rotar], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([btn_izq, centro, btn_der], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([btn_abajo], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        page.controls.clear()
        page.add(
            ft.Column(
                [
                    header,  # Barra superior (puntaje, nivel, siguiente pieza)
                    ft.Stack(
                        [
                        ft.Container(content=board, alignment=ft.alignment.Alignment(0, -0.5)),
                        # Botón de Pausa
                        ft.Container(
                                content=btn_pausa, 
                                left=20,  # A la izquierda
                                top=10    # Justo debajo del header
                            ),
                        # d-pad: abajo a la IZQUIERDA
                        ft.Container(content=dpad, left=50, bottom=1), # pegado a la izquierda y al fondo
                        # drop: abajo a la DERECHA
                        ft.Container(content=btn_drop, right=60, bottom=60), # pegado a la derecha y al fondo
                    ],
                    expand=True
                    )
                ],
                spacing=0,
                expand=True
                )
                )
        page.update() # Actualiza la interfaz

        # Loop principal del juego
        async def game_loop():
            while True:
                await asyncio.sleep(0.05) #Espera 50ms antes de cada actualizacion

                # Si las piezas llegaron arriba muestra game over
                if game.game_over:
                    show_game_over_screen(
                        page,
                        on_retry=lambda: start_game(game.level), # Reinicia el mismo nivel
                        on_menu=lambda: show_main_menu(page, lambda: start_game(1)) # Vuelve al menu
                    )
                    break #Sale del loop

                #Si jugador completo las lineas necesarias, muestra la pregunta
                if game.level_complete:
                    game.level_complete = False 
                    show_question_screen(
                        page, game,
                        on_correct=handle_correct, #Si responde bien pasa al siguiente nivel
                        on_wrong=lambda: show_game_over_screen(
                            page,
                            on_retry=lambda: start_game(game.level),
                            on_menu=lambda: show_main_menu(page, lambda: start_game(1))
                        )
                    )
                    break

                if not getattr(game, "paused", False):
                    game.update(50)
                    render() #Redibuja el tablero
                    page.update()

        page.run_task(game_loop)
        update_preview()  # fuerza actualización inmediata del mini tablero
        render()
        page.update()

    # Inicia la app mostrando el menú principal
    show_main_menu(page, on_start=lambda: start_game(1))


ft.app(target=main) # Ejecuta la app
