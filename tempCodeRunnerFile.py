    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Round Card Table")

    BASE_DIR = os.path.dirname(__file__)
    CARDS_DIR = os.path.join(BASE_DIR, "images")

    # --------- HELPERS ----------
    def clamp(min_v, v, max_v):
        return max(min_v, min(v, max_v))

    # --------- DYNAMIC GEOMETRY ----------
    cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) * (0.25 + 0.015 * NUM_PLAYERS)
    radius = min(radius, min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.42)

    card_width = SCREEN_WIDTH / (NUM_PLAYERS * 1.8)
    card_width = clamp(40, card_width, 90)
    card_height = int(card_width * 1.4)

    gap = int(card_width * 0.25)

    angle_step = 2 * math.pi / NUM_PLAYERS

    # --------- LOAD & SCALE CARDS ----------
    player_cards = []

    for hand in players:
        imgs = []
        for card in hand:
            img = pygame.image.load(
                os.path.join(CARDS_DIR, f"{card}.png")
            ).convert_alpha()

            img = pygame.transform.smoothscale(
                img, (int(card_width), card_height)
            )
            imgs.append(img)

        player_cards.append(imgs)

    # ================== MAIN LOOP ==================
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for i, hand in enumerate(player_cards):
            angle = i * angle_step - math.pi / 2

            px = cx + radius * math.cos(angle)
            py = cy + radius * math.sin(angle)

            hand_width = (
                CARDS_PER_PLAYER * card_width +
                (CARDS_PER_PLAYER - 1) * gap
            )

            start_x = px - hand_width / 2
            y = py - card_height / 2

            for j, card in enumerate(hand):
                x = start_x + j * (card_width + gap)
                screen.blit(card, (x, y))

        pygame.display.flip()

    pygame.quit()
