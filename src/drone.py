import math
from primitives import (
    drawPolygon, drawCircle, DrawLineBresenham, 
    scanline_fill
)
from transforms import get_rotation_matrix, apply_transform


def get_drone_parts():
    body = [
        (-40, 0),
        (-30, -20),
        (30, -20),
        (40, 0),
        (30, 15),
        (-30, 15),
    ]
    
    dome = [
        (-20, -20),
        (-10, -30),
        (10, -30),
        (20, -20),
    ]
    
    arm_left = [(-40, 0), (-55, 10), (-55, 10), (-55, 25)]
    arm_right = [(40, 0), (55, 10), (55, 10), (55, 25)]
    arm_center = [(0, 15), (0, 30)]
    
    circles = {
        'camera_left': (-15, -5, 6),
        'camera_right': (15, -5, 6),
        'pupil_left': (-15, -5, 3),
        'pupil_right': (15, -5, 3),
        'prop_left': (-55, 28, 5),
        'prop_right': (55, 28, 5),
        'prop_center': (0, 35, 6),
        'light': (0, -25, 4),
    }
    
    return {
        'body': body,
        'dome': dome,
        'arm_left': arm_left,
        'arm_right': arm_right,
        'arm_center': arm_center,
        'circles': circles
    }


def rotate_point(x, y, angle_degrees):
    rad = math.radians(angle_degrees)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    new_x = x * cos_a - y * sin_a
    new_y = x * sin_a + y * cos_a
    return new_x, new_y


def translate_points(points, tx, ty):
    return [(x + tx, y + ty) for x, y in points]


def rotate_points(points, angle):
    return [rotate_point(x, y, angle) for x, y in points]


def drawDrone(surface, x, y, angle, body_color, detail_color):
    parts = get_drone_parts()
    
    body = rotate_points(parts['body'], angle)
    body = translate_points(body, x, y)
    drawPolygon(surface, body, body_color)
    
    dome = rotate_points(parts['dome'], angle)
    dome = translate_points(dome, x, y)
    drawPolygon(surface, dome, detail_color)
    
    for arm_name in ['arm_left', 'arm_right', 'arm_center']:
        arm = parts[arm_name]
        rotated = rotate_points(arm, angle)
        translated = translate_points(rotated, x, y)
        for i in range(0, len(translated) - 1, 2):
            p1, p2 = translated[i], translated[i + 1]
            DrawLineBresenham(surface, int(p1[0]), int(p1[1]), 
                            int(p2[0]), int(p2[1]), body_color)
    
    circles = parts['circles']
    
    for name, (cx, cy, radius) in circles.items():
        rcx, rcy = rotate_point(cx, cy, angle)
        final_x, final_y = int(rcx + x), int(rcy + y)
        
        if 'pupil' in name:
            color = body_color
        elif 'light' in name:
            color = (255, 255, 100)
        else:
            color = detail_color
        
        drawCircle(surface, final_x, final_y, radius, color)


def drawDroneFilled(surface, x, y, angle, body_color, detail_color, fill_color):
    parts = get_drone_parts()
    
    body = rotate_points(parts['body'], angle)
    body = translate_points(body, x, y)
    body_int = [(int(px), int(py)) for px, py in body]
    scanline_fill(surface, body_int, fill_color)
    
    drawDrone(surface, x, y, angle, body_color, detail_color)
