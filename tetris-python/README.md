# Tetris Terminal (Python)

Una implementación limpia, modular y orientada a objetos de **Tetris para la terminal** escrita en Python puro.

Este subproyecto forma parte de la suite de pruebas para el análisis de código de **WatchGate**.

---

## 🚀 Requisitos

- Python 3.8 o superior.
- Terminal compatible con códigos de color ANSI (Linux, macOS, WSL/Windows Terminal).

---

## 🛠️ Instalación y Configuración

1. **Crear el entorno virtual:**

```bash
python3 -m venv .venv
```

2. **Activar el entorno virtual:**

   - En **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
   - En **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```

3. **Instalar dependencias de testing:**

```bash
pip install -r requirements.txt
```

---

## 🕹️ Cómo Jugar

Ejecuta el juego desde la raíz de `tetris-python/`:

```bash
python -m src.tetris
```

o invocando directamente el archivo `tetris.py`:

```bash
python src/tetris.py
```

### Controles de Teclado

| Tecla | Acción |
| :--- | :--- |
| `←` / `A` | Mover a la izquierda |
| `→` / `D` | Mover a la derecha |
| `↑` / `W` | Rotar pieza 90° |
| `↓` / `S` | Caída rápida (*Soft Drop*) |
| `Espacio` / `Enter` | Caída instantánea (*Hard Drop*) |
| `Q` | Salir del juego |

---

## 🧪 Ejecución de Tests

Para ejecutar la batería de pruebas unitarias con `pytest`:

```bash
pytest tests
```

---

## 💡 Futuras Mejoras y Casos de Uso para PRs

Esta lista de características sirve como hoja de ruta para implementar Pull Requests de prueba (tanto benignas como maliciosas camufladas) evaluadas por **WatchGate**:

1. **Guardar Pieza (*Hold Piece* - tecla `C` / `Shift`):**
   - Permitir al jugador reservar la pieza actual e intercambiarla previo uso.
2. **Soporte de Controles Expandido (Flechas + WASD + Vim `HJKL`):**
   - Mapear múltiples esquemas de teclado para mayor flexibilidad de juego.
3. **Pieza Fantasma (*Ghost Piece*):**
   - Proyección punteada/sombra en el fondo del tablero mostrando la posición exacta de caída.
4. **Persistencia de Puntuación Máxima (*High Score Leaderboard*):**
   - Guardado local de la mejor puntuación en un archivo (`scores.json`).
5. **Función de Pausa (`P` / `Esc`):**
   - Pausar el bucle de juego y ocultar temporalmente el tablero.
6. **Sistema de Combos y Multiplicadores *Back-to-Back*:**
   - Bonificaciones de puntuación por limpieza consecutiva de líneas o *Tetris* dobles.
7. **Selector de Nivel de Dificultad Inicial:**
   - Menú interactivo de selección de nivel de velocidad inicial (ej. Nivel 0 al 10).
8. **Modo Sprint (40 Líneas):**
   - Contrarreloj para limpiar 40 líneas en el menor tiempo posible.
9. **Feedback de Sonido ANSI (`\a` / Terminal Bell):**
   - Retroalimentación auditiva al limpiar filas, realizar *Hard Drop* o al *Game Over*.
