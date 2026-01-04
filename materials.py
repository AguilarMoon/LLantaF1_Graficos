"""
Módulo: materials.py
Define los materiales para el rendering Phong
Versión 5.1: Temas de color + materiales optimizados
"""

import numpy as np


class Material:
    """Clase que representa un material con propiedades Phong"""
    
    def __init__(self, nombre, ka, kd, ks, shininess, color):
        self.nombre = nombre
        self.ka = ka  # Coeficiente ambiental
        self.kd = kd  # Coeficiente difuso
        self.ks = ks  # Coeficiente especular
        self.shininess = shininess  # Brillo especular
        self.color = np.array(color)


# ========== MATERIALES BASE ==========

MATERIAL_GOMA = Material(
    "Goma Neumático", 
    ka=0.2, 
    kd=0.7, 
    ks=0.1, 
    shininess=5, 
    color=[0.12, 0.12, 0.12]
)

MATERIAL_METAL_DORADO = Material(
    "Metal Dorado (Rin)", 
    ka=0.3, 
    kd=0.6, 
    ks=0.9, 
    shininess=120,
    color=[0.80, 0.72, 0.28]
)

MATERIAL_METAL_OSCURO = Material(
    "Metal Oscuro (Centro)", 
    ka=0.2, 
    kd=0.5, 
    ks=0.8, 
    shininess=80,
    color=[0.25, 0.25, 0.30]
)

# 🎨 NUEVO: Pisos temáticos
MATERIAL_PISO_CLARO = Material(
    "Piso Concreto Claro",
    ka=0.3,
    kd=0.6,
    ks=0.2,
    shininess=10,
    color=[0.5, 0.5, 0.5]
)

MATERIAL_PISO_OSCURO = Material(
    "Piso Oscuro",
    ka=0.2,
    kd=0.4,
    ks=0.1,
    shininess=5,
    color=[0.12, 0.12, 0.15]  # Azul oscuro casi negro
)

MATERIAL_PISO_GARAGE = Material(
    "Piso Garage F1",
    ka=0.25,
    kd=0.5,
    ks=0.15,
    shininess=8,
    color=[0.18, 0.18, 0.20]  # Gris antracita
)

MATERIAL_PISO_NEGRO = Material(
    "Piso Negro Studio",
    ka=0.15,
    kd=0.3,
    ks=0.05,
    shininess=3,
    color=[0.05, 0.05, 0.05]  # Negro profundo
)

# Variable global para el piso actual (se actualiza dinámicamente)
MATERIAL_PISO = MATERIAL_PISO_OSCURO

# ========== MATERIALES F1 ==========

MATERIAL_BANDA_ROJA = Material(
    "Banda Roja Pirelli",
    ka=0.3,
    kd=0.8,
    ks=0.3,
    shininess=20,
    color=[0.90, 0.10, 0.10]
)

MATERIAL_BANDA_AMARILLA = Material(
    "Banda Amarilla Pirelli",
    ka=0.3,
    kd=0.8,
    ks=0.3,
    shininess=20,
    color=[1.0, 0.85, 0.0]
)

MATERIAL_BANDA_BLANCA = Material(
    "Banda Blanca Pirelli",
    ka=0.4,
    kd=0.7,
    ks=0.4,
    shininess=25,
    color=[0.95, 0.95, 0.95]
)

MATERIAL_TORNILLOS = Material(
    "Tornillos Hub",
    ka=0.2,
    kd=0.4,
    ks=0.9,
    shininess=100,
    color=[0.50, 0.50, 0.55]
)

MATERIAL_ANILLO_HUB = Material(
    "Anillo Decorativo Hub",
    ka=0.3,
    kd=0.5,
    ks=0.85,
    shininess=110,
    color=[0.70, 0.62, 0.20]
)

MATERIAL_DISCO_RELLENO = Material(
    "Disco Relleno Hub",
    ka=0.25,
    kd=0.5,
    ks=0.7,
    shininess=90,
    color=[0.65, 0.58, 0.22]
)

MATERIAL_SIDEWALL_MARCAS = Material(
    "Marcas Sidewall",
    ka=0.3,
    kd=0.6,
    ks=0.2,
    shininess=15,
    color=[0.85, 0.85, 0.85]
)

# ========== TEMAS DE COLOR 🎨 ==========

TEMAS = {
    'oscuro': {
        'fondo': (0.15, 0.15, 0.18),
        'piso': MATERIAL_PISO_OSCURO,
        'nombre': 'OSCURO DRAMÁTICO'
    },
    'negro': {
        'fondo': (0.05, 0.05, 0.05),
        'piso': MATERIAL_PISO_NEGRO,
        'nombre': 'NEGRO STUDIO'
    },
    'garage': {
        'fondo': (0.25, 0.27, 0.30),
        'piso': MATERIAL_PISO_GARAGE,
        'nombre': 'GARAGE F1'
    },
    'claro': {
        'fondo': (0.9, 0.9, 0.9),
        'piso': MATERIAL_PISO_CLARO,
        'nombre': 'CLARO ORIGINAL'
    }
}

# ========== COLORES DE LUZ 💡 ==========

COLORES_LUZ = {
    'blanca': {
        'color': np.array([1.0, 1.0, 1.0]),
        'nombre': 'BLANCA'
    },
    'roja': {
        'color': np.array([1.0, 0.3, 0.3]),
        'nombre': 'ROJA'
    },
    'azul': {
        'color': np.array([0.4, 0.6, 1.0]),
        'nombre': 'AZUL'
    },
    'amarilla': {
        'color': np.array([1.0, 0.9, 0.5]),
        'nombre': 'AMARILLA'
    },
    'verde': {
        'color': np.array([0.4, 1.0, 0.5]),
        'nombre': 'VERDE'
    },
    'morada': {
        'color': np.array([0.8, 0.4, 1.0]),
        'nombre': 'MORADA'
    }
}

# ========== FUNCIONES AUXILIARES ==========

MATERIALES_PIRELLI = {
    'soft': MATERIAL_BANDA_ROJA,
    'medium': MATERIAL_BANDA_AMARILLA,
    'hard': MATERIAL_BANDA_BLANCA,
}

def get_material_neumatico(tipo='soft'):
    """
    Retorna el material de banda según el tipo de neumático
    
    Args:
        tipo: 'soft', 'medium', o 'hard'
    
    Returns:
        Material correspondiente
    """
    return MATERIALES_PIRELLI.get(tipo, MATERIAL_BANDA_ROJA)


def get_tema(nombre_tema):
    """
    Retorna configuración de tema
    
    Args:
        nombre_tema: Nombre del tema ('oscuro', 'negro', 'garage', 'claro')
    
    Returns:
        Diccionario con configuración del tema
    """
    return TEMAS.get(nombre_tema, TEMAS['oscuro'])


def get_color_luz(nombre_color):
    """
    Retorna color de luz
    
    Args:
        nombre_color: Nombre del color ('blanca', 'roja', 'azul', etc.)
    
    Returns:
        Array numpy con color RGB
    """
    return COLORES_LUZ.get(nombre_color, COLORES_LUZ['blanca'])['color']