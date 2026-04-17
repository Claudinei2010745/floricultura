def normalizar_codigo(codigo):
    return str(int(codigo)) if codigo.isdigit() else codigo