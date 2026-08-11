# WatchGate Testbench Repository (`testing-test`)

Este repositorio existe como **banco de pruebas (testbench) multitecnología** para la evaluación y validación de **WatchGate**, un sistema automatizado de scoring de riesgo y revisión de Pull Requests en pipelines CI/CD.

El objetivo principal es disponer de proyectos de software reales y limpios en la rama principal (`main`) sobre los cuales abrir Pull Requests con diferentes comportamientos (benignos y maliciosos sintéticos) para analizar la tasa de detección y precisión de las 4 capas de WatchGate:

- **Capa Estática:** Detección de patrones peligrosos (Semgrep / YARA).
- **Capa de Dependencias:** Detección de vulnerabilidades, typosquatting y hooks maliciosos (OSV, npm/PyPI).
- **Capa de Reputación:** Verificación de la identidad e historial del autor del commit/PR.
- **Capa Semántica (LLM):** Inferencia de la intención real del cambio y detección de *backdoors* o exfiltraciones camufladas.

---

## 🗂️ Proyectos de Prueba Incluidos

El repositorio se organiza en proyectos independientes por juego y lenguaje:

| Proyecto | Lenguaje / Entorno | Descripción | Estado |
| :--- | :--- | :--- | :--- |
| [**Tetris Python**](./tetris-python/README.md) | Python 3 (curses / raw term) | Implementación de Tetris por terminal con UI ANSI |  Activo (`main`) |

---

## 🔄 Flujo de Trabajo con WatchGate

1. **Rama `main`:** Contiene la base de código limpia y legítima de los subproyectos.
2. **Ramas de prueba (`pr/...`):** Contienen cambios específicos destinados a probar escenarios de PRs (nuevas características benignas vs. parches maliciosos camuflados).
3. **CI/CD:** En cada PR abierta, la GitHub Action de WatchGate analiza el diff y emite un informe con el semáforo de riesgo (Verde / Amarillo / Rojo).
