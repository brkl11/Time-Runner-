import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (104, 117, 142)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time Runner: Menu")

# Fonts
font = pygame.font.SysFont('impact', 35)
button_font = pygame.font.SysFont('impact', 30)

# UI Elements
input_box = pygame.Rect(WIDTH / 2 - 150, HEIGHT / 2 - 200, 300, 50)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

# Global Variables
nickname = ''


def draw_menu():
    screen.fill(LIGHT_BLUE)

    # Draw Start button
    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, BLACK, start_button, 3)
    start_text = button_font.render('Start Game', True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 45))

    # Draw Quit button
    pygame.draw.rect(screen, WHITE, quit_button)
    pygame.draw.rect(screen, BLACK, quit_button, 3)
    quit_text = button_font.render('Quit', True, BLACK)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 55))

    # Draw nickname input box
    pygame.draw.rect(screen, WHITE, input_box)
    nickname_text = font.render(nickname, True, BLACK)
    screen.blit(nickname_text, (input_box.x + 10, input_box.y + 10))

    # Instructions text
    instructions = font.render("Enter Nickname:", True, BLACK)
    screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT / 2 - 250))

    pygame.display.update()


def handle_text_input(event):
    global nickname
    if event.key == pygame.K_BACKSPACE:
        nickname = nickname[:-1]
    elif event.key == pygame.K_RETURN and nickname:
        return "start", nickname
    elif len(nickname) < 15:
        nickname += event.unicode
    return None


def handle_button_click(mouse_pos):
    if start_button.collidepoint(mouse_pos) and nickname:
        return "start", nickname
    elif quit_button.collidepoint(mouse_pos):
        pygame.quit()
        sys.exit()
    return None


def main_menu():
    global nickname
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle text input
            if event.type == pygame.KEYDOWN:
                result = handle_text_input(event)
                if result:
                    return result

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = handle_button_click(pygame.mouse.get_pos())
                if result:
                    return result

        draw_menu()