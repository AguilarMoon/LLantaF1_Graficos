"""
Módulo: lighting.py
Implementa el modelo de iluminación Phong + Spotlight
Versión 5.1: Agregado modo linterna
"""

import numpy as np


def normalizar(vector):
    """Normaliza un vector a longitud unitaria"""
    norma = np.linalg.norm(vector)
    return vector / norma if norma > 0 else vector


def phong_shading(punto, normal, material, luz_pos, camara_pos, luz_color, luz_ambiente):
    """
    Calcula el color de un punto usando el modelo de iluminación Phong
    
    Args:
        punto: Posición del punto en el espacio
        normal: Vector normal de la superficie
        material: Objeto Material con propiedades
        luz_pos: Posición de la fuente de luz
        camara_pos: Posición de la cámara
        luz_color: Color de la luz (RGB)
        luz_ambiente: Color de la luz ambiental (RGB)
    
    Returns:
        Color final calculado (RGB)
    """
    # Normalizar vectores
    N = normalizar(normal)
    L = normalizar(luz_pos - punto)
    V = normalizar(camara_pos - punto)
    
    # Componente ambiental
    I_ambiente = material.ka * luz_ambiente * material.color
    
    # Componente difusa (Lambert)
    dot_NL = max(0.0, np.dot(N, L))
    I_difusa = material.kd * luz_color * dot_NL * material.color
    
    # Componente especular (Blinn-Phong simplificado)
    R = 2.0 * dot_NL * N - L
    R = normalizar(R)
    dot_RV = max(0.0, np.dot(R, V))
    especular_intensity = pow(dot_RV, material.shininess)
    I_especular = material.ks * luz_color * especular_intensity
    
    # Color final
    color_final = I_ambiente + I_difusa + I_especular
    return np.clip(color_final, 0.0, 1.0)


def spotlight_shading(punto, normal, material, luz_pos, luz_dir, camara_pos, 
                      luz_color, luz_ambiente, apertura=20.0, suavizado=5.0):
    """
    🔦 NUEVO: Calcula iluminación tipo linterna/spotlight con cono de luz
    
    Args:
        punto: Posición del punto en el espacio
        normal: Vector normal de la superficie
        material: Objeto Material con propiedades
        luz_pos: Posición de la fuente de luz
        luz_dir: Dirección del spotlight (vector normalizado)
        camara_pos: Posición de la cámara
        luz_color: Color de la luz (RGB)
        luz_ambiente: Color de la luz ambiental (RGB)
        apertura: Ángulo del cono en grados (típico: 15-30°)
        suavizado: Suavizado del borde en grados (típico: 3-8°)
    
    Returns:
        Color final calculado (RGB)
    """
    # Normalizar vectores
    N = normalizar(normal)
    L = normalizar(luz_pos - punto)
    V = normalizar(camara_pos - punto)
    luz_dir_norm = normalizar(luz_dir)
    
    # Calcular si el punto está dentro del cono del spotlight
    # Ángulo entre dirección de la luz y dirección hacia el punto
    cos_angulo = np.dot(-L, luz_dir_norm)
    angulo_punto = np.degrees(np.arccos(np.clip(cos_angulo, -1.0, 1.0)))
    
    # Calcular intensidad del spotlight con falloff suave
    if angulo_punto > apertura + suavizado:
        intensidad_spot = 0.0  # Fuera del cono completamente
    elif angulo_punto > apertura:
        # Zona de transición suave (falloff)
        factor = (apertura + suavizado - angulo_punto) / suavizado
        intensidad_spot = factor * factor  # Curva cuadrática para suavizado
    else:
        intensidad_spot = 1.0  # Dentro del cono principal
    
    # Atenuación por distancia (más suave para mayor alcance)
    distancia = np.linalg.norm(luz_pos - punto)
    atenuacion = 1.0 / (1.0 + 0.02 * distancia + 0.005 * distancia * distancia)
    intensidad_spot *= atenuacion
    
    # Componente ambiental (muy reducida para contraste dramático)
    I_ambiente = material.ka * luz_ambiente * material.color * 0.15
    
    # Componente difusa (AMPLIFICADA 2x para más intensidad)
    dot_NL = max(0.0, np.dot(N, L))
    I_difusa = material.kd * luz_color * dot_NL * material.color * intensidad_spot * 2.0
    
    # Componente especular (AMPLIFICADA 1.5x para brillos más intensos)
    R = 2.0 * dot_NL * N - L
    R = normalizar(R)
    dot_RV = max(0.0, np.dot(R, V))
    especular_intensity = pow(dot_RV, material.shininess)
    I_especular = material.ks * luz_color * especular_intensity * intensidad_spot * 1.5
    
    # Color final
    color_final = I_ambiente + I_difusa + I_especular
    return np.clip(color_final, 0.0, 1.0)