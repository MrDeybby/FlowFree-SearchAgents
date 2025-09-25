# Flow Free Levels

Esta carpeta contiene los archivos de nivel del juego Flow Free. Cada archivo representa una configuración de rompecabezas diferente.

## Estructura de archivos

Los archivos de nivel se nombran con el siguiente formato:
```
{ancho}x{alto}_{cantidad_colores}C_{número_nivel}.txt
```
Ejemplo: `5x5_4C_1.txt` representa una cuadrícula de 5x5, 4 colores, nivel 1

## Formato de nivel

Cada archivo de nivel contiene una representación de cuadrícula donde:

- `.` (punto) = Celda vacía
- `#` (hashtag) = Celda bloqueada
- Las letras representan extremos de diferentes colores:
- `A` = Azul
- `R` = Rojo
- `V` = Verde
- `Y` = Amarillo
- `M` = Magenta
- `C` = Cian
- `N` = Naranja

### Ejemplo
```
A...Y
V.YV.
...A.
R...R
```
En este ejemplo:
- A-A representa los extremos azules del camino
- R-R representa los extremos rojos del camino
- V-V representa los extremos verdes del camino
- Y-Y representa los extremos amarillos del camino