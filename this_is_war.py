import random
import os
import csv



class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def __repr__(self):
        return '<%d of %s>' % (self.value, self.suit)
        
        
        
SUITS = ['clubs', 'diamonds', 'spades', 'hearts']
VALUES = list(range(2,15))
CARD_LIST = []
for suit in SUITS:
    for value in VALUES:
        card = Card(suit, value)
        CARD_LIST.append(card)



def playturn(deck1, deck2):
    cards_played = [deck1.pop(0), deck2.pop(0)]
    #print(cards_played)
    compare = cards_played[0].value - cards_played[1].value
    if compare != 0:
        random.shuffle(cards_played)
        winner = deck1 if compare>0 else deck2
        winner.append(cards_played[0])
        winner.append(cards_played[1])
        return 1 if compare>0 else 2
    
    else: #tie
        #print('war!')
        if len(deck1) < 4:
            for c in deck1 + cards_played:
                deck2.append(c)
            deck1.clear()
            return 2
        if len(deck2) < 4:
            for c in deck2 + cards_played:
                deck1.append(c)
            deck2.clear()
            return 1
        pot = ([deck1.pop(0) for i in range(3)] 
             + [deck2.pop(0) for i in range(3)]
             + cards_played
             )
        result = playturn(deck1,deck2)
        winner = deck1 if result == 1 else deck2
        random.shuffle(pot)
        for c in pot:
            winner.append(c)
        return result


        
        

def playgame():
    random.shuffle(CARD_LIST)
    deck1 = CARD_LIST[:26]
    deck2 = CARD_LIST[26:]
    turn_counter = 0
    while len(deck1) > 0 and len(deck2) > 0:
        #print(len(deck1), len(deck2))
        #result = playturn(deck1, deck2)
        #print(result, 'wins this battle')
        playturn(deck1, deck2)
        turn_counter += 1
    winner = 1 if len(deck2) == 0 else 2
    #print(winner, 'wins in', turn_counter, 'moves')
    #print('  ', len(deck1), len(deck2))
    return winner, turn_counter
    
    


        
if __name__ == '__main__':
    p1_wins = p2_wins = 0
    turn_count_map = {}
    if os.path.exists('war.csv'):
        with open('war.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for t in map(tuple, reader):
                turn_count_map[int(t[0])] = int(t[1])
    else:
        turn_count_map = {0:0}
        
    for i in range(100000):
        winner, turns = playgame()
        
        if winner == 1:
            p1_wins += 1
        elif winner == 2: 
            p2_wins += 1
            
        if turns in turn_count_map.keys():
            turn_count_map[turns] += 1
        else:
            turn_count_map[turns] = 1
        
    for pair in sorted(turn_count_map.items()):
        #print(pair)
        with open('war.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(turn_count_map.items())
    
    print(p1_wins, 'wins to', p2_wins)

