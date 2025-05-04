import pygame
import time
import csv
from random import randint
from settings import *
from player import *
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites


class Game:
    _instance = None

    def __new__(cls, nickname, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Game, cls).__new__(cls, *args, **kwargs)
            cls._instance.nickname = nickname
        return cls._instance

    def __init__(self, nickname):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            pygame.init()
            self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('Time Runner')
            self.clock = pygame.time.Clock()
            self.running = True
            self.game_over_state = False
            self.nickname = nickname
            self.start_time = time.time()

            # Groups
            self.all_sprites = AllSprites()
            self.collision_sprites = pygame.sprite.Group()
            self.bullet_sprites = pygame.sprite.Group()
            self.enemy_sprites = pygame.sprite.Group()

            # Arrow timer
            self.can_shoot = True
            self.shoot_time = 0
            self.arrow_cooldown = 800

            # Setup
            self.load_images()
            self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'bullet.png')).convert_alpha()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot and self.player.ammo_count == 1:
            pos = self.arrow.rect.center + self.arrow.player_direction * 50
            Bullet(self.bullet_surf, pos, self.arrow.player_direction, (self.all_sprites, self.bullet_sprites), self.boss)
            self.player.ammo_count -= 1
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def arrow_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.arrow_cooldown:
                self.can_shoot = True

    def setup(self):
        map = load_pygame(join('data', 'maps', 'maplvl1', 'map1.tmx'))
        for layer_name in ['Ground1', 'Cliff2', 'Objects2', 'Objects1']:
            for x, y, image in map.get_layer_by_name(layer_name).tiles():
                Sprite((TILE_SIZE * x, TILE_SIZE * y), image, self.all_sprites)
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        for obj in map.get_layer_by_name('Spawns'):
            if obj.name == 'player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.arrow = Arrow(self.player, self.all_sprites)
            elif obj.name == 'enemy':
                enemy = Enemy((obj.x, obj.y), self.all_sprites, self.player, self.collision_sprites)
                self.enemy_sprites.add(enemy)
            elif obj.name == 'boss':
                self.boss = Boss((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def arrow_collision(self):
        for bullet in self.bullet_sprites:
            collided_enemies = pygame.sprite.spritecollide(bullet, self.enemy_sprites, True, pygame.sprite.collide_mask)
            if collided_enemies:
                bullet.kill()
            for enemy in collided_enemies:
                enemy.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.game_over_state = True
        if self.boss and pygame.sprite.collide_mask(self.player, self.boss):
            self.game_over_state = True

    def save_game_history(self, result):
        """Save the game history to a CSV file."""
        end_time = time.time()
        time_passed = round(end_time - self.start_time, 2)
        file_path = 'game_history.csv'
        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.nickname, time_passed, result])
        except FileNotFoundError:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Nickname', 'Time Passed (s)', 'Result'])
                writer.writerow([self.nickname, time_passed, result])

    def display_message(self, title, subtitle, instructions):
        font = pygame.font.SysFont('Impact', 150)
        instructions_font = pygame.font.SysFont('Impact', 50)

        title_text = font.render(title, True, (255, 151, 0))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))

        subtitle_text = instructions_font.render(subtitle, True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        instructions_text = instructions_font.render(instructions, True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))

        self.display_surface.fill((104, 117, 142))
        self.display_surface.blit(title_text, title_rect)
        self.display_surface.blit(subtitle_text, subtitle_rect)
        self.display_surface.blit(instructions_text, instructions_rect)
        pygame.display.update()

    def render_timer(self):
        elapsed_time = round(time.time() - self.start_time, 2)
        font = pygame.font.SysFont('Impact', 30)
        timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
        self.display_surface.blit(timer_text, (10, 10))

    def game_won(self):
        end_time = time.time()
        time_passed = round(end_time - self.start_time, 2)
        self.display_message("You Win!", f"Time: {time_passed} seconds", "Press R to Restart or Q to Quit")
        self.save_game_history("win")

    def game_over(self):
        end_time = time.time()
        time_passed = round(end_time - self.start_time, 2)
        self.display_message("Game Over!", f"Time: {time_passed} seconds", "Press R to Restart or Q to Quit")
        self.save_game_history("lose")

    def wait_for_restart(self):
        """Wait for the player to restart or quit."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

    def restart_game(self):
        self.game_over_state = False
        self.enemy_sprites.empty()
        self.all_sprites.empty()
        self.setup()
        self.running = True

    def run(self):
        """Main game loop."""
        while self.running:
            delta_time = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.game_over_state:
                self.game_over()
                self.wait_for_restart()
            elif self.boss and self.boss.health <= 0:
                self.game_won()
                self.wait_for_restart()
            else:
                self.arrow_timer()
                self.input()
                self.arrow_collision()
                self.player_collision()
                self.all_sprites.update(delta_time)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            if self.player:
                self.player.stamina_bar(self.display_surface)
                self.player.ammo_bar(self.display_surface)
            if self.boss:
                self.boss.health_bar(self.display_surface)

            # Render the timer
            self.render_timer()

            pygame.display.update()

        pygame.quit()


# Start the menu first, then start the game
if __name__ == "__main__":
    from main_menu import main_menu
    menu_result, nickname = main_menu()
    if menu_result == "start":
        game = Game(nickname)
        game.run()