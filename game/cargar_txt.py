def load(path, as_list=True):
    try:
        with open(path, "r", encoding="utf-8") as file:
            if as_list:
                return [line.strip() for line in file]
            return file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{path}'")
        return [] if as_list else ""


if __name__ == '__main__':
    
    lines = load("f")
    lines = load("levels/5_x_5_4C_1.txt")
    print(lines)