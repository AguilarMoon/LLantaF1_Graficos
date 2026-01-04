"""
Módulo: transforms.py
Transformaciones geométricas con matrices y coordenadas homogéneas
"""

import numpy as np


def crear_matriz_identidad():
    """
    Crea una matriz identidad 4x4 para transformaciones homogéneas
    
    Returns:
        Matriz 4x4 identidad
    """
    return np.identity(4)


def matriz_traslacion(tx, ty, tz):
    """
    Crea una matriz de traslación en coordenadas homogéneas
    
    [ 1  0  0  tx ]
    [ 0  1  0  ty ]
    [ 0  0  1  tz ]
    [ 0  0  0  1  ]
    
    Args:
        tx, ty, tz: Desplazamientos en x, y, z
    
    Returns:
        Matriz 4x4 de traslación
    """
    M = crear_matriz_identidad()
    M[0, 3] = tx
    M[1, 3] = ty
    M[2, 3] = tz
    return M


def matriz_escalamiento(sx, sy, sz):
    """
    Crea una matriz de escalamiento en coordenadas homogéneas
    
    [ sx  0   0   0 ]
    [ 0   sy  0   0 ]
    [ 0   0   sz  0 ]
    [ 0   0   0   1 ]
    
    Args:
        sx, sy, sz: Factores de escala en x, y, z
    
    Returns:
        Matriz 4x4 de escalamiento
    """
    M = crear_matriz_identidad()
    M[0, 0] = sx
    M[1, 1] = sy
    M[2, 2] = sz
    return M


def matriz_rotacion_x(angulo):
    """
    Crea una matriz de rotación alrededor del eje X
    
    Args:
        angulo: Ángulo en grados
    
    Returns:
        Matriz 4x4 de rotación
    """
    rad = np.radians(angulo)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    M = crear_matriz_identidad()
    M[1, 1] = cos_a
    M[1, 2] = -sin_a
    M[2, 1] = sin_a
    M[2, 2] = cos_a
    return M


def matriz_rotacion_y(angulo):
    """
    Crea una matriz de rotación alrededor del eje Y
    
    Args:
        angulo: Ángulo en grados
    
    Returns:
        Matriz 4x4 de rotación
    """
    rad = np.radians(angulo)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    M = crear_matriz_identidad()
    M[0, 0] = cos_a
    M[0, 2] = sin_a
    M[2, 0] = -sin_a
    M[2, 2] = cos_a
    return M


def matriz_rotacion_z(angulo):
    """
    Crea una matriz de rotación alrededor del eje Z
    
    Args:
        angulo: Ángulo en grados
    
    Returns:
        Matriz 4x4 de rotación
    """
    rad = np.radians(angulo)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    M = crear_matriz_identidad()
    M[0, 0] = cos_a
    M[0, 1] = -sin_a
    M[1, 0] = sin_a
    M[1, 1] = cos_a
    return M


def a_coordenadas_homogeneas(vertices):
    """
    Convierte vértices 3D a coordenadas homogéneas 4D
    [x, y, z] -> [x, y, z, 1]
    
    Args:
        vertices: Lista o array de vértices 3D
    
    Returns:
        Array numpy Nx4 con coordenadas homogéneas
    """
    vertices_array = np.array(vertices)
    if vertices_array.ndim == 1:
        # Un solo vértice
        return np.append(vertices_array, 1.0)
    else:
        # Múltiples vértices
        unos = np.ones((vertices_array.shape[0], 1))
        return np.hstack([vertices_array, unos])


def de_coordenadas_homogeneas(vertices_h):
    """
    Convierte coordenadas homogéneas 4D a coordenadas 3D
    [x, y, z, w] -> [x/w, y/w, z/w]
    
    Args:
        vertices_h: Array de vértices en coordenadas homogéneas
    
    Returns:
        Array numpy Nx3 con coordenadas cartesianas
    """
    vertices_array = np.array(vertices_h)
    if vertices_array.ndim == 1:
        # Un solo vértice
        w = vertices_array[3]
        return vertices_array[:3] / w if w != 0 else vertices_array[:3]
    else:
        # Múltiples vértices
        w = vertices_array[:, 3:4]
        return vertices_array[:, :3] / w


def aplicar_transformacion(vertices, matriz):
    """
    Aplica una matriz de transformación a un conjunto de vértices
    
    Args:
        vertices: Lista de vértices 3D [[x,y,z], ...]
        matriz: Matriz de transformación 4x4
    
    Returns:
        Lista de vértices transformados
    """
    # Convertir a coordenadas homogéneas
    vertices_h = a_coordenadas_homogeneas(vertices)
    
    # Aplicar transformación (multiplicación matricial)
    vertices_transformados_h = np.dot(vertices_h, matriz.T)
    
    # Convertir de vuelta a coordenadas 3D
    vertices_transformados = de_coordenadas_homogeneas(vertices_transformados_h)
    
    return vertices_transformados.tolist()


def componer_transformaciones(*matrices):
    """
    Compone múltiples matrices de transformación
    
    Args:
        *matrices: Secuencia de matrices 4x4
    
    Returns:
        Matriz 4x4 resultante de la composición
    """
    resultado = crear_matriz_identidad()
    for matriz in matrices:
        resultado = np.dot(resultado, matriz)
    return resultado


def imprimir_matriz(matriz, nombre="Matriz"):
    """
    Imprime una matriz de forma legible (útil para debugging)
    
    Args:
        matriz: Matriz numpy
        nombre: Nombre descriptivo de la matriz
    """
    print(f"\n{nombre}:")
    print(matriz)