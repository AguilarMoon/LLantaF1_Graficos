"""
Módulo: clipping.py
Implementa el algoritmo Sutherland-Hodgman para clipping 3D
"""

import math
import numpy as np


class PlanoClipping:
    """Representa un plano de clipping definido por Ax + By + Cz + D = 0"""
    
    def __init__(self, A, B, C, D):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        
        # Normalizar el vector normal del plano
        longitud = math.sqrt(A*A + B*B + C*C)
        if longitud > 0:
            self.A /= longitud
            self.B /= longitud
            self.C /= longitud
            self.D /= longitud
    
    def distancia(self, punto):
        """Calcula la distancia con signo de un punto al plano"""
        return self.A * punto[0] + self.B * punto[1] + self.C * punto[2] + self.D
    
    def esta_dentro(self, punto):
        """Determina si un punto está en el lado positivo del plano"""
        return self.distancia(punto) >= 0


def calcular_interseccion_plano(p1, p2, plano):
    """
    Calcula la intersección de un segmento de línea con un plano
    
    Args:
        p1: Primer punto del segmento
        p2: Segundo punto del segmento
        plano: PlanoClipping
    
    Returns:
        Punto de intersección o None si no hay intersección válida
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    direccion = p2 - p1
    
    denominador = plano.A * direccion[0] + plano.B * direccion[1] + plano.C * direccion[2]
    
    # Si el denominador es ~0, la línea es paralela al plano
    if abs(denominador) < 1e-10:
        return None
    
    numerador = -(plano.A * p1[0] + plano.B * p1[1] + plano.C * p1[2] + plano.D)
    t = numerador / denominador
    
    # Intersección debe estar entre p1 y p2
    if t < 0 or t > 1:
        return None
    
    interseccion = p1 + t * direccion
    return interseccion.tolist()


def sutherland_hodgman_clip_poligono(vertices, plano):
    """
    Recorta un polígono usando el algoritmo Sutherland-Hodgman
    
    Args:
        vertices: Lista de vértices del polígono
        plano: PlanoClipping
    
    Returns:
        Lista de vértices del polígono recortado
    """
    if len(vertices) < 3:
        return []
    
    vertices_recortados = []
    
    for i in range(len(vertices)):
        v_actual = vertices[i]
        v_siguiente = vertices[(i + 1) % len(vertices)]
        
        dentro_actual = plano.esta_dentro(v_actual)
        dentro_siguiente = plano.esta_dentro(v_siguiente)
        
        if dentro_actual and dentro_siguiente:
            # Ambos dentro: agregar el siguiente
            vertices_recortados.append(v_siguiente)
        elif dentro_actual and not dentro_siguiente:
            # Sale del área: agregar intersección
            interseccion = calcular_interseccion_plano(v_actual, v_siguiente, plano)
            if interseccion is not None:
                vertices_recortados.append(interseccion)
        elif not dentro_actual and dentro_siguiente:
            # Entra al área: agregar intersección y siguiente
            interseccion = calcular_interseccion_plano(v_actual, v_siguiente, plano)
            if interseccion is not None:
                vertices_recortados.append(interseccion)
            vertices_recortados.append(v_siguiente)
        # Si ambos están fuera, no se agrega nada
    
    return vertices_recortados


def recortar_malla_con_plano(vertices, caras, plano):
    """
    Recorta una malla completa usando un plano de clipping
    
    Args:
        vertices: Lista de vértices de la malla
        caras: Lista de caras (triángulos)
        plano: PlanoClipping
    
    Returns:
        Tupla (vertices_nuevos, caras_nuevas)
    """
    nuevas_caras = []
    vertices_usados = []
    mapa_vertices = {}
    
    for cara in caras:
        # Obtener vértices de la cara
        vertices_cara = [vertices[idx] for idx in cara]
        
        # Recortar polígono
        vertices_recortados = sutherland_hodgman_clip_poligono(vertices_cara, plano)
        
        if len(vertices_recortados) >= 3:
            indices_nuevos = []
            
            # Agregar o reusar vértices
            for v in vertices_recortados:
                v_tuple = tuple(v)
                if v_tuple not in mapa_vertices:
                    mapa_vertices[v_tuple] = len(vertices_usados)
                    vertices_usados.append(v)
                indices_nuevos.append(mapa_vertices[v_tuple])
            
            # Triangular el polígono recortado (fan triangulation)
            for i in range(1, len(indices_nuevos) - 1):
                nuevas_caras.append([
                    indices_nuevos[0], 
                    indices_nuevos[i], 
                    indices_nuevos[i+1]
                ])
    
    return vertices_usados, nuevas_caras