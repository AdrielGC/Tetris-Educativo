import pygame # Librería que proporciona todo lo necesario para crear ventanas, dibujar, detectar el teclado/ratón

import sys # Librería que importa módulos estándar para interactuar con el sistema y ejecución del programa

import random # Librería estándar que genera números aleatorios, especificamente en este juego
# se usa para elegir piezas y para generar los números en las preguntas de matemáticas

"""
Configuración general del tamaño de la cuadricula
"""
WIDTH, HEIGHT = 600, 700  # Ancho y alto de la ventana
CELL_SIZE = 34 # Cada cuadrado del tablero
# row: fila, col: columna
GRID_COLS, GRID_ROWS = 10, 20 # Número de columnas y filas del tablero

"""
Tamaño de las celdas
"""
GRID_X = 10 # Distancia desde la izquierda de la ventana, donde comienza el tablero
GRID_Y = 10 # Distancia desde la parte superior donde empieza el tablero
GRID_PX_W = GRID_COLS * CELL_SIZE # Ancho del tablero 10 columnas * 34 px = 340 px
GRID_PX_H = GRID_ROWS * CELL_SIZE # Alto del tablero 20 columnas * 34 px = 680 px

PANEL_X = GRID_X + GRID_PX_W + 20  # Coordenada donde empieza el panel lateral (donde se muestra puntuaje y next piece)

"""
Colores que se ocupan en el juego.
Cada línea define una variable que contiene una tupla de 3 enteros (R,G,B)
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
SKY_BLUE = (125, 186, 230)
BLUE = (0, 0, 200)
YELLOW = (255, 215, 0)
DARK_BLUE = (0, 0, 30)
RED = (255, 69, 58)
GREEN = (0, 100, 0)

# Colores asignados a cada tipo de pieza
piece_colors = [
    (255, 0, 0), #Rojo     
    (0, 255, 128), #Verde    
    (255, 255, 0), #Amarillo    
    (255, 128, 0), #Naranja    
    (255, 20, 147), #Rosa   
    (148, 0, 211), #Violeta  
    (0, 255, 255), #Cyan 
]

"""
Formas de las piezas del Tetris
El número 1 representa un bloque visible
"""
#Formas de las figuras
Shapes = {
    "I": [[1,1,1,1]], # Pieza en forma de línea
    "O": [[1,1],      # Pieza cuadrada
          [1,1]],     
    "T": [[1,1,1],    # Pieza en forma de T
          [0,1,0]],
    "J": [[1,0,0],    # Pieza J
          [1,1,1]],
    "L": [[0,0,1],    # Pieza L
          [1,1,1]],
    "S": [[0,1,1],    # Pieza S
          [1,1,0]],
    "Z": [[1,1,0],    # Pieza Z
          [0,1,1]],
}

# Lista con las claves de las piezas para elegirlas aleatoriamente
# Convierte las claves del diccionario en una lista
SHAPE_KEYS = list(Shapes.keys())

"""
Inicialización de pygame y ventana principal
"""
pygame.init() # Inicializa pygame 
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana
pygame.display.set_caption("Tetris Educativo") # Asigna el título del juego

# Definición de las fuentes que se usarán
font_title = pygame.font.SysFont("cambria", 100, bold=True) # Fuente para el título
font_button = pygame.font.SysFont("cambria", 30) # Fuente para botones
font_small  = pygame.font.SysFont("cambria", 24) # Fuente pequeña
font_big    = pygame.font.SysFont("cambria", 60, bold=True) # Fuente grande

"""
Definición de botones del menú principal
"""
play_button = pygame.Rect(250, 300, 100, 50) # Botón jugar
info_button = pygame.Rect(215, 375, 190, 50) # Botón instrucciones
exit_button = pygame.Rect(250, 450, 100, 50) # Botón salir
back_button = pygame.Rect(490, 630, 90, 50)  # Botón regresar al menú


"""
Cierra el juego correctamente
"""
def exit_game():
    pygame.quit() # Cierra pygame
    sys.exit() # Finaliza el programa


"""
Dibuja el fondo cuadriculado del menú
"""
def draw_menu_grid():
    for y in range(0, HEIGHT, CELL_SIZE): # Recorre filas
        for x in range(0, WIDTH, CELL_SIZE): # Recorre columnas
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE) # Crea cada celda
            pygame.draw.rect(screen, BLACK, rect) # Dibuja fondo negro       
            pygame.draw.rect(screen, GRAY, rect, 1) # Dibuja el borde gris


"""
Dibuja la cuadrícula del tablero de juego
"""
def draw_game_grid():
    grid_width = GRID_COLS * CELL_SIZE # Calcula el ancho total del tablero en píxeles
    grid_height = GRID_ROWS * CELL_SIZE # Calcula el alto total del tablero en píxeles
    start_x = 10 # Posición inicial del tablero en el eje X
    start_y = 10 # Posición inicial del tablero en el eje  Y

    for row in range(GRID_ROWS): # Recorre filas
        for col in range(GRID_COLS): # Recorre columnas
            rect = pygame.Rect(start_x + col * CELL_SIZE, # Calcula la posición X de la celda
                               start_y + row * CELL_SIZE, # Calcula la posición Y de la celda
                               CELL_SIZE, CELL_SIZE) # Ancho y alto de la celda
            pygame.draw.rect(screen, BLACK, rect) # Dibuja el fondo negro de la celda
            pygame.draw.rect(screen, GRAY, rect, 1) # Dibuja el borde gris de la celda


"""
Dibuja un bloque individual
"""
def draw_block(px, py, color):
    rect = pygame.Rect(px, py, CELL_SIZE, CELL_SIZE) # Crea el rectángulo del bloque
    pygame.draw.rect(screen, color, rect) # Dibuja el bloque con el color recibido
    pygame.draw.rect(screen, (20, 20, 20), rect, 2) # Dibuja un borde oscuro para dar efecto


""" 
Nos ayudará a crear una pieza completa en pantalla 
"""
def draw_tetromino(shape, gx, gy, color):
    for r, row in enumerate(shape):  # Recorre las filas de la forma de la pieza
        for c, v in enumerate(row):  # Recorre las columnas de la forma
            if v: # Si el valor es 1, significa que ahí va un bloque
                x = (gx + c) * CELL_SIZE # Calcula la posición X del bloque
                y = (gy + r) * CELL_SIZE # Calcula la posición Y del bloque
                draw_block(x, y, color) # Dibuja el bloque en pantalla

def _ui_safe_start_row():
    safe_px = exit_button.bottom + 16  # Calcula un espacio seguro debajo del botón salir
    return max(0, safe_px // CELL_SIZE) # Regresa la fila segura en formato de cuadrícula


"""
Rota una pieza 90 grados
"""
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])] # Algoritmo que rota la matriz de la pieza


"""
Nos permite que la pieza se pueda girar varias veces
"""
def rot(shape, times=1):
    out = shape # Guarda la forma original
    for _ in range(times % 4): # Limita las rotaciones a un máximo de 4
        out = rotate_shape(out) # Aplica la rotación
    return out # Regresa la forma rotada


"""
Piezas decorativas que aparecen en el menú principal
"""
def draw_static_showcase():
    grid_w = WIDTH // CELL_SIZE # Calcula el ancho de la pantalla en celdas
    grid_h = HEIGHT // CELL_SIZE # Calcula el alto de la pantalla en celdas

    pile_top = max(_ui_safe_start_row(), grid_h - 8) # Define la altura base de las piezas
    base_y = max(0, pile_top - 5) # Ajusta la base para que no se salga de pantalla
    I_vert = rotate_shape(Shapes["I"]) # Rota la pieza I verticalmente
    L_vert = rotate_shape(Shapes["L"]) # Rota la pieza L verticalmente

    placements = [ # Lista de piezas con su posición y color
        (I_vert, 8, 4, (255, 0, 0)), 
        (Shapes["T"], 4, 11, (255, 255, 0)), 
        (L_vert, 12, 10, (255, 20, 147)),
        (rot(Shapes["J"], 3), 0, 17, (255, 128, 0)),
        (rot(Shapes["T"], 2), 2, 18, (255, 255, 0)),
        (Shapes["I"], 5, 19, (255, 0, 0)),
        (Shapes["S"], 6, 17, (148, 0, 211)),
        (Shapes["O"], 9, 18, (0, 255, 128)),
        (Shapes["Z"], 11, 18, (0, 255, 255)),
        (L_vert, 14, 17, (255, 20, 147)),
        (Shapes["O"], 16, 18, (0, 255, 128)),
        (Shapes["O"], 15, 13, (0, 255, 128)),
    ]

    for shape, gx, gy, color in placements: # Recorre cada pieza decorativa
        if gy + len(shape) <= grid_h:  # Verifica que no se salga de la pantalla
            draw_tetromino(shape, gx, gy, color) # Dibuja la pieza


"""
Nos ayuda a dibujar la pantalla principal 
"""
def draw_start_screen():
    draw_menu_grid() # Dibuja el fondo del menú
    draw_static_showcase() # Dibuja las piezas decorativas

    title_surface = font_title.render("TETRIS", True, SKY_BLUE) # Crea el texto del título
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 150)) # Centra el título
    border_rect = title_rect.inflate(6, 6) # Crea un borde alrededor del título
    pygame.draw.rect(screen, BLACK, border_rect) # Dibuja el borde
    screen.blit(title_surface, title_rect) # Muestra el título en pantalla

    pygame.draw.rect(screen, YELLOW, play_button) # Dibuja el botón jugar
    pygame.draw.rect(screen, BLACK, play_button, 2) # Dibuja el borde del botón
    play_text = font_button.render("Jugar", True, BLACK) # Texto del botón
    screen.blit(play_text, (play_button.x + 20, play_button.y + 10))# Muestra el texto

    pygame.draw.rect(screen, YELLOW, info_button) # Dibuja el botón instrucciones
    pygame.draw.rect(screen, BLACK, info_button, 2) # Borde del botón
    info_text = font_button.render("Instrucciones ", True, BLACK) # Texto del botón
    screen.blit(info_text, (info_button.x + 5, info_button.y + 10)) # Muestra el texto

    pygame.draw.rect(screen, YELLOW, exit_button) # Dibuja el botón salir
    pygame.draw.rect(screen, BLACK, exit_button, 2) # Borde del botón
    exit_text = font_button.render("Salir", True, BLACK) # Texto del botón
    screen.blit(exit_text, (exit_button.x + 25, exit_button.y + 10)) # Muestra el texto

    pygame.display.flip() # Actualiza la pantalla


"""
Crea la página de las instrucciones 
"""
def show_instructions():
    draw_menu_grid() # Dibuja el fondo del menú
    lines = [ # Lista con todas las líneas del texto de instrucciones
        "                        INSTRUCCIONES",
        "Como jugar:",
        "1. Las piezas van a empezar a caer",
        "2. Tendras que acomodarlas",
        "Controles:",
        "1.Presiona la flecha hacia la izquierda de",
        "tu teclado y se movera a la izquierda", 
        "2.Presiona la flecha hacia la derecha de",
        "tu teclado y se movera a la derecha", 
        "3.Presiona la flecha hacia abajo de",
        "tu teclado y bajara más rapido", 
        "4.Presiona la flecha hacia arriba de tu teclado",
        "y rotara la pieza", 
        "Niveles y preguntas:",
        "1.Cada que subas de nivel aparacerá",
        "una pregunta",
        "2.Si respondes bien sigues jugando",
        "3.Si fallas vuelves a intentarlo"
    ]
    for i, line in enumerate(lines): # Recorre cada línea de texto
        text = font_button.render(line, True, WHITE) # Renderiza el texto
        screen.blit(text, (4, 35 + i * 36)) # Dibuja el texto con separación
    pygame.draw.rect(screen, YELLOW, back_button) # Dibuja el botón menú
    pygame.draw.rect(screen, BLACK, back_button, 2) # Borde del botón
    back_text = font_button.render("Menú", True, BLACK) # Texto del botón
    screen.blit(back_text, (back_button.x + 10, back_button.y + 10)) # Muestra el texto

    pygame.display.flip() # Actualiza la pantalla

    waiting = True # Controla la espera en esta pantalla
    while waiting:
        for event in pygame.event.get():  # Revisa los eventos
            if event.type == pygame.QUIT: # Si se cierra la ventana
                exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN: # Si se da click
                if back_button.collidepoint(event.pos): # Si se presiona menú
                    waiting = False # Regresa al menú principal


"""
Inicia la pantalla del juego
"""
def start_game(): 
    running = True # Controla el ciclo del juego
    while running:
        screen.fill(DARK_BLUE) # Limpia la pantalla
        draw_game_grid() # Dibuja el tablero

        for event in pygame.event.get(): # Revisa los eventos
            if event.type == pygame.QUIT: # Si se cierra la ventana
                exit_game()
            elif event.type == pygame.KEYDOWN: # Si se presiona una tecla
                if event.key == pygame.K_ESCAPE: # Si se presiona ESC
                    running = False # Sale del juego

        pygame.display.flip() # Actualiza la pantalla


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
        self.color = piece_colors[SHAPE_KEYS.index(key)] # Asigna el color correspondiente
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
        self.clock = pygame.time.Clock() # Control del tiempo y FPS
        self.level = 1 # Nivel inicial
        self.lines_cleared = 0 #Lineas eliminadas
        self.lines_for_level = 1 # Lineas necesarias para pasar de nivel
        self.base_speed = 650 # Velocidad base de caída
        self.fall_interval_ms = self.base_speed # Intervalo de caída

        self.exit_program = False # Indica si se debe cerrar el juego
        self.end_to_menu = False # Indica si se regresa al menú

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

        # Velocidad base por nivel: cada nivel reduce el intervalo de caída para que las piezas bajen más rápido
        self.fall_interval_ms = self.base_speed - (self.level - 1) * 150
        
        # En el nivel 4 para agregar un extra de velocidad para agregarle más dificultad,
        # se le restan algunos milisegundos adicionales
        if self.level == 4:
            self.fall_interval_ms -= 80  
        
        # Aseguramos que el intervalo nunca baje de 130 ms, porque si es menos
        # el juego se vuelve demasiado rápido y prácticamente injugable
        self.fall_interval_ms = max(130, self.fall_interval_ms) 

    #Verifica si la pieza esta dentro del tablero, aparte verifica si se puede seguir creando piezas
    def valid(self, t):
        """
        Comprueba si una pieza puede colocarse en el tablero.
        Verifica límites del tablero y colisiones con piezas ya fijadas.
        """
        for r, row in enumerate(t.shape): # Recorre las filas de la forma
            for c, v in enumerate(row): # Recorre las columnas
                if not v: # Si no hay bloque, se ignora
                    continue
                gx, gy = t.x + c, t.y + r # Calcula posición real en la cuadrícula
                if gx < 0 or gx >= GRID_COLS or gy >= GRID_ROWS: # Fuera del tablero
                    return False
                if gy >= 0 and self.grid[gy][gx] is not None: # Colisión con otra pieza
                    return False 
        return True # La posición es válida

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
            self.check_level_progress()
            return

        self.current = self.next_piece # Actualiza la pieza actual
        self.next_piece = Tetromino() # Genera la siguiente
        if not self.valid(self.current): # Si no puede colocarse
            self.game_over = True 

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
        Baja la pieza una posición cuando el jugador presiona la flecha abajo.
        """
        test = Tetromino(self.current.key) # Crea una copia de la pieza
        test.shape = [row[:] for row in self.current.shape]
        test.color = self.current.color
        test.x, test.y = self.current.x, self.current.y + 1

        if self.valid(test): # Si la posición es válida
            self.current.y += 1   # Baja la pieza
        else:
            self.lock_piece()  # Fija la pieza

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

    #Controla la entrada desde el teclado
    def handle_input(self, event):
        """
        Detecta y procesa las teclas presionadas por el jugador.
        """
        if event.type != pygame.KEYDOWN:  # Si no es una tecla presionada
            return # No hace nada
        t = self.current # Referencia a la pieza actual

        #Tecla de flecha hacia la izquierda
        if event.key == pygame.K_LEFT: # Flecha izquierda
            test = Tetromino(t.key)  # Crea una copia de la pieza
            test.shape = [r[:] for r in t.shape] # Copia la forma
            test.color = t.color # Copia el color
            test.x, test.y = t.x - 1, t.y # Intenta mover a la izquierda
            if self.valid(test): # Si el movimiento es válido
                t.x -= 1  # Mueve la pieza real
                
        #Tecla de flecha hacia la derecha
        elif event.key == pygame.K_RIGHT:
            test = Tetromino(t.key)
            test.shape = [r[:] for r in t.shape]
            test.color = t.color
            test.x, test.y = t.x + 1, t.y # Intenta mover a la derecha
            if self.valid(test):
                t.x += 1
        #Tecla de flecha hacia abajo
        elif event.key == pygame.K_DOWN: 
            self.soft_drop() # Baja la pieza manualmente

        #Tecla de flecha hacia arriba
        elif event.key == pygame.K_UP:
            rot = t.rotated() # Intenta rotar la pieza
            if self.valid(rot): # Si la rotación es válida
                self.current = rot # Aplica la rotación
            else:
                rot.x -= 1 # Intenta mover a la izquierda
                if self.valid(rot):
                    self.current = rot
                else:
                    rot.x += 2  # Intenta mover a la derecha
                    if self.valid(rot):
                        self.current = rot

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

        # Permite la entrada de la respuesta por el usuario
        user_answer = ""

        while True:
            for event in pygame.event.get(): # Procesa eventos
                if event.type == pygame.QUIT: 
                    return "quit" # Sale del juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: # Verifica que haya algo escrito
                        if user_answer != "": 
                            try:
                                ans = int(user_answer) # Convierte a entero
                            except:
                                ans = None
                            if ans == correct:
                                return "correct" # Respuesta correcta
                            else:
                                return "wrong" # Respuesta incorrecta
                    elif event.key == pygame.K_BACKSPACE:
                        user_answer = user_answer[:-1] # Borra último dígito
                    else:
                        if event.unicode.isdigit() and len(user_answer) < 3:
                            user_answer += event.unicode # Agrega dígito
            # Crea la pantalla para hacer la pregunta
            screen.fill(BLUE)  # Limpia la pantalla con color azul
            t1 = font_button.render("¡¡Felicidades pasaste de nivel!!", True, WHITE)
            t2 = font_small.render("Ahora para continuar contesta la siguiente pregunta", True, WHITE)
            q  = font_button.render(f"¿Cuánto es {a} {oper} {b}?", True, WHITE)

            # Dibuja los textos centrados
            screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 100)) 
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 150))
            screen.blit(q,  (WIDTH//2 - q.get_width()//2, 230))

            box = pygame.Rect(WIDTH//2 - 150, 340, 300, 60)  # Crea el rectángulo de la caja de respuesta
            pygame.draw.rect(screen, WHITE, box) # Dibuja la caja blanca
            pygame.draw.rect(screen, BLACK, box, 2) 

            resp = font_small.render("Respuesta:", True, BLACK) # Texto "Respuesta:"
            screen.blit(resp, (box.x + 10, box.y + 10))

            txt = font_small.render(user_answer, True, BLACK) # Texto con lo que el usuario escribe
            screen.blit(txt, (box.x + 125, box.y + 10))

            pygame.display.flip() # Actualiza la pantalla
            self.clock.tick(30) # Controla la velocidad del ciclo

    def level_failed_screen(self):
        """
        Muestra la pantalla cuando el jugador falla una pregunta.
        """
        retry_rect = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 50) # Rectángulo del botón "Reintentar"
        menu_rect  = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50) # Rectángulo del botón "Menú principal"
        
        # Ciclo que mantiene activa la pantalla hasta que el jugador elija una opción
        while True:
            for event in pygame.event.get(): # Captura eventos del sistema
                if event.type == pygame.QUIT:  # Si se cierra la ventana del juego
                    return "quir" # Indica salida del juego
                if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic con el mouse
                    if retry_rect.collidepoint(event.pos): # Si se hace clic en "Reintentar"
                        return "retry" # Indica que se reinicia el nivel
                    if menu_rect.collidepoint(event.pos): # Si se hace clic en "Menú principal"
                        return "menu" # Regresa al menú principal

            screen.fill(RED) # Limpia la pantalla con color rojo
            # Textos informativos
            t1 = font_big.render("¡¡Casi!!", True, WHITE)
            t2 = font_big.render("Intenta otra vez", True, WHITE)
            t3 = font_small.render(f"Puntaje: {self.score}", True, WHITE)
            
            # Dibuja los textos centrados
            screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 160))
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 230))
            screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 320))

            # Dibuja el botón "Reintentar"
            pygame.draw.rect(screen, YELLOW, retry_rect)
            pygame.draw.rect(screen, BLACK, retry_rect, 2)
            txt1 = font_small.render("Reintentar", True, BLACK)
            screen.blit(txt1, txt1.get_rect(center=retry_rect.center))

            # Dibuja el botón "Menú principal"
            pygame.draw.rect(screen, YELLOW, menu_rect)
            pygame.draw.rect(screen, BLACK, menu_rect, 2)
            txt2 = font_small.render("Menú principal", True, BLACK)
            screen.blit(txt2, txt2.get_rect(center=menu_rect.center))

            pygame.display.flip() # Actualiza la pantalla
            self.clock.tick(30) # Controla la velocidad del bucle
            
    def level_success_screen(self):
        """
        Muestra la pantalla cuando el jugador responde correctamente.
        """
        next_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 40, 240, 50) # Botón para avanzar al siguiente nivel
        menu_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 110, 200, 50) # Botón para regresar al menú principal

        # Mantiene la pantalla activa hasta que el jugador elija una opción
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Si se cierra la ventana
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic con el mouse
                    if next_rect.collidepoint(event.pos): # Si se presiona "Siguiente nivel"
                        return "next"
                    if menu_rect.collidepoint(event.pos): # Si se presiona "Menú principal"
                        return "menu"
            
            # Limpia la pantalla con color verde
            screen.fill(GREEN)
            # Textos informativos
            t1 = font_big.render("¡¡Correcto!!", True, WHITE)
            t2 = font_big.render("Sigue así", True, WHITE)
            t3 = font_small.render(f"Puntaje: {self.score}", True, WHITE)
            t4 = font_small.render(f"Pasas al nivel {self.level + 1}", True, WHITE)

            # Dibuja los textos centrados
            screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 150))
            screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 210))
            screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 300))
            screen.blit(t4, (WIDTH//2 - t4.get_width()//2, 340))
            
            # Botón "Siguiente nivel"
            pygame.draw.rect(screen, YELLOW, next_rect)
            pygame.draw.rect(screen, BLACK, next_rect, 2)
            txt1 = font_small.render("Siguiente nivel", True, BLACK)
            screen.blit(txt1, txt1.get_rect(center=next_rect.center))
            
            # Botón "Menú principal"
            pygame.draw.rect(screen, YELLOW, menu_rect)
            pygame.draw.rect(screen, BLACK, menu_rect, 2)
            txt2 = font_small.render("Menú principal", True, BLACK)
            screen.blit(txt2, txt2.get_rect(center=menu_rect.center))

            pygame.display.flip() # Actualiza la pantalla
            self.clock.tick(30) # Controla la velocidad del bucle

    def final_screen(self):
        """
        Muestra la pantalla final cuando el jugador termina el juego.
        """
        menu_rect  = pygame.Rect(WIDTH//2 - 110, HEIGHT//2 + 80, 220, 50) # Botón para volver al menú
        quit_rect  = pygame.Rect(WIDTH//2 - 80, HEIGHT//2 + 160, 160, 50)  # Botón para salir del juego

        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # Si se cierra la ventana
                    return "quit" 
                if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic con el mouse
                    if menu_rect.collidepoint(event.pos): # Opción menú principal
                        return "menu"
                    if quit_rect.collidepoint(event.pos): # Opción salir del juego
                        return "quit"

            screen.fill(SKY_BLUE)  # Fondo azul claro

            # Mensajes finales
            txt1 = font_big.render("¡Felicidades!", True, DARK_BLUE)
            txt2 = font_big.render("¡Acabaste el juego!", True, DARK_BLUE)

            # Dibuja los textos
            screen.blit(txt1, (WIDTH//2 - txt1.get_width()//2, 100))
            screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 180))
            
            # Botón menú
            pygame.draw.rect(screen, YELLOW, menu_rect)
            pygame.draw.rect(screen, BLACK, menu_rect, 2)
            t2 = font_small.render("Menú principal", True, BLACK)
            screen.blit(t2, t2.get_rect(center=menu_rect.center))

            # Botón salir
            pygame.draw.rect(screen, YELLOW, quit_rect)
            pygame.draw.rect(screen, BLACK, quit_rect, 2)
            t3 = font_small.render("Salir", True, BLACK)
            screen.blit(t3, t3.get_rect(center=quit_rect.center))

            pygame.display.flip() # Actualiza la pantalla
            self.clock.tick(30) # Controla la velocidad del bucle

    def check_level_progress(self):
        """
        Controla el avance del jugador entre niveles.
        """
        result = self.ask_math_question() # Llama a la función que hace la pregunta matemática
        if result == "quit": # Si el jugador decide salir
            self.exit_program = True
            return
        if result == "wrong": # Si el jugador falla la pregunta
            action = self.level_failed_screen()
            if action == "quit":
                self.exit_program = True
            elif action == "menu":
                self.end_to_menu = True
            elif action == "retry":
                self.reset_game(1)
            return

        if self.level < 4: # Si el nivel actual no es el último
            action = self.level_success_screen()
            if action == "quit":
                self.exit_program = True
                return
            if action == "menu":
                self.end_to_menu = True
                return
            if action == "next":
                self.level += 1 # Avanza al siguiente nivel
                self.reset_game(self.level) # Reinicia el estado del juego
                return
        else: # Si ya es el nivel final
            action = self.final_screen()
            if action == "quit":
                self.exit_program = True
            elif action == "menu":
                self.end_to_menu = True
            elif action == "retry":
                self.reset_game(1)

    # Nos ayuda a crear la pantalla del juego completo
    def draw(self):
        """
        Dibuja todos los elementos del juego en pantalla.
        """
        screen.fill(DARK_BLUE) # Limpia la pantalla con color de fondo
        draw_game_grid() # Dibuja la cuadrícula del tablero

        for r in range(GRID_ROWS): # Recorre las filas del tablero
            for c in range(GRID_COLS): # Recorre las columnas
                color = self.grid[r][c] # Obtiene el color en esa posición
                if color is not None: # Si hay una pieza fija
                    draw_block(GRID_X + c * CELL_SIZE, GRID_Y + r * CELL_SIZE, color)

        for r, row in enumerate(self.current.shape): # Recorre la pieza actual
            for c, v in enumerate(row):
                if v and self.current.y + r >= 0: # Si hay bloque visible
                    draw_block(GRID_X + (self.current.x + c) * CELL_SIZE,
                               GRID_Y + (self.current.y + r) * CELL_SIZE,
                               self.current.color)

        pygame.draw.rect(screen, (15, 15, 15), (PANEL_X - 10, GRID_Y, 200, 260)) # Fondo del panel
        pygame.draw.rect(screen, GRAY, (PANEL_X - 10, GRID_Y, 200, 260), 2) # Borde del panel
        screen.blit(font_small.render(f"Puntaje: {self.score}", True, WHITE), (PANEL_X, GRID_Y + 10)) # Muestra el puntaje
        screen.blit(font_small.render(f"Nivel: {self.level}", True, WHITE),   (PANEL_X, GRID_Y + 30)) # Muestra el nivel
        screen.blit(font_small.render("S. pieza:", True, WHITE),              (PANEL_X, GRID_Y + 50)) # Texto de siguiente pieza

        for r, row in enumerate(self.next_piece.shape): # Dibuja la siguiente pieza
            for c, v in enumerate(row):
                if v:
                    draw_block(PANEL_X + c * CELL_SIZE, GRID_Y + 80 + r * CELL_SIZE, self.next_piece.color)

    #Se encarga de procesar todos los eventos que ocurren dentro del juego
    def loop(self):
        """
        Ejecuta el ciclo principal del juego.
        """
        self.exit_program = False  # Controla si se sale del juego
        self.end_to_menu = False   # Controla si se regresa al menú

        while not self.exit_program and not self.end_to_menu: 
            dt = self.clock.tick(60) # Controla los FPS y obtiene delta time
            for event in pygame.event.get(): # Recorre los eventos
                if event.type == pygame.QUIT:
                    self.exit_program = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.end_to_menu = True
                else:
                    self.handle_input(event) # Maneja el input del jugador

            if self.exit_program or self.end_to_menu: 
                break

            if self.game_over: # Si el juego terminó
                action = self.level_failed_screen()
                if action == "quit":
                    self.exit_program = True
                elif action == "menu":
                    self.end_to_menu = True
                elif action == "retry":
                    self.reset_game(1)
                self.game_over = False
                continue

            self.update(dt) # Actualiza la lógica del juego
            self.draw() # Dibuja todo en pantalla
            pygame.display.flip() # Actualiza la pantalla

        return not self.exit_program # Regresa si vuelve al menú

#Controla el menú principal
def start_menu():
    """
    Muestra el menú principal y gestiona la navegación
    entre jugar, ver instrucciones o salir del juego.
    """
    while True: # Bucle infinito para mantener activo el menú
        draw_start_screen() # Dibuja la pantalla inicial del menú
        for event in pygame.event.get(): # Recorre todos los eventos generados por el usuario
            if event.type == pygame.QUIT: # Si el usuario cierra la ventana del juego
                exit_game() # Finaliza el programa
            elif event.type == pygame.MOUSEBUTTONDOWN: # Si el usuario hace clic con el mouse
                if play_button.collidepoint(event.pos): # Si se presiona el botón "Jugar"
                    game = Game() # Se crea una nueva instancia del juego
                    back_to_menu = game.loop() # Se inicia el ciclo principal del juego
                    if not back_to_menu: # Si el juego indica que no se debe volver al menú
                        exit_game() # Se cierra el programa
                elif info_button.collidepoint(event.pos): # Si se presiona el botón "Instrucciones"
                    show_instructions() # Muestra la pantalla de instrucciones
                elif exit_button.collidepoint(event.pos): # Si se presiona el botón "Salir"
                    exit_game() # Cierra el juego completamente

start_menu() # Llama a la función del menú principal para iniciar el programa