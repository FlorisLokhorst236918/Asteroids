import arcade
import math
import random
from constants import *


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS

        angle_rad = math.radians(angle)
        self.vx = math.cos(angle_rad) * BULLET_SPEED
        self.vy = math.sin(angle_rad) * BULLET_SPEED
        self.life = BULLET_LIFE

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.WHITE)


class Asteroid:
    def __init__(self, x, y, size, wave=1):
        self.x = x
        self.y = y
        self.size = size

        if size == "large":
            self.radius = ASTEROID_LARGE_RADIUS
        elif size == "medium":
            self.radius = ASTEROID_MEDIUM_RADIUS
        else:
            self.radius = ASTEROID_SMALL_RADIUS

        speed_multiplier = 1 + (wave - 1) * 0.1
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, ASTEROID_BASE_SPEED) * speed_multiplier
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.shape = self.generate_shape()

    def generate_shape(self):
        points = []
        num_points = random.randint(8, 12)

        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            distance = self.radius * random.uniform(0.7, 1.0)
            point_x = math.cos(angle) * distance
            point_y = math.sin(angle) * distance
            points.append((point_x, point_y))

        return points

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x > SCREEN_WIDTH + self.radius:
            self.x = -self.radius
        elif self.x < -self.radius:
            self.x = SCREEN_WIDTH + self.radius

        if self.y > SCREEN_HEIGHT + self.radius:
            self.y = -self.radius
        elif self.y < -self.radius:
            self.y = SCREEN_HEIGHT + self.radius

    def draw(self):
        world_points = []
        for point_x, point_y in self.shape:
            world_x = self.x + point_x
            world_y = self.y + point_y
            world_points.append((world_x, world_y))

        arcade.draw_polygon_outline(world_points, arcade.color.WHITE, 2)


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 90
        self.vx = 0
        self.vy = 0
        self.radius = SHIP_RADIUS
        self.thrust_on = False
        self.invulnerable = 0

    def rotate_left(self):
        self.angle += SHIP_TURN_SPEED

    def rotate_right(self):
        self.angle -= SHIP_TURN_SPEED

    def thrust(self):
        angle_rad = math.radians(self.angle)
        self.vx += math.cos(angle_rad) * SHIP_THRUST
        self.vy += math.sin(angle_rad) * SHIP_THRUST

    def update(self):
        self.vx *= SHIP_DRAG
        self.vy *= SHIP_DRAG

        self.x += self.vx
        self.y += self.vy

        if self.x > SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH

        if self.y > SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT

        if self.invulnerable > 0:
            self.invulnerable -= 1

    def draw(self):
        if self.invulnerable > 0 and (self.invulnerable // 10) % 2 == 0:
            return

        angle_rad = math.radians(self.angle)

        point1_x = self.x + math.cos(angle_rad) * self.radius
        point1_y = self.y + math.sin(angle_rad) * self.radius

        point2_x = self.x + math.cos(angle_rad + 2.5) * self.radius
        point2_y = self.y + math.sin(angle_rad + 2.5) * self.radius

        point3_x = self.x + math.cos(angle_rad - 2.5) * self.radius
        point3_y = self.y + math.sin(angle_rad - 2.5) * self.radius

        arcade.draw_triangle_filled(
            point1_x, point1_y,
            point2_x, point2_y,
            point3_x, point3_y,
            arcade.color.WHITE
        )
