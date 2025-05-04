# Coursework Report: Time Runner

## 1. Introduction

### Application Overview

**Time Runner** is a 2D action-adventure game built using Python and the Pygame library. The game challenges players to navigate through maze levels, defeat enemies, and face a boss, all while managing limited resources like stamina and ammo that requires realoading. **Time Runner** offers a challenging and engaging experience. Designed to be a fun and strategic adventure.

### How to Run the Program

To run the program, ensure that you have *Python*, *Pygame* _(pip install pygame)_ and *Tiled* _(pip install pytmx)_ installed on your system as well as all of the additional *.png* files and *Python* scripts in one directory. Then, execute the **main.py** script using *Python*.

### How to Use the Program

- In main menu enter your **NICKNAME** and press **START GAME** or **ENTER** to start playing or press **QUIT** to exit the game.

- Use the **'w' 'a' 's' 'd'** keys to move the player character (**'a'** to move left, **'d'** to move right, **'w'** to move up, **'s'** to move down).

- Use **SPACEBAR** to sprint (Held down **SPACEBAR**  to make the player sprint continuously).

- Use **MOUSE1** to shoot (**MOUSE1** can be held down to make the player shoot continuously).

- After completing or loosing the level follow the prompts on screen (**'r'** to restart, **'q'** to quit).


  

## 2. Body/Analysis

### Code Structure

My application is split into 7 separate python scripts: 

- **game.py**: script manages the core game logic, including initialization,collision detection, and game state transitions (win, lose, restart). It also handles rendering, saving game history to a CSV file, and running the main game loop.

- **main_menu.py**: script manages the main menu functionality, including rendering the menu screen, handling text input for the player's nickname, and detecting button clicks for starting the game or quitting.

- **groups.py**: script defines a custom sprite group, AllSprites, to manage and render all game sprites with an offset for a dynamic camera effect. It calculates the offset based on a target position (e.g., the player) to center the screen around the target, ensuring smooth scrolling and a focused view during gameplay.

- **player.py**: script defines the Player class, which manages the player's movement, stamina, and ammo mechanics. It handles player input, collision detection, and rendering of UI elements like the stamina and ammo bars, ensuring smooth gameplay and resource management.

- **sprites.py**: script defines various sprite classes, including Sprite, CollisionSprite, Arrow, Bullet, Enemy, and Boss, to manage game entities and their behaviors. It handles sprite rendering, movement, collisions, and interactions, such as enemy tracking, bullet collisions, and boss health management.

- **test.py**: script contains unit tests for the game's core functionality, ensuring the correctness of features like the Singleton pattern, saving game history, displaying messages, and resetting the game state. It uses the unittest framework with mocks and patches to simulate game behavior and validate methods like game_won, game_over, and restart_game.

### Object-Oriented Programming (OOP) Pillars

1. **Polymorphism:**  *Polymorphism* is used extensively in a project to allow objects of different types (e.g., Player, Enemy, Arrow, Bullet) to share a common interface while exhibiting unique behaviors. This makes a code more flexible, reusable, and easier to extend.

**Example**: in the **Sprite** class and its subclasses **(CollisionSprite, Arrow, etc.)** override or extend methods to provide specific behaviors. For example, the Arrow class has methods like get_direction and rotate_arrow that are specific to its functionality, while still being treated as a pygame.sprite.Sprite.
   

   ```python
   class Arrow(pygame.sprite.Sprite):
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_arrow(self):
        angle = degrees(atan2(-self.player_direction.y, self.player_direction.x))
        self.image = pygame.transform.rotate(self.arrow_surf, angle)
   	#Further logic
   ```

   **Polymorphism** is evident in the project as objects like **Player, Enemy, Arrow, and Bullet** share a common interface **(pygame.sprite.Sprite)** while implementing unique behaviors. It demonstrates how polymorphism allows flexible and reusable code by enabling different objects to be treated uniformly.

   

2. **Abstraction:** is used in the project to hide implementation details and expose only the essential functionalities, making the code easier to understand, maintain, and extend. It allows complex logic to be encapsulated within methods or classes, providing a clean and simplified interface for interacting with objects.

**Example**: Abstracting game Logic in the **Game Class**
The **Game class** encapsulates the core game logic, such as input handling, collision detection, and game state transitions, while hiding the underlying implementation details. For instance, methods like **arrow_timer, arrow_collision, and player_collision** abstract the specific logic for managing cooldowns, detecting collisions, and handling game-over conditions.


```python
   class Game:
    def arrow_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.arrow_cooldown:
                self.can_shoot = True

    def arrow_collision(self):
        for bullet in self.bullet_sprites:
            collided_enemies = pygame.sprite.spritecollide        for enemy in collided_enemies:
                enemy.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.game_over_state = True
        if self.boss and pygame.sprite.collide_mask(self.player, self.boss):
            self.game_over_state = True
   	#Further logic
   ```

   The methods demonstrate **abstraction** by hiding the details of how cooldowns, collisions, and game-over conditions are implemented, exposing only the essential functionality required to manage these aspects of the game.
    


3. **Inheritance:** is used in the project to allow classes to derive properties and methods from a parent class, promoting code reuse and reducing redundancy. It enables specialized classes to extend or override the functionality of their base class while maintaining a shared structure.

**Example**: Inheriting **from pygame.sprite.Sprite
The Player, Enemy, Arrow, and Bullet classes inherit from the pygame.sprite.Sprite class,** allowing them to be treated as sprites while implementing their own unique behaviors.
   

	```python
   class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'boy.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.collision_sprites = collision_sprites
        # Additional player-specific attributes and methods

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, target, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'enemy.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.target = target
        # Additional enemy-specific attributes and methods
```
  
Both **Player and Enemy** demonstrate **inheritance** by deriving common attributes and methods **(e.g., image, rect, update) from pygame.sprite.Sprite**, reducing code duplication and promoting reusability. Each subclass extends or overrides the base functionality to implement specific behaviors, such as player movement or enemy tracking, while maintaining a shared structure.


   
4. **Encapsulation:** is used in the project to bundle data and methods within classes, restricting direct access to certain attributes and ensuring controlled interaction through public methods. This approach improves code security, maintainability, and modularity by hiding implementation details and exposing only necessary functionality.

**Example**: Encapsulating game logic in the **Game Class**
The **Game class** encapsulates the core game logic, such as **input handling, collision detection, and game state transitions**, while restricting direct access to its internal attributes like **nickname, start_time, and game_over_state**. Interaction with these attributes is managed through methods like **input, arrow_timer, and save_game_history.**

   ```python
   class Game:
    def __init__(self, nickname):
        self.nickname = nickname
        self.start_time = time.time()
        self.game_over_state = False
        self.can_shoot = True
        self.shoot_time = 0
        self.arrow_cooldown = 800
        # Additional initialization logic

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
   	#Further player attributes and methods
   
   class Enemy(Character):
   	def __init__(self, x, y):
           super().__init__(x, y, 175, player_texture, 100)
           self.__shoot_frequency = 20
           self.__shoot_timer = self.__shoot_frequency
           self.can_shoot = True
           self.enemy_rays = enemy_rays
   	#Further enemy attributes and methods
   ```
   
   

   In my project, I **encapsulate** critical game attributes such as **nickname, start_time, game_over_state, and can_shoot** within the **Game class**. Controlled access is provided through methods like input, **arrow_timer, and save_game_history**, promoting information hiding and reducing the risk of unintended modifications to the internal state, effectively demonstrating the principle of **encapsulation**.
   
   

### Design patterns

My application implements **Singleton** design pattern. It is implemented in the **'Game** class (*game.py*).

**Singleton** ensures that only one instance of the game exists throughout the application's lifecycle. This pattern is crucial for maintaining a consistent game state and preventing the creation of multiple game instances, which could lead to resource conflicts or unexpected behavior. It is achieved by overriding the *__ new __* method to control the instantiation process. If an instance of the **Game** class already exists, the existing instance is returned; otherwise, a new instance is created.


```python
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
            self.nickname = nickname
```



### Writing to File

In my project, writing to file is primarily handled by the **game.py** script. This script manages the **game history** and stores the player's **nickname, elapsed time, and result (win/lose)** in a file named **game_history.csv**. The game uses this functionality to track player performance and save results after each game session.


```python
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
```



### Testing

In my project, testing is essential to ensure that the game operates correctly and reliably under various scenarios. The **test.py** script serves as a dedicated module for testing the core functionalities of the game, primarily focusing on the **game.py** script. This testing script verifies multiple aspects, including the **Singleton pattern, saving game history, displaying messages, game state transitions, and cooldown mechanics.** By systematically testing these components, I can confirm that each feature functions as expected and identify any potential bugs or issues.



## 3. Results and Summary

### Results

- Result: a working video game.
- The implementation of OOP principles greatly improved the organization and modularity of the codebase, leading to easier maintenance and scalability.
- Custom sprite and texture integration added visual appeal, aligning seamlessly with the gameplay mechanics and character hitboxes.

### Conclusions

My coursework successfully implemented all 4 OOP pillars and a design pattern, which led to a well-structured and modular codebase, laying a solid foundation for future enhancements and improvements. In the future, potential enhancements could include adding more levels with unique challenges and environments, introducing new game mechanics and additional characters, as well as power-ups to boos character's abilities. Also enhancements could be done to the code itself: reusing classes as well as implementing more design patterns.
The result of my coursework is a simple, functional video game, containing all the aspects expected in such a project. However, I had plans to add many more features and improvements.

