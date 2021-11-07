import random
from config import *

def create_deck(deck_list = None):
    """создает колоду карт в пустом списке"""
    global SUITS,NUMBERS
    if deck_list is None:
        deck_list = []
    elif len(deck_list)>0:
        return "list is not empty"
    for s in SUITS:
        for n in NUMBERS:
            deck_list.append(tuple([n,s]))
    return "deck is formed"

def shuffle(deck_list,sh:"раз" = 10000):
    """перемешиваем колоду"""
    n = len(deck_list)
    if n<=0: return "nothing to shuffle"
    for _ in range (sh):
        card1 = random.randint(0, n-1)
        card2 = card1
        while card1 ==card2:card2 = random.randint(0,n-1)
        deck_list[card1],deck_list[card2] = deck_list[card2],deck_list[card1]
    return "shuffled " + str(sh)+" times"