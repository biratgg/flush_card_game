# shuffle.py
import random

def shuffle_and_deal(n):
    cards_num = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
    card_type = ['H', 'D', 'C', 'S']

    deck = [num + suit for num in cards_num for suit in card_type]
    random.shuffle(deck)

    players = [[] for _ in range(n)]

    for i in range(n * 3):
        players[i % n].append(deck[i])

    return players
