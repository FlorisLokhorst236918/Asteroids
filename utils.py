import math


def check_collision(obj1, obj2):
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    distance = math.sqrt(dx**2 + dy**2)
    return distance < (obj1.radius + obj2.radius)
