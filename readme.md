<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://img.shields.io/badge/License-MIT-green"/>
    <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white&color=blue" />
    <img src="https://img.shields.io/github/contributors/MrDeybby/FlowFree-SearchAgents"/>
    <img src="https://img.shields.io/github/last-commit/MrDeybby/FlowFree-SearchAgents"/>
  </a>
</p>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=github,py,vscode" />
  </a>
</p>

# FlowFree-SearchAgents

Este proyecto académico de la asignatura *Juegos Inteligentes* es una implementación del juego **Flow Free** en terminal, junto con agentes de búsqueda (BFS, DFS, USC, A*) en desarrollo para resolver los tableros. El sistema incluye un menú interactivo, selección de niveles y soporte para entrada por teclado.

## Contenido

- [Introducción](#introducción)  
- [Funcionalidades del proyecto](#Funcionalidades-del-proyecto)  
- [Requisitos previos](#requisitos-previos)  
- [Requisitos del sistema](#requisitos-del-sistema)  
- [Dependencias](#dependencias)  
- [Instalación](#instalación)  
- [Ejecución del juego](#ejecución-del-juego)  
- [Primer uso](#primer-uso)  
- [Flujo de navegación](#flujo-de-navegación)  
- [Solución de problemas](#solución-de-problemas)  
- [Integrantes y responsabilidades](#integrantes-y-responsabilidades)  
- [Convenciones de commits](#convenciones-de-commits)  
- [Licencia](#licencia)  

---

## Introducción

**FlowFree-SearchAgents** es una implementación del popular puzzle *Flow Free* en Python.  
El sistema incluye un motor de juego, un sistema de niveles y agentes de búsqueda que se desarrollarán en futuras versiones.  

---

## Funcionalidades del proyecto  

- Juego *Flow Free* jugable en consola.  
- Lectura de tableros desde archivos `.txt` con tamaño variable.  
- Implementación de tres algoritmos de búsqueda:  
  - Búsqueda en amplitud (**BFS**).  
  - Búsqueda en profundidad (**DFS**).  
  - Búsqueda **A\***.  
- Generación de métricas en `output.txt`:  
  - Ruta de la solución.  
  - Costo de la ruta.  
  - Nodos expandidos.  
  - Profundidad de la solución.  
  - Máxima profundidad de búsqueda.  
  - Tiempo de ejecución.  
  - Uso máximo de memoria RAM.  

---

---

## Requisitos previos

- Python 3.8 o superior  
- Entorno de terminal compatible con teclas de flechas 

---

## Requisitos del sistema

| Requisito        | Detalles                          |
|------------------|-----------------------------------|
| **Python**       | 3.7 o superior                   |
| **SO**           | Windows, macOS o Linux           |
| **Terminal**     | Compatible con códigos ANSI      |
| **Entrada**      | Teclado con soporte de flechas   |

---

## Dependencias

El proyecto utiliza una única dependencia externa para el manejo de entradas por teclado:  

```
keyboard==0.13.5
```

Archivo fuente: `requirements.txt`  

---

## Instalación

1. **Clonar repositorio**  

```bash
git clone https://github.com/MrDeybby/FlowFree-SearchAgents
cd FlowFree-SearchAgents
```

2. **Instalar dependencias**  

```bash
pip install -r requirements.txt
```

3. **Verificar instalación**  

Ir a la carpeta del juego y comprobar que el archivo de entrada existe:  

```bash
cd game
ls main.py
```

---

## Ejecución del juego

El punto de entrada es `main.py`.  
El juego inicializa el motor principal y la interfaz de usuario basada en teclado.  

### Comando de inicio

```bash
python main.py
```

Esto lanzará el bucle principal de la aplicación con la función `app()`.

---

## Primer uso

Al iniciar por primera vez, el sistema realiza la siguiente secuencia de inicialización:

1. Motor del juego  
2. Interfaz de usuario  
3. Sistema de niveles  

---

## Flujo de navegación

| Paso | Acción del usuario          | Respuesta del sistema                |
|------|-----------------------------|--------------------------------------|
| 1    | Ejecutar `main.py`          | Se muestra el menú principal          |
| 2    | Seleccionar "Jugar"         | Muestra selección de dificultad       |
| 3    | Elegir dificultad           | Lista de niveles disponibles          |
| 4    | Seleccionar nivel           | Carga y muestra el tablero            |
| 5    | Usar controles del teclado  | Inicia la partida interactiva         |

---

## Solución de problemas

- **Problemas de instalación de dependencias**  
  Ejecutar:  
  ```bash
  pip install --upgrade keyboard==0.13.5
  ```

- **Permisos**  
  En algunos sistemas se requieren permisos elevados para capturar entradas:  
  ```bash
  sudo python main.py
  ```

- **Compatibilidad de terminal**  
  Asegúrese de que el terminal soporte:  
  - Códigos de color ANSI  
  - Detección de teclas de flecha  
  - Codificación UTF-8  

--- 

## Integrantes y responsabilidades  

- **Flow Free jugable:** Deybby  
- **Algoritmo BFS:** Héctor  
- **Algoritmo DFS:** Sarah  
- **Algoritmo A\*:** Carlos

Cada integrante deberá documentar su parte en un archivo Word y subirlo al repositorio.  
Posteriormente, se dará formato unificado a la documentación final.  

---

## Convenciones de commits  

Para mantener un historial claro y consistente, se utilizarán los siguientes prefijos en los mensajes de commit:  

- **add** → para agregar un archivo.
- **feat** → para una nueva funcionalidad.  
- **fix** → para correcciones de errores.  
- **docs** → cambios en documentación.  
- **style** → cambios de formato, espacios, comas, nada que altere lógica.  
- **refactor** → cambios en el código que no agregan funcionalidad ni arreglan bugs.  
- **perf** → optimizaciones de rendimiento.  
- **test** → agregar o corregir pruebas.  
- **chore** → tareas de mantenimiento (configuración, build, dependencias, etc.).  
- **ci** → cambios en integración continua.  
- **build** → cambios que afectan compilación, dependencias, herramientas.  

---

## Licencia  

Este proyecto se distribuye bajo la licencia **MIT**.  
