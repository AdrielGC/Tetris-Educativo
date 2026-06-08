# PROYECTO TETRIS EDUCATIVO

## Equipo de desarrollo

Adriel González Carmona - 010211972 (SCRUM MASTER)
Román Gutiérrez Guillén - 010211992 (DEVELOPER)
Azul Fernanda Soto Terán - 010212224 (DEVELOPER)
Leslie Berenice Plata Hernández - 190219329 (TESTER Y DEVELOPER)
Lizbeth Carmona Orea - 010212016 (DESIGNER)

## Información general

**Nombre del proyecto:** Tetris Educativo con preguntas matemáticas  
**Tipo de proyecto:** Videojuego educativo 2D multiplataforma  
**Lenguaje principal:** Python  
**Framework actual:** Flet (Basado en Flutter)

Este proyecto es la evolución del videojuego tipo Tetris original, migrado de PyGame a **Flet** para permitir su ejecución nativa en Android y Windows. Integra las mecánicas clásicas del juego con un sistema de preguntas matemáticas por niveles, reforzando el aprendizaje interactivo.

## Objetivo del proyecto

Desarrollar un videojuego educativo que combine entretenimiento y aprendizaje, permitiendo al usuario practicar habilidades matemáticas mientras avanza en los niveles del juego de forma fluida en dispositivos móviles y de escritorio.

### Objetivos específicos
- Implementar las reglas básicas del juego Tetris con una arquitectura moderna.
- Integrar un sistema de niveles progresivos y desafíos matemáticos.
- Diseñar una interfaz gráfica intuitiva, táctil y multiplataforma.
- Optimizar el rendimiento mediante el motor de renderizado de Flutter.

## Descripción del funcionamiento

- El jugador controla piezas que caen desde la parte superior del tablero.
- Al completar un número determinado de líneas, se incrementa la dificultad.
- Al cambiar de nivel, el juego presenta un desafío matemático.
- La respuesta correcta permite continuar; un error activa un flujo de recuperación o reintento.

## Tecnologías utilizadas

- **Python**
- **Flet** (Framework multiplataforma)
- **Flutter SDK** (Motor de compilación para Android)

## Estructura del proyecto
/Tetris-Flet
│
├── main.py              # Archivo principal de la aplicación
├── assets/              # Recursos visuales y sonoros
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto

## Instalación y ejecución

Asegurarse de tener Python 3.x instalado.

1. Instalar las dependencias ejecutando: `pip install -r requirements.txt`
2. Ejecutar el juego: `flet run main.py`
3. **Android:** Compilar el APK utilizando el comando: `flet build apk`

## Documentación del código

El código fuente utiliza:
- Estructura modular para facilitar el mantenimiento.
- Documentación técnica (Docstrings) en funciones clave.
- Integración nativa de componentes de Flet para la interfaz de usuario.

## Estado del proyecto

El proyecto ha sido migrado exitosamente a la versión Flet, cumpliendo con los objetivos académicos y extendiendo su compatibilidad a entornos móviles.

## Licencia

Este proyecto fue desarrollado con fines académicos.