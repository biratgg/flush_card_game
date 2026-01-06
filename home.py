import pygame
import sys

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 800
BG_COLOR = (0, 128, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (200, 50, 50)

FPS = 60
# --------------------------------------


def welcome_screen(screen):
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 90)
    text_font = pygame.font.SysFont(None, 36)

    blink = True
    blink_timer = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(BG_COLOR)

        title = title_font.render("ROUND CARD GAME", True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

        blink_timer += 1
        if blink_timer > FPS // 2:
            blink = not blink
            blink_timer = 0

        if blink:
            start = text_font.render("Press ENTER to Start", True, WHITE)
            screen.blit(start, start.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()


def input_number_players(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    user_text = ""
    error_msg = ""

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.isdigit():
                        num = int(user_text)
                        if 2 <= num <= 17:
                            return num
                        else:
                            error_msg = "Players must be between 2 and 17"
                    else:
                        error_msg = "Enter a valid number"

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                else:
                    if event.unicode.isdigit():
                        user_text += event.unicode

        screen.fill(BG_COLOR)

        prompt = font.render("Enter number of players:", True, WHITE)
        screen.blit(prompt, (350, 300))

        text_surface = font.render(user_text, True, YELLOW)
        screen.blit(text_surface, (350, 350))

        if error_msg:
            error = font.render(error_msg, True, RED)
            screen.blit(error, (350, 400))

        pygame.display.flip()


def input_player_name(screen, index):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    user_text = ""
    error_msg = ""

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip():
                        return user_text.strip()
                    else:
                        error_msg = "Name cannot be empty"

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                else:
                    if event.unicode.isprintable():
                        user_text += event.unicode

        screen.fill(BG_COLOR)

        prompt = font.render(f"Enter name of Player {index}:", True, WHITE)
        screen.blit(prompt, (320, 300))

        text_surface = font.render(user_text, True, YELLOW)
        screen.blit(text_surface, (320, 350))

        if error_msg:
            error = font.render(error_msg, True, RED)
            screen.blit(error, (320, 400))

        pygame.display.flip()


def run_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Card Game")

    welcome_screen(screen)

    num_players = input_number_players(screen)

    names = []
    for i in range(1, num_players + 1):
        name = input_player_name(screen, i)
        names.append(name)

    return num_players, names


if __name__ == "__main__":
    num_players, player_names = run_menu()
    print("Players:", num_players)
    print("Names:", player_names)

    import display_cards
    display_cards.display_cards(num_players, player_names)
