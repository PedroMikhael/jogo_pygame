import math

def circle_collision(x1, y1, r1, x2, y2, r2):

    dx = x1 - x2
    dy = y1 - y2

    distance = math.sqrt(dx * dx + dy * dy)

    return distance <= (r1 + r2)
 