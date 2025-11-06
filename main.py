import arcade
import math
import random
import os
import sys
from constants import *
from entities import Ship, Asteroid, Bullet
from game_data import GameData
from utils import check_collision


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class AsteroidsGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.game_state = "MENU"
        self.player_name = ""
        self.just_switched_to_menu = False

        self.game_data = GameData()
        self.load_sounds()

    def load_sounds(self):
        self.sounds = {}
        sound_files = {
            'shoot': 'sounds/shoot.wav',
            'explode': 'sounds/explode.wav',
            'hit': 'sounds/hit.wav'
        }

        for sound_name, filepath in sound_files.items():
            try:
                full_path = resource_path(filepath)
                if os.path.exists(full_path):
                    self.sounds[sound_name] = arcade.load_sound(full_path)
                else:
                    self.sounds[sound_name] = None
            except:
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            arcade.play_sound(self.sounds[sound_name])

    def setup(self):
        self.score = 0
        self.game_time = 0
        self.lives = 3
        self.asteroids_destroyed = 0
        self.wave = 1

        self.ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False

        self.asteroids = []
        self.spawn_asteroids(STARTING_ASTEROIDS)

        self.bullets = []
        self.game_state = "PLAYING"

    def spawn_asteroids(self, count):
        for _ in range(count):
            while True:
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)

                dx = x - self.ship.x
                dy = y - self.ship.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance > 150:
                    self.asteroids.append(Asteroid(x, y, "large", self.wave))
                    break

    def shoot(self):
        angle_rad = math.radians(self.ship.angle)
        bullet_x = self.ship.x + math.cos(angle_rad) * self.ship.radius
        bullet_y = self.ship.y + math.sin(angle_rad) * self.ship.radius

        bullet = Bullet(bullet_x, bullet_y, self.ship.angle)
        self.bullets.append(bullet)
        self.play_sound('shoot')

    def on_draw(self):
        self.clear()

        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "PLAYING":
            self.draw_game()
        elif self.game_state == "PAUSED":
            self.draw_game()
            self.draw_pause_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game()
            self.draw_game_over()

    def draw_menu(self):
        arcade.draw_text("ASTEROIDS", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                        arcade.color.WHITE, 64, anchor_x="center", bold=True)

        highscore = self.game_data.get_highscore()
        highscore_player = self.game_data.get_highscore_player()
        if highscore > 0 and highscore_player:
            arcade.draw_text(f"HIGH SCORE: {highscore} by {highscore_player}",
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                            arcade.color.GOLD, 20, anchor_x="center", bold=True)

        arcade.draw_text("Enter your name:", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10,
                        arcade.color.WHITE, 24, anchor_x="center")

        display_name = self.player_name + "_"
        arcade.draw_text(display_name, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                        arcade.color.YELLOW, 28, anchor_x="center", bold=True)

        arcade.draw_text("Press ENTER to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                        arcade.color.GREEN, 18, anchor_x="center")

        arcade.draw_text("Controls: W=Thrust, A/D=Rotate, SPACE=Shoot, ESC=Pause",
                        SCREEN_WIDTH // 2, 50,
                        arcade.color.GRAY, 14, anchor_x="center")

    def draw_pause_menu(self):
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH,
            0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        arcade.draw_text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80,
                        arcade.color.YELLOW, 48, anchor_x="center", bold=True)

        arcade.draw_text("ESC - Resume Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10,
                        arcade.color.WHITE, 24, anchor_x="center")

        arcade.draw_text("R - Restart Game", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                        arcade.color.WHITE, 24, anchor_x="center")

        arcade.draw_text("M - Back to Menu", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 70,
                        arcade.color.WHITE, 24, anchor_x="center")

    def draw_game(self):
        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

        if self.game_state == "PLAYING":
            self.ship.draw()

        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30,
                        arcade.color.WHITE, 16)

        arcade.draw_text(f"Wave: {self.wave}", 10, SCREEN_HEIGHT - 55,
                        arcade.color.CYAN, 16)

        arcade.draw_text(f"Lives: {self.lives}", 10, SCREEN_HEIGHT - 80,
                        arcade.color.WHITE, 16)

        arcade.draw_text(f"Time: {int(self.game_time)}s", SCREEN_WIDTH - 120,
                        SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

    def draw_game_over(self):
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH,
            0, SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                        arcade.color.RED, 48, anchor_x="center", bold=True)

        arcade.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 + 50,
                        arcade.color.WHITE, 32, anchor_x="center")

        highscore = self.game_data.get_highscore()
        if self.score >= highscore and self.score > 0:
            arcade.draw_text("NEW HIGH SCORE!", SCREEN_WIDTH // 2,
                            SCREEN_HEIGHT // 2 + 10,
                            arcade.color.GOLD, 24, anchor_x="center", bold=True)

        arcade.draw_text(f"Player: {self.player_name}", SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 - 20,
                        arcade.color.WHITE, 20, anchor_x="center")

        arcade.draw_text(f"Time: {int(self.game_time)}s | Asteroids: {self.asteroids_destroyed}",
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                        arcade.color.GRAY, 16, anchor_x="center")

        arcade.draw_text("Press R to Restart | Press M for Menu",
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90,
                        arcade.color.GREEN, 18, anchor_x="center")

    def on_update(self, delta_time):
        if self.just_switched_to_menu:
            self.just_switched_to_menu = False

        if self.game_state == "PLAYING":
            self.game_time += delta_time

            if self.left_pressed:
                self.ship.rotate_left()
            if self.right_pressed:
                self.ship.rotate_right()
            if self.up_pressed:
                self.ship.thrust()

            self.ship.update()

            for asteroid in self.asteroids:
                asteroid.update()

            for bullet in self.bullets[:]:
                bullet.update()
                if bullet.life <= 0:
                    self.bullets.remove(bullet)

            for bullet in self.bullets[:]:
                for asteroid in self.asteroids[:]:
                    if check_collision(bullet, asteroid):
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

                        if asteroid in self.asteroids:
                            self.asteroids.remove(asteroid)
                            self.asteroids_destroyed += 1
                            self.play_sound('explode')

                        if asteroid.size == "large":
                            self.score += SCORE_LARGE
                            self.asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", self.wave))
                            self.asteroids.append(Asteroid(asteroid.x, asteroid.y, "medium", self.wave))
                        elif asteroid.size == "medium":
                            self.score += SCORE_MEDIUM
                            self.asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", self.wave))
                            self.asteroids.append(Asteroid(asteroid.x, asteroid.y, "small", self.wave))
                        else:
                            self.score += SCORE_SMALL

                        break

            if self.ship.invulnerable == 0:
                for asteroid in self.asteroids:
                    if check_collision(self.ship, asteroid):
                        self.lives -= 1
                        self.play_sound('hit')
                        self.ship.invulnerable = SHIP_INVULNERABILITY_TIME

                        if self.lives <= 0:
                            self.game_data.save_session(
                                self.player_name,
                                self.score,
                                self.game_time,
                                self.asteroids_destroyed
                            )
                            self.game_state = "GAME_OVER"

                        break

            if len(self.asteroids) == 0:
                self.wave += 1
                asteroid_count = min(STARTING_ASTEROIDS + self.wave - 1, 10)
                self.spawn_asteroids(asteroid_count)

    def on_key_press(self, key, modifiers):
        if self.game_state == "MENU":
            if key == arcade.key.ENTER and len(self.player_name) > 0:
                self.setup()
            elif key == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]

        elif self.game_state == "PLAYING":
            if key == arcade.key.ESCAPE:
                self.game_state = "PAUSED"
                return

            if key == arcade.key.A:
                self.left_pressed = True
            if key == arcade.key.D:
                self.right_pressed = True
            if key == arcade.key.W:
                self.up_pressed = True

            if key == arcade.key.SPACE:
                self.shoot()

        elif self.game_state == "PAUSED":
            if key == arcade.key.ESCAPE:
                self.game_state = "PLAYING"
            elif key == arcade.key.R:
                self.setup()
            elif key == arcade.key.M:
                self.game_state = "MENU"
                self.just_switched_to_menu = True

        elif self.game_state == "GAME_OVER":
            if key == arcade.key.R:
                self.setup()
            elif key == arcade.key.M or key == arcade.key.ESCAPE:
                self.game_state = "MENU"
                self.just_switched_to_menu = True

    def on_text(self, text):
        if self.game_state == "MENU" and not self.just_switched_to_menu:
            if len(self.player_name) < 15 and (text.isalnum() or text == " "):
                self.player_name += text

    def on_key_release(self, key, modifiers):
        if self.game_state == "PLAYING":
            if key == arcade.key.A:
                self.left_pressed = False
            if key == arcade.key.D:
                self.right_pressed = False
            if key == arcade.key.W:
                self.up_pressed = False


def main():
    game = AsteroidsGame()
    arcade.run()


if __name__ == "__main__":
    main()
