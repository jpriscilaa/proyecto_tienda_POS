import os

def buscar_importaciones(ruta_base):
    archivos_py = []
    archivos_importados = set()

    for root, _, files in os.walk(ruta_base):
        for file in files:
            if file.endswith('.py'):
                ruta_completa = os.path.join(root, file)
                archivos_py.append(ruta_completa)
                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    for otro_file in files:
                        if otro_file.endswith('.py') and otro_file != file:
                            nombre = otro_file.replace('.py', '')
                            if f'import {nombre}' in contenido or f'from {nombre}' in contenido:
                                archivos_importados.add(nombre)

    no_importados = []
    for archivo in archivos_py:
        nombre = os.path.basename(archivo).replace('.py', '')
        if nombre not in archivos_importados and nombre != '__init__':
            no_importados.append(archivo)

    return no_importados

# Uso
sin_usar = buscar_importaciones("backend/")
print("Posibles archivos no usados:")
for archivo in sin_usar:
    print(archivo)