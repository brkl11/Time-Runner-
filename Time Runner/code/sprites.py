import pygame
from math import atan2, degrees
from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.distance = 50
        self.player_direction = pygame.Vector2(1, 0)
        self.arrow_surf = pygame.image.load(join('images', 'arrow.png')).convert_alpha()
        self.image = self.arrow_surf
        self.rect = self.image.get_rect(
            center=self.player.rect.center + self.player_direction * self.distance
        )

    def get_direction(self):
        """Calculate the direction of the arrow based on the mouse position."""
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_arrow(self):
        """Rotate the arrow to face the direction of the mouse."""
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) + 90
        self.image = pygame.transform.rotozoom(self.arrow_surf, angle, 1)

    def update(self, _):
        """Update the arrow's direction and position."""
        self.get_direction()
        self.rotate_arrow()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, boss=None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1500
        self.direction = direction
        self.speed = 600
        self.boss = boss

    def update(self, delta_time):
        """Update the bullet's position and check for collisions."""
        self.rect.center += self.direction * self.speed * delta_time
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()
        if self.boss and self.rect.colliderect(self.boss.rect):
            self.boss.take_damage(1)
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        self.image = pygame.image.load(join('images', 'slime.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 110

    def move(self, delta_time):
        """Move the enemy toward the player."""
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        """Handle collisions with other sprites."""
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    elif self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def update(self, delta_time):
        self.move(delta_time)


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'boss.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(30, 30)
        self.collision_sprites = collision_sprites
        self.health = 5
        self.max_health = 5

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def health_bar(self, surface):
        bar_width, bar_height = 150, 30
        x, y = WINDOW_WIDTH - 400, 50
        pygame.draw.rect(surface, (60, 10, 100), (x, y, bar_width, bar_height))
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(surface, (150, 60, 230), (x, y, health_width, bar_height))
        font = pygame.font.SysFont('Impact', 16)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + bar_width / 2, y + bar_height / 2))
        surface.blit(health_text, text_rect)
        boss_text = font.render("BOSS", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=(x + bar_width // 2, y - 15))
        surface.blit(boss_text, boss_text_rect)

    def update(self, delta_time):
        pass