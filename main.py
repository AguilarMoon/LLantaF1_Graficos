"""
PROYECTO: Llanta de F1
Versión 5.1: Spotlight + Temas de Color + Múltiples Luces
Programa principal
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Importar módulos del proyecto
from materials import (MATERIAL_GOMA, MATERIAL_METAL_DORADO, MATERIAL_METAL_OSCURO, 
                      MATERIAL_BANDA_ROJA, MATERIAL_TORNILLOS, 
                      MATERIAL_ANILLO_HUB, MATERIAL_DISCO_RELLENO, 
                      MATERIAL_SIDEWALL_MARCAS, get_material_neumatico,
                      TEMAS, COLORES_LUZ, get_tema, get_color_luz)
from clipping import PlanoClipping, recortar_malla_con_plano
from geometry import (generar_vertices_cilindro, generar_toroide, 
                     generar_radios_aerodinamicos, calcular_normales, generar_piso,
                     generar_banda_color_neumatico, generar_tornillos_hub, 
                     generar_anillo_central_hub, generar_disco_relleno,
                     generar_marcas_sidewall)
from rendering import (dibujar_malla_phong, dibujar_malla_spotlight, 
                      dibujar_wireframe, dibujar_plano_corte_z)
from transforms import (matriz_rotacion_x, aplicar_transformacion)


def main():
    # Inicializar Pygame y OpenGL
    pygame.init()
    display = (1200, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("🏎️ Llanta F1 - V5.1: SPOTLIGHT + TEMAS")
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (1200/900), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -20)
    
    glEnable(GL_DEPTH_TEST)
    
    # 🎨 Tema inicial: OSCURO
    tema_actual = 'oscuro'
    tema_config = get_tema(tema_actual)
    glClearColor(*tema_config['fondo'], 1.0)
    
    print("\n" + "="*70)
    print("🏎️  LLANTA F1 V5.1 - SPOTLIGHT + TEMAS DE COLOR")
    print("="*70)
    
    print("\n🔧 Generando geometría F1 realista...")
    
    # Neumático
    vertices_neumatico_orig, caras_neumatico_orig = generar_toroide(
        radio_mayor=2.8, radio_menor=0.5, segmentos_mayor=64, segmentos_menor=24
    )
    
    # Banda Pirelli
    vertices_banda_orig, caras_banda_orig = generar_banda_color_neumatico(
        radio_mayor=2.8, radio_menor=0.5, posicion_y=0.0, ancho_banda=0.15, segmentos=64
    )
    
    # Rin
    vertices_rin_orig, caras_rin_orig = generar_vertices_cilindro(2.2, 0.85, 64)
    
    # Radios aerodinámicos
    vertices_radios_orig, caras_radios_orig = generar_radios_aerodinamicos(
        radio_interno=0.9, radio_externo=2.1, altura=0.8, num_radios=10
    )
    
    # Centro
    vertices_centro_orig, caras_centro_orig = generar_vertices_cilindro(0.8, 0.75, 32)
    
    # Tornillos
    vertices_tornillos_orig, caras_tornillos_orig = generar_tornillos_hub(
        radio=0.5, altura=0.8, num_tornillos=5
    )
    
    # Anillo decorativo
    vertices_anillo_orig, caras_anillo_orig = generar_anillo_central_hub(
        radio_interno=0.65, radio_externo=0.77, altura=0.78, segmentos=32
    )
    
    # Disco relleno
    vertices_relleno_orig, caras_relleno_orig = generar_disco_relleno(
        radio_interno=2.2, radio_externo=2.8, altura=0.85, segmentos=64
    )
    
    # Marcas sidewall
    vertices_sidewall_orig, caras_sidewall_orig = generar_marcas_sidewall(
        radio_mayor=2.8, radio_menor=0.5, num_marcas=12
    )
    
    # Rotar geometría 90° en X
    matriz_correccion = matriz_rotacion_x(90)
    vertices_neumatico_orig = aplicar_transformacion(vertices_neumatico_orig, matriz_correccion)
    vertices_banda_orig = aplicar_transformacion(vertices_banda_orig, matriz_correccion)
    vertices_rin_orig = aplicar_transformacion(vertices_rin_orig, matriz_correccion)
    vertices_centro_orig = aplicar_transformacion(vertices_centro_orig, matriz_correccion)
    vertices_radios_orig = aplicar_transformacion(vertices_radios_orig, matriz_correccion)
    vertices_tornillos_orig = aplicar_transformacion(vertices_tornillos_orig, matriz_correccion)
    vertices_anillo_orig = aplicar_transformacion(vertices_anillo_orig, matriz_correccion)
    vertices_relleno_orig = aplicar_transformacion(vertices_relleno_orig, matriz_correccion)
    vertices_sidewall_orig = aplicar_transformacion(vertices_sidewall_orig, matriz_correccion)
    
    # Generar piso
    vertices_piso, caras_piso = generar_piso(ancho=15, profundidad=15, posicion_y=-3.5)
    
    print("\n" + "="*70)
    print("✅ GEOMETRÍA F1 REALISTA GENERADA")
    print("="*70)
    print("\n🎮 CONTROLES:")
    print("\n💡 ILUMINACIÓN:")
    print("   [L] - Modo LINTERNA fija 🔦 (apunta al centro)")
    print("   [K] - Modo LINTERNA LIBRE 🎯 (controlas con mouse)")
    print("   [1-6] - Cambiar color de luz (blanca/roja/azul/amarilla/verde/morada)")
    print("   [[/]] - Ajustar apertura del spotlight")
    print("   [N] - Volver a luz NORMAL")
    print("\n🎨 TEMAS:")
    print("   [T] - Cambiar tema (Oscuro/Negro/Garage/Claro)")
    print("\n🖼️ RENDERIZADO:")
    print("   [W] - Modo SÓLIDO (Phong shading)")
    print("   [E] - Modo WIREFRAME")
    print("   [Q] - Modo MIXTO")
    print("\n✂️ CLIPPING:")
    print("   [↑/↓] - Mover plano de corte")
    print("   [C] - Toggle clipping ON/OFF")
    print("   [V] - Toggle visualización del plano")
    print("\n🎬 ANIMACIÓN:")
    print("   [SPACE] - Toggle rotación")
    print("   [+/-] - Velocidad de rotación")
    print("\n🎮 VISTA:")
    print("   [P] - Toggle piso ON/OFF")
    print("   [Mouse + Click Izq] - Rotar vista (modo normal)")
    print("   [Mouse + Click Der] - Controlar linterna (modo linterna libre)")
    print("   [Rueda] - Zoom")
    print("   [R] - Resetear vista")
    print("   [ESC] - Salir")
    print("="*70 + "\n")
    
    # Variables de control
    angulo_x = 20
    angulo_y = 45
    zoom = -20
    mouse_down_left = False
    mouse_down_right = False
    last_mouse_x, last_mouse_y = 0, 0
    
    modo_render = "solido"
    clipping_activo = True
    mostrar_plano = True
    posicion_corte = 0.0
    
    animacion_activa = False
    angulo_rotacion_llanta = 0.0
    velocidad_rotacion = 2.0
    
    mostrar_piso = True
    
    # 🔦 NUEVO: Variables de iluminación
    modo_luz = "normal"  # "normal", "linterna", o "linterna_libre"
    color_luz_actual = 'blanca'
    apertura_spotlight = 20.0
    suavizado_spotlight = 5.0
    
    # 🎯 NUEVO: Control de linterna libre
    luz_libre_activa = False
    angulo_luz_x = 0.0  # Ángulo vertical de la luz
    angulo_luz_y = 0.0  # Ángulo horizontal de la luz
    
    # Copias de trabajo
    vertices_neumatico = vertices_neumatico_orig.copy()
    caras_neumatico = caras_neumatico_orig.copy()
    vertices_banda = vertices_banda_orig.copy()
    caras_banda = caras_banda_orig.copy()
    vertices_rin = vertices_rin_orig.copy()
    caras_rin = caras_rin_orig.copy()
    vertices_centro = vertices_centro_orig.copy()
    caras_centro = caras_centro_orig.copy()
    vertices_radios = vertices_radios_orig.copy()
    caras_radios = caras_radios_orig.copy()
    vertices_tornillos = vertices_tornillos_orig.copy()
    caras_tornillos = caras_tornillos_orig.copy()
    vertices_anillo = vertices_anillo_orig.copy()
    caras_anillo = caras_anillo_orig.copy()
    vertices_relleno = vertices_relleno_orig.copy()
    caras_relleno = caras_relleno_orig.copy()
    vertices_sidewall = vertices_sidewall_orig.copy()
    caras_sidewall = caras_sidewall_orig.copy()
    
    clock = pygame.time.Clock()
    running = True
    
    # Bucle principal
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Modos de render
                elif event.key == pygame.K_w:
                    modo_render = "solido"
                    print("🎨 Modo: SÓLIDO (Phong)")
                elif event.key == pygame.K_e:
                    modo_render = "wireframe"
                    print("🔲 Modo: WIREFRAME")
                elif event.key == pygame.K_q:
                    modo_render = "mixto"
                    print("🎨🔲 Modo: MIXTO")
                
                # 🔦 NUEVO: Controles de iluminación
                elif event.key == pygame.K_l:
                    modo_luz = "linterna"
                    luz_libre_activa = False
                    print(f"🔦 Luz: LINTERNA FIJA (apunta al centro)")
                elif event.key == pygame.K_k:
                    modo_luz = "linterna_libre"
                    luz_libre_activa = True
                    print(f"🎯 Luz: LINTERNA LIBRE (usa click derecho para apuntar)")
                elif event.key == pygame.K_n:
                    modo_luz = "normal"
                    luz_libre_activa = False
                    print(f"💡 Luz: NORMAL")
                
                # Cambiar color de luz (teclas 1-6)
                elif event.key == pygame.K_1:
                    color_luz_actual = 'blanca'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                elif event.key == pygame.K_2:
                    color_luz_actual = 'roja'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                elif event.key == pygame.K_3:
                    color_luz_actual = 'azul'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                elif event.key == pygame.K_4:
                    color_luz_actual = 'amarilla'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                elif event.key == pygame.K_5:
                    color_luz_actual = 'verde'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                elif event.key == pygame.K_6:
                    color_luz_actual = 'morada'
                    print(f"💡 Luz: {COLORES_LUZ[color_luz_actual]['nombre']}")
                
                # Ajustar apertura del spotlight
                elif event.key == pygame.K_LEFTBRACKET:  # [
                    apertura_spotlight = max(5.0, apertura_spotlight - 2.0)
                    print(f"🔦 Apertura: {apertura_spotlight:.0f}°")
                elif event.key == pygame.K_RIGHTBRACKET:  # ]
                    apertura_spotlight = min(45.0, apertura_spotlight + 2.0)
                    print(f"🔦 Apertura: {apertura_spotlight:.0f}°")
                
                # 🎨 NUEVO: Cambiar tema
                elif event.key == pygame.K_t:
                    temas_lista = list(TEMAS.keys())
                    idx = (temas_lista.index(tema_actual) + 1) % len(temas_lista)
                    tema_actual = temas_lista[idx]
                    tema_config = get_tema(tema_actual)
                    glClearColor(*tema_config['fondo'], 1.0)
                    print(f"🎨 Tema: {tema_config['nombre']}")
                
                # Clipping
                elif event.key == pygame.K_UP:
                    posicion_corte += 0.1
                    print(f"✂️ Plano: Z = {posicion_corte:.2f}")
                elif event.key == pygame.K_DOWN:
                    posicion_corte -= 0.1
                    print(f"✂️ Plano: Z = {posicion_corte:.2f}")
                elif event.key == pygame.K_c:
                    clipping_activo = not clipping_activo
                    print(f"✂️ Clipping: {'ON' if clipping_activo else 'OFF'}")
                elif event.key == pygame.K_v:
                    mostrar_plano = not mostrar_plano
                    print(f"👁️ Plano: {'VISIBLE' if mostrar_plano else 'OCULTO'}")
                
                # Animación
                elif event.key == pygame.K_SPACE:
                    animacion_activa = not animacion_activa
                    print(f"🎬 Animación: {'ON' if animacion_activa else 'OFF'}")
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    velocidad_rotacion += 0.5
                    print(f"⚡ Velocidad: {velocidad_rotacion:.1f}°/f")
                elif event.key == pygame.K_MINUS:
                    velocidad_rotacion = max(0.5, velocidad_rotacion - 0.5)
                    print(f"⚡ Velocidad: {velocidad_rotacion:.1f}°/f")
                
                # Otros
                elif event.key == pygame.K_p:
                    mostrar_piso = not mostrar_piso
                    print(f"🏁 Piso: {'ON' if mostrar_piso else 'OFF'}")
                elif event.key == pygame.K_r:
                    angulo_x, angulo_y, zoom = 20, 45, -20
                    angulo_rotacion_llanta = 0.0
                    angulo_luz_x, angulo_luz_y = 0.0, 0.0  # 🎯 Reset luz también
                    print("🔄 Vista reseteada")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    mouse_down_left = True
                    last_mouse_x, last_mouse_y = event.pos
                elif event.button == 3:  # Click derecho
                    mouse_down_right = True
                    last_mouse_x, last_mouse_y = event.pos
                elif event.button == 4:
                    zoom += 1
                elif event.button == 5:
                    zoom -= 1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down_left = False
                elif event.button == 3:
                    mouse_down_right = False
            
            elif event.type == pygame.MOUSEMOTION:
                dx = event.pos[0] - last_mouse_x
                dy = event.pos[1] - last_mouse_y
                
                # Click izquierdo: rotar vista (siempre)
                if mouse_down_left:
                    angulo_y += dx * 0.5
                    angulo_x += dy * 0.5
                
                # Click derecho: controlar linterna (solo en modo libre)
                if mouse_down_right and luz_libre_activa:
                    angulo_luz_y += dx * 0.5
                    angulo_luz_x += dy * 0.5
                
                last_mouse_x, last_mouse_y = event.pos
        
        # Actualizar animación
        if animacion_activa:
            angulo_rotacion_llanta += velocidad_rotacion
            if angulo_rotacion_llanta >= 360:
                angulo_rotacion_llanta -= 360
        
        # Aplicar clipping
        if clipping_activo:
            plano = PlanoClipping(0, 0, 1, -posicion_corte)
            
            vertices_neumatico, caras_neumatico = recortar_malla_con_plano(
                vertices_neumatico_orig, caras_neumatico_orig, plano)
            vertices_banda, caras_banda = recortar_malla_con_plano(
                vertices_banda_orig, caras_banda_orig, plano)
            vertices_rin, caras_rin = recortar_malla_con_plano(
                vertices_rin_orig, caras_rin_orig, plano)
            vertices_centro, caras_centro = recortar_malla_con_plano(
                vertices_centro_orig, caras_centro_orig, plano)
            vertices_radios, caras_radios = recortar_malla_con_plano(
                vertices_radios_orig, caras_radios_orig, plano)
            vertices_tornillos, caras_tornillos = recortar_malla_con_plano(
                vertices_tornillos_orig, caras_tornillos_orig, plano)
            vertices_anillo, caras_anillo = recortar_malla_con_plano(
                vertices_anillo_orig, caras_anillo_orig, plano)
            vertices_relleno, caras_relleno = recortar_malla_con_plano(
                vertices_relleno_orig, caras_relleno_orig, plano)
            vertices_sidewall, caras_sidewall = recortar_malla_con_plano(
                vertices_sidewall_orig, caras_sidewall_orig, plano)
        else:
            vertices_neumatico = vertices_neumatico_orig
            caras_neumatico = caras_neumatico_orig
            vertices_banda = vertices_banda_orig
            caras_banda = caras_banda_orig
            vertices_rin = vertices_rin_orig
            caras_rin = caras_rin_orig
            vertices_centro = vertices_centro_orig
            caras_centro = caras_centro_orig
            vertices_radios = vertices_radios_orig
            caras_radios = caras_radios_orig
            vertices_tornillos = vertices_tornillos_orig
            caras_tornillos = caras_tornillos_orig
            vertices_anillo = vertices_anillo_orig
            caras_anillo = caras_anillo_orig
            vertices_relleno = vertices_relleno_orig
            caras_relleno = caras_relleno_orig
            vertices_sidewall = vertices_sidewall_orig
            caras_sidewall = caras_sidewall_orig
        
        # Calcular normales
        normales_neumatico = calcular_normales(vertices_neumatico, caras_neumatico)
        normales_banda = calcular_normales(vertices_banda, caras_banda)
        normales_rin = calcular_normales(vertices_rin, caras_rin)
        normales_centro = calcular_normales(vertices_centro, caras_centro)
        normales_radios = calcular_normales(vertices_radios, caras_radios)
        normales_tornillos = calcular_normales(vertices_tornillos, caras_tornillos)
        normales_anillo = calcular_normales(vertices_anillo, caras_anillo)
        normales_relleno = calcular_normales(vertices_relleno, caras_relleno)
        normales_sidewall = calcular_normales(vertices_sidewall, caras_sidewall)
        
        if mostrar_piso:
            normales_piso = calcular_normales(vertices_piso, caras_piso)
        
        # Renderizar
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(angulo_x, 1, 0, 0)
        glRotatef(angulo_y, 0, 1, 0)
        
        # 💡 Configurar luz según modo
        camara_pos = np.array([0.0, 0.0, -zoom])
        luz_color = get_color_luz(color_luz_actual)
        
        # 🎯 Calcular posición y dirección de la luz según el modo
        if modo_luz == "linterna":
            # 🔦 Modo linterna fija: luz sale DESDE la cámara hacia adelante
            # La luz está en la posición de la cámara
            luz_pos = camara_pos.copy()
            
            # Dirección: hacia donde mira la cámara (considerando rotaciones)
            # Calcular vector "adelante" considerando las rotaciones de la vista
            rad_x = np.radians(angulo_x)
            rad_y = np.radians(angulo_y)
            
            # Vector adelante después de aplicar rotaciones (dirección de vista)
            luz_dir = np.array([
                np.sin(np.radians(angulo_y)),
                -np.sin(np.radians(angulo_x)),
                np.cos(np.radians(angulo_y)) * np.cos(np.radians(angulo_x))
            ])
            luz_dir = luz_dir / np.linalg.norm(luz_dir)
            
        elif luz_libre_activa:
            # 🎯 Modo linterna libre: luz desde arriba, dirección controlable
            luz_pos = np.array([10.0, 10.0, 10.0])
            
            # Calcular dirección desde ángulos (más sensible)
            rad_x = np.radians(angulo_luz_x)
            rad_y = np.radians(angulo_luz_y)
            
            luz_dir = np.array([
                np.sin(rad_y) * np.cos(rad_x),
                -np.sin(rad_x),
                -np.cos(rad_y) * np.cos(rad_x)
            ])
            luz_dir = luz_dir / np.linalg.norm(luz_dir)
        else:
            # 💡 Modo normal: luz estática desde arriba
            luz_pos = np.array([10.0, 10.0, 10.0])
            luz_dir = np.array([0.0, 0.0, -1.0])
        
        # Plano de corte
        if mostrar_plano and clipping_activo:
            dibujar_plano_corte_z(posicion_corte)
        
        # Piso
        if mostrar_piso:
            material_piso = tema_config['piso']
            if modo_render == "solido" or modo_render == "mixto":
                if modo_luz in ["linterna", "linterna_libre"]:
                    dibujar_malla_spotlight(vertices_piso, caras_piso, normales_piso,
                                          material_piso, luz_pos, luz_dir, camara_pos,
                                          luz_color, apertura=apertura_spotlight,
                                          suavizado=suavizado_spotlight)
                else:
                    dibujar_malla_phong(vertices_piso, caras_piso, normales_piso,
                                       material_piso, luz_pos, camara_pos, luz_color)
            if modo_render == "wireframe" or modo_render == "mixto":
                dibujar_wireframe(vertices_piso, caras_piso, [0.3, 0.3, 0.3], 2.0)
        
        # Llanta con rotación
        glPushMatrix()
        glRotatef(angulo_rotacion_llanta, 0, 0, 1)
        
        componentes = [
            (vertices_neumatico, caras_neumatico, normales_neumatico, MATERIAL_GOMA,
             [0.0, 1.0, 0.0], [0.0, 0.5, 0.0]),
            (vertices_banda, caras_banda, normales_banda, MATERIAL_BANDA_ROJA,
             [1.0, 0.0, 0.0], [0.6, 0.0, 0.0]),
            (vertices_rin, caras_rin, normales_rin, MATERIAL_METAL_DORADO,
             [1.0, 1.0, 0.0], [0.6, 0.6, 0.0]),
            (vertices_relleno, caras_relleno, normales_relleno, MATERIAL_DISCO_RELLENO,
             [0.7, 0.6, 0.2], [0.5, 0.4, 0.15]),
            (vertices_sidewall, caras_sidewall, normales_sidewall, MATERIAL_SIDEWALL_MARCAS,
             [0.9, 0.9, 0.9], [0.6, 0.6, 0.6]),
            (vertices_radios, caras_radios, normales_radios, MATERIAL_METAL_DORADO,
             [1.0, 1.0, 0.0], [0.6, 0.6, 0.0]),
            (vertices_anillo, caras_anillo, normales_anillo, MATERIAL_ANILLO_HUB,
             [0.8, 0.7, 0.3], [0.5, 0.4, 0.2]),
            (vertices_centro, caras_centro, normales_centro, MATERIAL_METAL_OSCURO,
             [0.5, 0.5, 0.5], [0.3, 0.3, 0.3]),
            (vertices_tornillos, caras_tornillos, normales_tornillos, MATERIAL_TORNILLOS,
             [0.6, 0.6, 0.6], [0.4, 0.4, 0.4]),
        ]
        
        for verts, faces, norms, mat, wire_pure, wire_mixed in componentes:
            if len(faces) > 0:
                if modo_render == "solido" or modo_render == "mixto":
                    if modo_luz in ["linterna", "linterna_libre"]:
                        dibujar_malla_spotlight(verts, faces, norms, mat, 
                                              luz_pos, luz_dir, camara_pos, luz_color,
                                              apertura=apertura_spotlight,
                                              suavizado=suavizado_spotlight)
                    else:
                        dibujar_malla_phong(verts, faces, norms, mat, 
                                          luz_pos, camara_pos, luz_color)
                
                if modo_render == "wireframe" or modo_render == "mixto":
                    color = wire_pure if modo_render == "wireframe" else wire_mixed
                    dibujar_wireframe(verts, faces, color, 1.5)
        
        glPopMatrix()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n👋 Programa finalizado\n")


if __name__ == "__main__":
    main()