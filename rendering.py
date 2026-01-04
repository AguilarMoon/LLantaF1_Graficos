"""
Módulo: rendering.py
Funciones de renderizado OpenGL
Versión 5.1: Agregado soporte para spotlight
"""

import numpy as np
from OpenGL.GL import *
from lighting import phong_shading, spotlight_shading


def dibujar_malla_phong(vertices, caras, normales, material, luz_pos, camara_pos, 
                       luz_color=None, luz_ambiente=None):
    """
    Dibuja una malla 3D con iluminación Phong
    
    Args:
        vertices: Lista de vértices
        caras: Lista de caras (triángulos)
        normales: Lista de normales (una por cara)
        material: Material de la malla
        luz_pos: Posición de la luz
        camara_pos: Posición de la cámara
        luz_color: Color de la luz (opcional)
        luz_ambiente: Color de luz ambiental (opcional)
    """
    if luz_color is None:
        luz_color = np.array([1.0, 1.0, 1.0])
    if luz_ambiente is None:
        luz_ambiente = np.array([0.4, 0.4, 0.4])
    
    glDisable(GL_LIGHTING)
    glBegin(GL_TRIANGLES)
    
    for i, cara in enumerate(caras):
        v1 = np.array(vertices[cara[0]])
        v2 = np.array(vertices[cara[1]])
        v3 = np.array(vertices[cara[2]])
        centro = (v1 + v2 + v3) / 3.0
        
        color = phong_shading(centro, normales[i], material, luz_pos, camara_pos,
                             luz_color, luz_ambiente)
        glColor3fv(color)
        
        for vertice_idx in cara:
            glVertex3fv(vertices[vertice_idx])
    
    glEnd()


def dibujar_malla_spotlight(vertices, caras, normales, material, luz_pos, luz_dir, 
                           camara_pos, luz_color=None, luz_ambiente=None, 
                           apertura=20.0, suavizado=5.0):
    """
    🔦 NUEVO: Dibuja una malla 3D con iluminación tipo spotlight/linterna
    
    Args:
        vertices: Lista de vértices
        caras: Lista de caras (triángulos)
        normales: Lista de normales (una por cara)
        material: Material de la malla
        luz_pos: Posición de la luz
        luz_dir: Dirección del spotlight
        camara_pos: Posición de la cámara
        luz_color: Color de la luz (opcional)
        luz_ambiente: Color de luz ambiental (opcional)
        apertura: Ángulo del cono del spotlight
        suavizado: Suavizado del borde
    """
    if luz_color is None:
        luz_color = np.array([1.0, 1.0, 1.0])
    if luz_ambiente is None:
        luz_ambiente = np.array([0.2, 0.2, 0.2])  # Más oscuro para spotlight
    
    glDisable(GL_LIGHTING)
    glBegin(GL_TRIANGLES)
    
    for i, cara in enumerate(caras):
        v1 = np.array(vertices[cara[0]])
        v2 = np.array(vertices[cara[1]])
        v3 = np.array(vertices[cara[2]])
        centro = (v1 + v2 + v3) / 3.0
        
        color = spotlight_shading(centro, normales[i], material, luz_pos, luz_dir,
                                 camara_pos, luz_color, luz_ambiente, 
                                 apertura, suavizado)
        glColor3fv(color)
        
        for vertice_idx in cara:
            glVertex3fv(vertices[vertice_idx])
    
    glEnd()


def dibujar_wireframe(vertices, caras, color, grosor=1.5):
    """
    Dibuja la malla en modo wireframe (solo aristas)
    
    Args:
        vertices: Lista de vértices
        caras: Lista de caras
        color: Color RGB del wireframe
        grosor: Grosor de las líneas
    """
    glDisable(GL_LIGHTING)
    glLineWidth(grosor)
    glColor3fv(color)
    
    for cara in caras:
        glBegin(GL_LINE_LOOP)
        for vertice_idx in cara:
            glVertex3fv(vertices[vertice_idx])
        glEnd()
    
    glLineWidth(1.0)


def dibujar_plano_corte(posicion_y, tamano=5.0):
    """
    Dibuja un plano semi-transparente que representa el plano de corte
    
    Args:
        posicion_y: Posición Y del plano
        tamano: Tamaño del plano en X y Z
    """
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glBegin(GL_QUADS)
    glColor4f(1.0, 0.0, 0.0, 0.3)
    glVertex3f(-tamano, posicion_y, -tamano)
    glVertex3f(tamano, posicion_y, -tamano)
    glVertex3f(tamano, posicion_y, tamano)
    glVertex3f(-tamano, posicion_y, tamano)
    glEnd()
    
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)


def dibujar_plano_corte_z(posicion_z, tamano=5.0):
    """
    Dibuja un plano semi-transparente perpendicular al eje Z
    
    Args:
        posicion_z: Posición Z del plano
        tamano: Tamaño del plano en X y Y
    """
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glBegin(GL_QUADS)
    glColor4f(1.0, 0.0, 0.0, 0.3)
    glVertex3f(-tamano, -tamano, posicion_z)
    glVertex3f(tamano, -tamano, posicion_z)
    glVertex3f(tamano, tamano, posicion_z)
    glVertex3f(-tamano, tamano, posicion_z)
    glEnd()
    
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)