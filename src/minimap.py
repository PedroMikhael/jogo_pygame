import pygame
from primitives import drawPolygon, scanline_fill, drawCircle

def draw_minimap(surface, x, y, width, height, map_zones, player_pos, map_width, map_height, objects_dict=None):
    """
    Desenha o minimapa na tela usando funções primitivas.
    """
    # Fundo do minimapa
    bg_points = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height)
    ]
    # Borda
    drawPolygon(surface, bg_points, (200, 200, 200))
    # Fundo semi-transparente (simulado com scanline de pontos alternados ou cor sólida por enquanto)
    # Como scanline_fill preenche tudo, vamos usar uma cor sólida escura
    scanline_fill(surface, bg_points, (0, 0, 0))

    # Escala
    scale_x = width / map_width
    scale_y = height / map_height

    # Desenha as zonas do mapa (limitadas ao minimapa)
    # map_zones é uma lista de polígonos (listas de pontos)
    for zone in map_zones:
        minimap_zone = []
        for px, py in zone:
            mx = x + int(px * scale_x)
            my = y + int(py * scale_y)
            # Clip simples para garantir que não desenhe fora (opcional, já que o mapa deve caber)
            mx = max(x, min(x + width, mx))
            my = max(y, min(y + height, my))
            minimap_zone.append((mx, my))
        
        # Desenha a zona
        if len(minimap_zone) >= 3:
            scanline_fill(surface, minimap_zone, (0, 100, 200)) # Azul claro para áreas navegáveis?
            # Ou usar a cor original se passada. Vamos assumir azul para "água/navegável" ou cinza se for parede.
            # No map.py, as zonas desenhadas são "Ocean Deep".
            # Vamos desenhar apenas o contorno ou preenchimento diferenciado.
            # Como o map.py desenha o "caminho" (ocean deep), vamos preencher com azul escuro
            scanline_fill(surface, minimap_zone, (40, 60, 100))

    # Desenha o jogador
    px, py = player_pos
    mx = x + int(px * scale_x)
    my = y + int(py * scale_y)
    
    # Marcador do jogador (Ponto verde ou amarelo)
    if x <= mx <= x + width and y <= my <= y + height:
        drawCircle(surface, mx, my, 3, (255, 255, 0))

    # Desenha objetivos (se houver)
    if objects_dict:
        # Base
        if 'base' in objects_dict:
            bx, by = objects_dict['base']
            mbx = x + int(bx * scale_x)
            mby = y + int(by * scale_y)
            drawCircle(surface, mbx, mby, 4, (0, 255, 0)) # Base Verde

        # Cápsulas (suporte para múltiplas)
        if 'capsules' in objects_dict:
            for cap in objects_dict['capsules']:
                if cap and not cap.get('collected', False):
                    cx, cy = cap['x'], cap['y']
                    mcx = x + int(cx * scale_x)
                    mcy = y + int(cy * scale_y)
                    drawCircle(surface, mcx, mcy, 3, (255, 0, 0)) # Cápsula Vermelha
        
        # Compatibilidade com cápsula única (legado)
        elif 'capsule' in objects_dict:
            cap = objects_dict['capsule']
            if cap and not cap.get('collected', False):
                cx, cy = cap['x'], cap['y']
                mcx = x + int(cx * scale_x)
                mcy = y + int(cy * scale_y)
                drawCircle(surface, mcx, mcy, 3, (255, 0, 0)) # Cápsula Vermelha

