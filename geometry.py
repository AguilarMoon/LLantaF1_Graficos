"""
Módulo: geometry.py
Generación de geometrías 3D (cilindros, toroides, etc.)
Versión 5.0: Llanta F1 Realista con detalles visuales
"""

import math
import numpy as np


def generar_vertices_cilindro(radio, altura, segmentos=64):
    """
    Genera un cilindro con tapas
    
    Args:
        radio: Radio del cilindro
        altura: Altura del cilindro
        segmentos: Número de subdivisiones alrededor del cilindro
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    # Vértices superiores
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = radio * math.cos(angulo)
        z = radio * math.sin(angulo)
        vertices.append([x, altura/2, z])
    
    # Vértices inferiores
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        x = radio * math.cos(angulo)
        z = radio * math.sin(angulo)
        vertices.append([x, -altura/2, z])
    
    # Caras laterales
    for i in range(segmentos):
        actual_sup = i
        siguiente_sup = (i + 1) % segmentos
        actual_inf = i + segmentos
        siguiente_inf = ((i + 1) % segmentos) + segmentos
        
        caras.append([actual_sup, actual_inf, siguiente_sup])
        caras.append([siguiente_sup, actual_inf, siguiente_inf])
    
    # Tapas
    centro_sup = len(vertices)
    vertices.append([0, altura/2, 0])
    centro_inf = len(vertices)
    vertices.append([0, -altura/2, 0])
    
    for i in range(segmentos):
        siguiente = (i + 1) % segmentos
        caras.append([centro_sup, i, siguiente])
        caras.append([centro_inf, siguiente + segmentos, i + segmentos])
    
    return vertices, caras


def generar_toroide(radio_mayor, radio_menor, segmentos_mayor=32, segmentos_menor=16):
    """
    Genera un toroide (dona)
    
    Args:
        radio_mayor: Radio del círculo central
        radio_menor: Radio del tubo
        segmentos_mayor: Subdivisiones alrededor del círculo mayor
        segmentos_menor: Subdivisiones alrededor del tubo
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    for i in range(segmentos_mayor):
        theta = 2.0 * math.pi * i / segmentos_mayor
        for j in range(segmentos_menor):
            phi = 2.0 * math.pi * j / segmentos_menor
            x = (radio_mayor + radio_menor * math.cos(phi)) * math.cos(theta)
            y = radio_menor * math.sin(phi)
            z = (radio_mayor + radio_menor * math.cos(phi)) * math.sin(theta)
            vertices.append([x, y, z])
    
    # Conectar vértices en cuadriláteros (divididos en 2 triángulos)
    for i in range(segmentos_mayor):
        for j in range(segmentos_menor):
            p1 = i * segmentos_menor + j
            p2 = i * segmentos_menor + (j + 1) % segmentos_menor
            p3 = ((i + 1) % segmentos_mayor) * segmentos_menor + (j + 1) % segmentos_menor
            p4 = ((i + 1) % segmentos_mayor) * segmentos_menor + j
            
            caras.append([p1, p2, p3])
            caras.append([p1, p3, p4])
    
    return vertices, caras


def generar_banda_color_neumatico(radio_mayor, radio_menor, posicion_y, ancho_banda, segmentos=64):
    """
    ⭐ NUEVO: Genera una banda de color (roja/amarilla) en el neumático estilo Pirelli
    
    Args:
        radio_mayor: Radio del toroide
        radio_menor: Radio del tubo del toroide
        posicion_y: Posición Y de la banda (-0.3 a 0.3 aprox)
        ancho_banda: Ancho de la banda
        segmentos: Subdivisiones
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    # Calcular ángulo phi para la posición Y deseada
    phi_centro = math.asin(posicion_y / radio_menor)
    delta_phi = ancho_banda / radio_menor / 2
    
    for i in range(segmentos):
        theta = 2.0 * math.pi * i / segmentos
        
        # Banda superior
        phi_sup = phi_centro + delta_phi
        x_sup = (radio_mayor + radio_menor * math.cos(phi_sup)) * math.cos(theta)
        y_sup = radio_menor * math.sin(phi_sup)
        z_sup = (radio_mayor + radio_menor * math.cos(phi_sup)) * math.sin(theta)
        vertices.append([x_sup, y_sup, z_sup])
        
        # Banda inferior
        phi_inf = phi_centro - delta_phi
        x_inf = (radio_mayor + radio_menor * math.cos(phi_inf)) * math.cos(theta)
        y_inf = radio_menor * math.sin(phi_inf)
        z_inf = (radio_mayor + radio_menor * math.cos(phi_inf)) * math.sin(theta)
        vertices.append([x_inf, y_inf, z_inf])
    
    # Crear caras de la banda
    for i in range(segmentos):
        idx1 = i * 2
        idx2 = i * 2 + 1
        idx3 = ((i + 1) % segmentos) * 2 + 1
        idx4 = ((i + 1) % segmentos) * 2
        
        caras.append([idx1, idx2, idx3])
        caras.append([idx1, idx3, idx4])
    
    return vertices, caras


def generar_radios_aerodinamicos(radio_interno, radio_externo, altura, num_radios=10):
    """
    ⭐ MEJORADO: Genera radios estilo F1 (más delgados y aerodinámicos)
    
    Args:
        radio_interno: Radio donde comienzan los radios
        radio_externo: Radio donde terminan los radios
        altura: Grosor del rin
        num_radios: Número de radios
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    grosor_radio = 0.08  # ⭐ Más delgado (antes 0.15)
    
    for i in range(num_radios):
        angulo = 2.0 * math.pi * i / num_radios
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        cos_perp = math.cos(angulo + math.pi/2)
        sin_perp = math.sin(angulo + math.pi/2)
        
        base_idx = len(vertices)
        
        # ⭐ Perfil aerodinámico: más ancho en el interior, más delgado en el exterior
        grosor_int = grosor_radio * 1.2
        grosor_ext = grosor_radio * 0.7
        
        # 8 vértices por radio (4 arriba, 4 abajo)
        # Interior superior
        vertices.append([radio_interno * cos_a + grosor_int * cos_perp, altura/2, 
                        radio_interno * sin_a + grosor_int * sin_perp])
        vertices.append([radio_interno * cos_a - grosor_int * cos_perp, altura/2,
                        radio_interno * sin_a - grosor_int * sin_perp])
        # Exterior superior
        vertices.append([radio_externo * cos_a - grosor_ext * cos_perp, altura/2,
                        radio_externo * sin_a - grosor_ext * sin_perp])
        vertices.append([radio_externo * cos_a + grosor_ext * cos_perp, altura/2,
                        radio_externo * sin_a + grosor_ext * sin_perp])
        
        # Interior inferior
        vertices.append([radio_interno * cos_a + grosor_int * cos_perp, -altura/2,
                        radio_interno * sin_a + grosor_int * sin_perp])
        vertices.append([radio_interno * cos_a - grosor_int * cos_perp, -altura/2,
                        radio_interno * sin_a - grosor_int * sin_perp])
        # Exterior inferior
        vertices.append([radio_externo * cos_a - grosor_ext * cos_perp, -altura/2,
                        radio_externo * sin_a - grosor_ext * sin_perp])
        vertices.append([radio_externo * cos_a + grosor_ext * cos_perp, -altura/2,
                        radio_externo * sin_a + grosor_ext * sin_perp])
        
        # Caras del radio (12 triángulos)
        caras.append([base_idx, base_idx+1, base_idx+2])
        caras.append([base_idx, base_idx+2, base_idx+3])
        caras.append([base_idx+4, base_idx+6, base_idx+5])
        caras.append([base_idx+4, base_idx+7, base_idx+6])
        caras.append([base_idx, base_idx+3, base_idx+7])
        caras.append([base_idx, base_idx+7, base_idx+4])
        caras.append([base_idx+1, base_idx+5, base_idx+6])
        caras.append([base_idx+1, base_idx+6, base_idx+2])
        caras.append([base_idx+3, base_idx+2, base_idx+6])
        caras.append([base_idx+3, base_idx+6, base_idx+7])
        caras.append([base_idx, base_idx+4, base_idx+5])
        caras.append([base_idx, base_idx+5, base_idx+1])
    
    return vertices, caras


def generar_tornillos_hub(radio, altura, num_tornillos=5):
    """
    ⭐ NUEVO: Genera tornillos decorativos en el hub central
    
    Args:
        radio: Radio donde se colocan los tornillos
        altura: Grosor del hub
        num_tornillos: Número de tornillos (típicamente 5 en F1)
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    radio_tornillo = 0.12
    segmentos = 8
    
    for i in range(num_tornillos):
        angulo_base = 2.0 * math.pi * i / num_tornillos
        centro_x = radio * math.cos(angulo_base)
        centro_z = radio * math.sin(angulo_base)
        
        # Crear cilindro pequeño para cada tornillo
        base_idx = len(vertices)
        
        # Vértices superiores del tornillo
        for j in range(segmentos):
            angulo = 2.0 * math.pi * j / segmentos
            x = centro_x + radio_tornillo * math.cos(angulo)
            z = centro_z + radio_tornillo * math.sin(angulo)
            vertices.append([x, altura/2, z])
        
        # Vértices inferiores del tornillo
        for j in range(segmentos):
            angulo = 2.0 * math.pi * j / segmentos
            x = centro_x + radio_tornillo * math.cos(angulo)
            z = centro_z + radio_tornillo * math.sin(angulo)
            vertices.append([x, -altura/2, z])
        
        # Caras laterales del tornillo
        for j in range(segmentos):
            actual_sup = base_idx + j
            siguiente_sup = base_idx + (j + 1) % segmentos
            actual_inf = base_idx + j + segmentos
            siguiente_inf = base_idx + ((j + 1) % segmentos) + segmentos
            
            caras.append([actual_sup, actual_inf, siguiente_sup])
            caras.append([siguiente_sup, actual_inf, siguiente_inf])
        
        # Tapas del tornillo
        centro_sup = len(vertices)
        vertices.append([centro_x, altura/2, centro_z])
        centro_inf = len(vertices)
        vertices.append([centro_x, -altura/2, centro_z])
        
        for j in range(segmentos):
            siguiente = (j + 1) % segmentos
            caras.append([centro_sup, base_idx + j, base_idx + siguiente])
            caras.append([centro_inf, base_idx + siguiente + segmentos, base_idx + j + segmentos])
    
    return vertices, caras


def generar_anillo_central_hub(radio_interno, radio_externo, altura, segmentos=32):
    """
    ⭐ NUEVO: Genera el anillo decorativo alrededor del centro
    
    Args:
        radio_interno: Radio interior del anillo
        radio_externo: Radio exterior del anillo
        altura: Grosor del anillo
        segmentos: Subdivisiones
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    # Vértices del anillo (4 capas: interno-sup, externo-sup, interno-inf, externo-inf)
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        
        # Superior
        vertices.append([radio_interno * cos_a, altura/2, radio_interno * sin_a])
        vertices.append([radio_externo * cos_a, altura/2, radio_externo * sin_a])
        
        # Inferior
        vertices.append([radio_interno * cos_a, -altura/2, radio_interno * sin_a])
        vertices.append([radio_externo * cos_a, -altura/2, radio_externo * sin_a])
    
    # Crear caras
    for i in range(segmentos):
        base = i * 4
        next_base = ((i + 1) % segmentos) * 4
        
        # Cara superior (anillo)
        caras.append([base, base+1, next_base+1])
        caras.append([base, next_base+1, next_base])
        
        # Cara inferior (anillo)
        caras.append([base+2, next_base+2, base+3])
        caras.append([base+3, next_base+2, next_base+3])
        
        # Cara exterior
        caras.append([base+1, base+3, next_base+3])
        caras.append([base+1, next_base+3, next_base+1])
        
        # Cara interior
        caras.append([base, next_base, base+2])
        caras.append([base+2, next_base, next_base+2])
    
    return vertices, caras


def generar_disco_relleno(radio_interno, radio_externo, altura, segmentos=32):
    """
    ⭐ NUEVO: Genera un disco sólido para rellenar gaps (el círculo blanco)
    
    Args:
        radio_interno: Radio interior
        radio_externo: Radio exterior
        altura: Grosor
        segmentos: Subdivisiones
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    for i in range(segmentos):
        angulo = 2.0 * math.pi * i / segmentos
        cos_a = math.cos(angulo)
        sin_a = math.sin(angulo)
        
        # Superior
        vertices.append([radio_interno * cos_a, altura/2, radio_interno * sin_a])
        vertices.append([radio_externo * cos_a, altura/2, radio_externo * sin_a])
        
        # Inferior
        vertices.append([radio_interno * cos_a, -altura/2, radio_interno * sin_a])
        vertices.append([radio_externo * cos_a, -altura/2, radio_externo * sin_a])
    
    for i in range(segmentos):
        base = i * 4
        next_base = ((i + 1) % segmentos) * 4
        
        # Cara superior
        caras.append([base, base+1, next_base+1])
        caras.append([base, next_base+1, next_base])
        
        # Cara inferior
        caras.append([base+2, next_base+2, base+3])
        caras.append([base+3, next_base+2, next_base+3])
        
        # Cara exterior
        caras.append([base+1, base+3, next_base+3])
        caras.append([base+1, next_base+3, next_base+1])
        
        # Cara interior
        caras.append([base, next_base, base+2])
        caras.append([base+2, next_base, next_base+2])
    
    return vertices, caras


def generar_marcas_sidewall(radio_mayor, radio_menor, num_marcas=8):
    """
    ⭐ NUEVO: Genera marcas visuales en los lados del neumático para ver rotación
    Simula letras/líneas del fabricante
    
    Args:
        radio_mayor: Radio del toroide
        radio_menor: Radio del tubo
        num_marcas: Número de marcas alrededor
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = []
    caras = []
    
    # Posición lateral de las marcas (hacia un lado del neumático)
    phi_marca = math.pi * 0.4  # ~72° hacia el lado
    ancho_marca = 0.08
    alto_marca = 0.3
    
    for i in range(num_marcas):
        theta = 2.0 * math.pi * i / num_marcas
        
        # Centro de la marca
        x_centro = (radio_mayor + radio_menor * math.cos(phi_marca)) * math.cos(theta)
        y_centro = radio_menor * math.sin(phi_marca)
        z_centro = (radio_mayor + radio_menor * math.cos(phi_marca)) * math.sin(theta)
        
        # Crear una pequeña barra rectangular elevada
        # Vectores tangentes para orientar la marca
        tangente_theta = [-math.sin(theta), 0, math.cos(theta)]
        tangente_phi = [
            -math.sin(phi_marca) * math.cos(theta),
            math.cos(phi_marca),
            -math.sin(phi_marca) * math.sin(theta)
        ]
        
        base_idx = len(vertices)
        
        # 4 vértices por marca (rectángulo elevado)
        for dy in [-alto_marca/2, alto_marca/2]:
            for dt in [-ancho_marca/2, ancho_marca/2]:
                x = x_centro + tangente_theta[0] * dt + tangente_phi[0] * dy
                y = y_centro + tangente_theta[1] * dt + tangente_phi[1] * dy
                z = z_centro + tangente_theta[2] * dt + tangente_phi[2] * dy
                
                # Elevar ligeramente hacia afuera
                factor = 1.02
                x *= factor
                z *= factor
                
                vertices.append([x, y, z])
        
        # Crear 2 triángulos para la marca
        caras.append([base_idx, base_idx+1, base_idx+2])
        caras.append([base_idx+1, base_idx+3, base_idx+2])
    
    return vertices, caras


def generar_piso(ancho=10, profundidad=10, posicion_y=-3.5):
    """
    Genera un piso rectangular plano
    
    Args:
        ancho: Ancho del piso en X
        profundidad: Profundidad del piso en Z
        posicion_y: Altura del piso (Y)
    
    Returns:
        Tupla (vertices, caras)
    """
    vertices = [
        [-ancho/2, posicion_y, -profundidad/2],
        [ancho/2, posicion_y, -profundidad/2],
        [ancho/2, posicion_y, profundidad/2],
        [-ancho/2, posicion_y, profundidad/2]
    ]
    
    # Dos triángulos para formar un cuadrado
    caras = [
        [0, 1, 2],
        [0, 2, 3]
    ]
    
    return vertices, caras


def calcular_normales(vertices, caras):
    """
    Calcula las normales de cada cara usando producto cruz
    
    Args:
        vertices: Lista de vértices
        caras: Lista de caras (triángulos)
    
    Returns:
        Lista de vectores normales (uno por cara)
    """
    normales = []
    for cara in caras:
        v1 = np.array(vertices[cara[0]])
        v2 = np.array(vertices[cara[1]])
        v3 = np.array(vertices[cara[2]])
        
        edge1 = v2 - v1
        edge2 = v3 - v1
        normal = np.cross(edge1, edge2)
        
        longitud = np.linalg.norm(normal)
        if longitud > 0:
            normal = normal / longitud
        
        normales.append(normal)
    
    return normales