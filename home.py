import pygame
import sys
from display_cards import display_cards

WIDTH, HEIGHT = 1000, 800
BG = (0, 128, 0)
WHITE = (255, 255, 255)
FPS = 60


def welcome(screen):
    font = pygame.font.SysFont(None, 80)
    small = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return

        screen.fill(BG)
        t = font.render("ROUND CARD GAME", True, WHITE)
        screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))

        p = small.render("Press ENTER to start", True, WHITE)
        screen.blit(p, p.get_rect(center=(WIDTH//2, HEIGHT//2 + 40)))
        pygame.display.flip()


def input_players(screen):
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    num_text = ""
    done = False

    while not done:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if num_text.strip().isdigit():
                        n = int(num_text.strip())
                        if 2 <= n <= 17:
                            done = True
                elif e.key == pygame.K_BACKSPACE:
                    num_text = num_text[:-1]
                elif e.unicode.isdigit():
                    num_text += e.unicode

        screen.fill((0, 128, 0))
        txt = font.render(
            f"Number of Players (2–17): {num_text}", True, (255, 255, 255)
        )
        screen.blit(txt, (280, 360))
        pygame.display.flip()

    # -------- NAME INPUT ----------
    names = []
    for i in range(n):
        text = ""
        entered = False

        while not entered:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if text.strip():
                            names.append(text.strip())
                            entered = True
                    elif e.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif e.unicode.isprintable():
                        text += e.unicode

            screen.fill((0, 128, 0))
            t = font.render(
                f"Enter name of Player {i+1}: {text}",
                True,
                (255, 255, 255)
            )
            screen.blit(t, (240, 360))
            pygame.display.flip()

    return n, names



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Card Game")

    welcome(screen)
    num_players, names = input_players(screen)

    display_cards(num_players, names)
