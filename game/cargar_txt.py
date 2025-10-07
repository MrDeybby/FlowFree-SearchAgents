def load(path:str, as_list:bool=True):
    """
    The `load` function reads a file from the specified path and returns its content either as a list of
    lines or as a single string.
    
    :param path: The `path` parameter in the `load` function is a string that represents the file path
    of the file you want to load
    :type path: str
    :param as_list: The `as_list` parameter in the `load` function is a boolean parameter that
    determines whether the file content should be returned as a list of lines (if `as_list` is True) or
    as a single string containing the entire file content (if `as_list` is False), defaults to True
    :type as_list: bool (optional)
    :return: The `load` function returns either a list of lines from the file (if `as_list` is `True`)
    or the entire content of the file as a string (if `as_list` is `False`). If the file is not found,
    an error message is printed and an empty list or an empty string is returned based on the value of
    `as_list`.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            
            if as_list:
                return [line.strip() for line in file]
            
            # The `return file.read()` statement in the `load` function is returning the entire
            # content of the file as a single string. When `as_list` parameter is set to `False`, the
            # function reads the content of the file using `file.read()` and returns it as a single
            # string.
            return file.read()
    # The `except FileNotFoundError` block in the `load` function is a part of error handling
    # mechanism in Python.
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{path}'")
        # The line `return [] if as_list else ""` in the `load` function is a conditional return
        # statement based on the value of the `as_list` parameter. Return a void str or list if the file not founded
        return [] if as_list else ""


if __name__ == '__main__':
    
    lines = load("f")
    lines = load("levels/5x5_4C_1.txt")
    print(lines)