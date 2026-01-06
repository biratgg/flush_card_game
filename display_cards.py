import pygame
import os
import math
import sys
import random
from shuffle import shuffle_and_deal  # your fixed shuffle.py

# ================== CONFIG ==================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (0, 128, 0)  # table green

CARDS_PER_PLAYER = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
BUTTON_GAP = 20


def clamp(min_v, v, max_v):
    return max(min_v, min(v, max_v))


def draw_button(screen, font, text, rect, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=5)
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def get_label_and_button_rect(px, py, card_w, card_h, angle):
    offset = 20  # distance from cards

    norm_angle = angle % (2 * math.pi)

    label_x, label_y = px, py
    flip_x, flip_y = px, py

    if (norm_angle >= 0 and norm_angle < math.pi / 8) or (norm_angle >= 15 * math.pi / 8 and norm_angle < 2 * math.pi):
        # Center Top
        label_x = px
        label_y = py - card_h / 2 - offset
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= math.pi / 8 and norm_angle < 3 * math.pi / 8:
        # Top-Right
        label_x = px + card_w / 2 + offset
        label_y = py - card_h / 2 - offset / 2
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 3 * math.pi / 8 and norm_angle < 5 * math.pi / 8:
        # Right-Top
        label_x = px + card_w / 2 + offset
        label_y = py - offset
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 5 * math.pi / 8 and norm_angle < 7 * math.pi / 8:
        # Right-Bottom
        label_x = px + card_w / 2 + offset
        label_y = py + card_h / 2 + offset / 2
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 7 * math.pi / 8 and norm_angle < 9 * math.pi / 8:
        # Center Bottom
        label_x = px
        label_y = py + card_h / 2 + offset
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 9 * math.pi / 8 and norm_angle < 11 * math.pi / 8:
        # Bottom-Left
        label_x = px - card_w / 2 - offset
        label_y = py + card_h / 2 + offset / 2
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 11 * math.pi / 8 and norm_angle < 13 * math.pi / 8:
        # Left-Bottom
        label_x = px - card_w / 2 - offset
        label_y = py + offset
        flip_x = label_x
        flip_y = label_y + 30

    elif norm_angle >= 13 * math.pi / 8 and norm_angle < 15 * math.pi / 8:
        # Left-Top
        label_x = px - card_w / 2 - offset
        label_y = py - card_h / 2 - offset / 2
        flip_x = label_x
        flip_y = label_y + 30

    else:
        # Fallback center top
        label_x = px
        label_y = py - card_h / 2 - offset
        flip_x = label_x
        flip_y = label_y + 30

    name_pos = (label_x, label_y)
    flip_btn_rect = pygame.Rect(0, 0, 80, 30)
    flip_btn_rect.center = (flip_x, flip_y)

    return name_pos, flip_btn_rect


def display_cards(num_players, names):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Round Card Table")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 26)

    BASE_DIR = os.path.dirname(__file__)
    CARDS_DIR = os.path.join(BASE_DIR, "images")

    back_img_path = os.path.join(CARDS_DIR, "back.png")
    if not os.path.isfile(back_img_path):
        print(f"Error: '{back_img_path}' not found!")
        pygame.quit()
        sys.exit(1)

    # Initial deal
    players = shuffle_and_deal(num_players)

    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * (0.25 + 0.015 * num_players)
    radius = min(radius, min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.42)

    card_width = SCREEN_WIDTH / (num_players * 1.8)
    card_width = clamp(40, card_width, 90)
    card_height = int(card_width * 1.4)
    gap = int(card_width * 0.15)

    angle_step = 2 * math.pi / num_players

    def load_player_cards():
        cards_img_list = []
        for hand in players:
            imgs = []
            for card in hand:
                card_path = os.path.join(CARDS_DIR, f"{card}.png")
                if not os.path.isfile(card_path):
                    print(f"Warning: Card image '{card_path}' not found. Skipping.")
                    continue
                img = pygame.image.load(card_path).convert_alpha()
                img = pygame.transform.smoothscale(img, (int(card_width), card_height))
                imgs.append(img)
            cards_img_list.append(imgs)
        return cards_img_list

    player_cards = load_player_cards()

    back_img = pygame.image.load(back_img_path).convert_alpha()
    back_img = pygame.transform.smoothscale(back_img, (int(card_width), card_height))

    flipped = [False] * num_players

    # Buttons: Shuffle and Display All
    shuffle_btn_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    display_all_btn_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)

    # Position buttons centered bottom with gap
    total_width = BUTTON_WIDTH * 2 + BUTTON_GAP
    start_x = (SCREEN_WIDTH - total_width) // 2
    shuffle_btn_rect.topleft = (start_x, SCREEN_HEIGHT - BUTTON_HEIGHT - 20)
    display_all_btn_rect.topleft = (start_x + BUTTON_WIDTH + BUTTON_GAP, SCREEN_HEIGHT - BUTTON_HEIGHT - 20)

    display_all_state = False  # False = cards facedown, True = all flipped faceup

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

        screen.fill(BACKGROUND_COLOR)

        # Draw all players' cards + names + flip buttons
        for i, hand in enumerate(player_cards):
            angle = i * angle_step - math.pi / 2

            px = cx + radius * math.cos(angle)
            py = cy + radius * math.sin(angle)

            hand_width = CARDS_PER_PLAYER * card_width + (CARDS_PER_PLAYER - 1) * gap
            start_x_hand = px - hand_width / 2
            y = py - card_height / 2

            # Draw cards
            for j, card in enumerate(hand):
                x = start_x_hand + j * (card_width + gap)
                if flipped[i]:
                    screen.blit(card, (x, y))
                else:
                    screen.blit(back_img, (x, y))

            # Draw name and flip button (positioned properly)
            name_pos, flip_btn_rect = get_label_and_button_rect(px, py, card_width, card_height, angle)

            name_surf = font.render(names[i], True, WHITE)
            name_rect = name_surf.get_rect(center=name_pos)
            screen.blit(name_surf, name_rect)

            hover = flip_btn_rect.collidepoint(mouse_pos)
            draw_button(screen, font, "Flip", flip_btn_rect, hover)

            if mouse_clicked and hover:
                flipped[i] = not flipped[i]

        # Draw Shuffle and Display All buttons
        hover_shuffle = shuffle_btn_rect.collidepoint(mouse_pos)
        hover_display_all = display_all_btn_rect.collidepoint(mouse_pos)

        draw_button(screen, font, "Shuffle", shuffle_btn_rect, hover_shuffle)
        draw_button(screen, font, "Display All", display_all_btn_rect, hover_display_all)

        if mouse_clicked:
            if hover_shuffle:
                # Reshuffle cards and reset flipped to False
                players = shuffle_and_deal(num_players)
                player_cards = load_player_cards()
                flipped = [False] * num_players
                display_all_state = False

            elif hover_display_all:
                # Toggle all flipped state
                display_all_state = not display_all_state
                flipped = [display_all_state] * num_players

        pygame.display.flip()

    pygame.quit()
