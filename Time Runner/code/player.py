from settings import *
from sprites import Arrow


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'boy.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-5, -30)

        # Movement
        self.direction = pygame.Vector2()
        self.default_speed = 300
        self.boosted_speed = 500
        self.speed = self.default_speed
        self.collision_sprites = collision_sprites

        # Stamina
        self.max_stamina = 50
        self.stamina = self.max_stamina
        self.stamina_depletion_rate = 20
        self.stamina_regeneration_rate = 5
        self.cooldown_time = 1.5
        self.cooldown_timer = 0

        # Ammo
        self.max_ammo = 1
        self.ammo_count = 1
        self.ammo_regeneration_rate = 0.5

    def input(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

        if keys[pygame.K_SPACE] and self.stamina > 0 and self.cooldown_timer == 0:
            self.speed = self.boosted_speed
            self.stamina -= self.stamina_depletion_rate * delta_time
        else:
            self.speed = self.default_speed
            self.stamina += self.stamina_regeneration_rate * delta_time

        if self.stamina <= 0:
            self.stamina = 0
            if self.cooldown_timer == 0:
                self.cooldown_timer = self.cooldown_time

        if self.cooldown_timer > 0:
            self.cooldown_timer -= delta_time
        if self.cooldown_timer <= 0 and self.stamina > 0:
            self.cooldown_timer = 0

        if self.ammo_count < 1:
            self.ammo_count += self.ammo_regeneration_rate * delta_time
        self.ammo_count = min(self.ammo_count, self.max_ammo)

        self.stamina = max(0, min(self.stamina, self.max_stamina))

    def move(self, delta_time):
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def render_bar(self, surface, x, y, bar_width, bar_height, current_value, max_value, bg_color, fg_color, label):
        # Background
        pygame.draw.rect(surface, bg_color, (x, y, bar_width, bar_height))

        # Foreground
        value_width = (current_value / max_value) * bar_width
        pygame.draw.rect(surface, fg_color, (x, y, value_width, bar_height))

        # Label
        font = pygame.font.SysFont('impact', 25)
        text = font.render(label, True, (255, 0, 0))
        text_rect = text.get_rect(center=(x + bar_width / 2, y + bar_height / 2))
        surface.blit(text, text_rect)

    def stamina_bar(self, surface):
        self.render_bar(
            surface=surface,
            x=WINDOW_WIDTH / 2 - 70,
            y=50,
            bar_width=150,
            bar_height=30,
            current_value=self.stamina,
            max_value=self.max_stamina,
            bg_color=(175, 95, 0),
            fg_color=(255, 151, 0),
            label="STAMINA"
        )

    def ammo_bar(self, surface):
        self.render_bar(
            surface=surface,
            x=WINDOW_WIDTH / 2 - 70,
            y=100,
            bar_width=150,
            bar_height=30,
            current_value=self.ammo_count,
            max_value=self.max_ammo,
            bg_color=(25, 135, 140),
            fg_color=(70, 230, 240),
            label="AMMO"
        )

    def update(self, delta_time):
        self.input(delta_time)
        self.move(delta_time)