import numpy as np
from tqdm import tqdm
import itertools

from phevaluator import evaluate_cards, evaluate_omaha_cards
import random

suits = ['d','s','c','h']
ranks = ['A','2','3','4','5','6','7','8','9','T','J','Q','K']
cards = []
for r in ranks:
    for s in suits:
        cards.append(r+s)

def flop(hand, table, players, hand_size):
    hand = hand[:]
    table = table[:]

    full = table + hand
    deck = list(set(cards[:]) - set(full))
    np.random.shuffle(deck)
        
    hands = [[deck.pop() for _ in range(hand_size)] for _ in range(players)]
    
    #flop, turn, river
    while len(table) < 5:
        card = deck.pop()
        table.append(card)
        full.append(card)
    # my_hand_rank = evaluate_cards(full[0],full[1],full[2],full[3],full[4],full[5],full[6])
    if hand_size > 2:
        my_hand_rank = evaluate_omaha_cards(*full)
    else:
        my_hand_rank = evaluate_cards(*full)
    
    # print(table, hand, players, hands)

    for check_hand in hands:
        all_cards = table + check_hand
        
        if hand_size > 2:
            opponent = evaluate_omaha_cards(*all_cards)
        else:
            opponent = evaluate_cards(*all_cards)
        
        # from the definition of the library we use for hand evaluation, larger evaluations correspond to less strong hands
        #so, the game is won by the player with the smallest hand evaluation
        if opponent < my_hand_rank:
            return 1 #'LOSE'
        if opponent == my_hand_rank:
            return 2 #'SPLIT'
        return 0 #'WIN'
    
def preflop(hand, **kwargs):
    # deck = random.sample(cards,len(cards)) #shuffle the deck
    # deck = list(filter(lambda x: x not in hand, deck))    
    table = []
    return flop(hand, table, **kwargs)
    
def monte_carlo(f, samples=100, **kwargs):
    dist = [0,0,0]

    for i in range(samples):
        outcome = f(**kwargs)
        dist[outcome] += 1
    return list(map(lambda x: x/samples, dist))    

def reg():
    j = dict()
    
    for p in tqdm(list(itertools.combinations(cards, 2))):
        j[p] = monte_carlo(preflop, hand=list(p), players=4, hand_size=2)

    return j

def omaha():
    j = dict()
    
    for p in tqdm(list(itertools.combinations(cards, 4))):
        j[p] = monte_carlo(preflop, hand=list(p), players=4, hand_size=4)

    return j

r = reg()
print(r)
# o = omaha()