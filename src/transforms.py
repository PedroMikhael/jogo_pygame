"""
Módulo de Transformações Geométricas
Funções para manipulação de matrizes e transformações 2D.
"""
import math
def mat_mul(A, B):
    """ Multiplies two 3x3 matrices. """
    C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                C[i][j] += A[i][k] * B[k][j]
    return C

def get_translation_matrix(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def get_rotation_matrix(angle_degrees):
    rad = math.radians(angle_degrees)
    c = math.cos(rad)
    s = math.sin(rad)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ]

def get_scale_matrix(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def apply_transform(points, matrix):
    new_points = []
    for x, y in points:
        vec = [x, y, 1]
        new_x = matrix[0][0]*vec[0] + matrix[0][1]*vec[1] + matrix[0][2]*vec[2]
        new_y = matrix[1][0]*vec[0] + matrix[1][1]*vec[1] + matrix[1][2]*vec[2]
        new_points.append((new_x, new_y))
    return new_points

def get_rotation_around_point_matrix(angle_degrees, cx, cy):
    """
    Cria matriz de rotação em torno de um ponto arbitrário (cx, cy).
    Processo: T(-cx,-cy) -> R(angle) -> T(cx,cy)
    """
    to_origin = get_translation_matrix(-cx, -cy)
    rotation = get_rotation_matrix(angle_degrees)
    back = get_translation_matrix(cx, cy)
    
    temp = mat_mul(rotation, to_origin)
    return mat_mul(back, temp)

def get_identity_matrix():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]



def get_window_to_viewport_matrix_pygame(janela, viewport):
    """
    Transforma coordenadas da janela (mundo) para viewport (tela).
    Versão SEM inversão de Y (para Pygame onde Y já cresce para baixo).
    """
    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport
    
    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin) 
    
    m = get_identity_matrix()
    m = mat_mul(get_translation_matrix(-Wxmin, -Wymin), m)
    m = mat_mul(get_scale_matrix(sx, sy), m)
    m = mat_mul(get_translation_matrix(Vxmin, Vymin), m)
    
    return m


