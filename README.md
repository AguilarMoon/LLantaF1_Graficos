Llanta F1 3D - Visualizador Interactivo

Proyecto de renderizado 3D de una llanta de Fórmula 1 con iluminación avanzada, clipping geométrico y múltiples modos de visualización.

Descripción

Sistema de visualización 3D que implementa desde cero el renderizado de una llanta de F1 realista, utilizando PyGame y OpenGL. Incluye geometría procedural, iluminación Phong, spotlight dinámico, clipping 3D con algoritmo Sutherland-Hodgman, y múltiples temas visuales.

Características

Renderizado

- Modo Sólido: Iluminación Phong completa con componentes ambiental, difusa y especular
- Modo Wireframe: Visualización de la estructura de malla
- Modo Mixto: Combinación de ambos modos

Sistema de Iluminación

- Luz Normal: Iluminación estática desde arriba
- Linterna Fija : Spotlight que sigue la cámara
- Linterna Libre: Spotlight direccional controlable con el mouse
- 6 Colores de Luz: Blanca, roja, azul, amarilla, verde, morada
- Apertura Ajustable: Control del ángulo del cono de luz

Temas Visuales

- Oscuro Dramático: Fondo azul oscuro con piso matching
- Negro Studio: Ambiente de fotografía profesional
- Garage F1: Ambiente realista de pit
- Claro Original: Fondo claro para contraste

Clipping 3D

- Algoritmo Sutherland-Hodgman implementado desde cero
- Corte en tiempo real con plano móvil
- Visualización del plano de corte
- Preserva topología durante el clipping

Geometría Realista

- Neumático: Toroide con marcas sidewall simuladas
- Banda Pirelli: Banda de color estilo F1 (roja/amarilla/blanca)
- Rin: Cilindro con acabado dorado metálico
- Radios Aerodinámicos: 10 radios con perfil delgado estilo F1
- Hub Central: Con anillo decorativo y 5 tornillos
- Piso: Superficie con iluminación y temas

 Tecnologías

- Python 3.x
- PyGame: Manejo de ventana y eventos
- PyOpenGL: Renderizado 3D
- NumPy: Cálculos matemáticos y transformaciones
- Algoritmos propios: Sutherland-Hodgman, Phong shading, geometría procedural

 Instalación

```bash
# Clonar el repositorio
git clone [url-del-repo]
cd llanta-f1

# Instalar dependencias
pip install pygame PyOpenGL PyOpenGL_accelerate numpy
```

 Uso

```bash
python main.py
```

 Controles

Iluminación

| Tecla         | Acción                              |
| ------------- | ------------------------------------ |
| `L`         | Modo LINTERNA FIJA (sigue cámara)   |
| `K`         | Modo LINTERNA LIBRE (control manual) |
| `N`         | Volver a luz NORMAL                  |
| `1-6`       | Cambiar color de luz                 |
| `[` / `]` | Ajustar apertura del spotlight       |

Temas

| Tecla | Acción             |
| ----- | ------------------- |
| `T` | Cambiar tema visual |

Renderizado

| Tecla | Acción        |
| ----- | -------------- |
| `W` | Modo SÓLIDO   |
| `E` | Modo WIREFRAME |
| `Q` | Modo MIXTO     |

Clipping

| Tecla           | Acción                         |
| --------------- | ------------------------------- |
| `↑` / `↓` | Mover plano de corte            |
| `C`           | Toggle clipping ON/OFF          |
| `V`           | Toggle visualización del plano |

Animación

| Tecla         | Acción                        |
| ------------- | ------------------------------ |
| `SPACE`     | Toggle rotación automática   |
| `+` / `-` | Ajustar velocidad de rotación |

Vista

| Control               | Acción                         |
| --------------------- | ------------------------------- |
| `Click Izq + Mouse` | Rotar vista                     |
| `Click Der + Mouse` | Controlar linterna (modo libre) |
| `Rueda`             | Zoom in/out                     |
| `P`                 | Toggle piso                     |
| `R`                 | Resetear vista                  |
| `ESC`               | Salir                           |

 Estructura del Proyecto

```
llanta-f1/
│
├── main.py              # Programa principal y loop de renderizado
├── geometry.py          # Generación de geometría procedural
├── materials.py         # Definición de materiales y temas
├── lighting.py          # Modelos de iluminación (Phong + Spotlight)
├── rendering.py         # Funciones de dibujado OpenGL
├── clipping.py          # Algoritmo Sutherland-Hodgman
├── transforms.py        # Transformaciones con matrices homogéneas
└── README.md           # Este archivo
```

 Algoritmos Implementados

Sutherland-Hodgman (clipping.py)

Algoritmo de clipping de polígonos contra planos arbitrarios:

1. Para cada arista del polígono
2. Clasifica vértices (dentro/fuera del plano)
3. Calcula intersecciones con el plano
4. Construye nuevo polígono recortado

Phong Shading (lighting.py)

Modelo de iluminación con tres componentes:

- Ambiental: Luz uniforme base
- Difusa: Iluminación Lambertiana (N·L)
- Especular: Reflexión brillante (R·V)^shininess

Spotlight (lighting.py)

Iluminación cónica con:

- Cálculo de ángulo entre dirección de luz y punto
- Falloff suave en los bordes
- Atenuación por distancia

 Conceptos Demostrados

- Geometría 3D: Generación procedural de primitivas (cilindros, toroides)
- Álgebra Lineal: Transformaciones con matrices homogéneas 4×4
- Gráficas por Computadora: Pipeline de renderizado, clipping, iluminación
- Algoritmos Geométricos: Sutherland-Hodgman, cálculo de normales
- Arquitectura de Software: Modularización, separación de responsabilidades

 Notas Técnicas

Coordenadas Homogéneas

El proyecto utiliza coordenadas homogéneas (x, y, z, w) para permitir transformaciones afines mediante multiplicación matricial.

Normalización de Normales

Todas las normales se normalizan antes de los cálculos de iluminación para garantizar resultados correctos.

Triangulación

Los polígonos resultantes del clipping se triangulan usando fan triangulation desde el primer vértice.

 Autor

Brandon David Aguilar Cabadas

Versión: 5.1
Última actualización: Enero 2025
Python: 3.x
Estado:  Funcional y completo
