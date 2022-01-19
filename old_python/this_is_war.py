import random
import os
import csv


class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    def __repr__(self):
        return "<%d of %s>" % (self.value, self.suit)


class Player(object):
    def __init__(self, cards):
        self.draw = list(cards)
        self.discard = []

    def __repr__(self):
        return "<draw: %d, discard: %d>" % (len(self.draw), len(self.discard))

    def fight(self):
        if len(self.draw) > 0:
            return self.draw.pop()

        elif len(self.discard) > 0:
            self.draw = self.discard
            random.shuffle(self.draw)
            self.discard = []
            return self.draw.pop()

        else:
            return None

    def plunder(self, pot):
        self.discard += pot


SUITS = ['clubs', 'diamonds', 'spades', 'hearts']
VALUES = list(range(2,15))
CARD_LIST = []
for suit in SUITS:
    for value in VALUES:
        card = Card(suit, value)
        CARD_LIST.append(card)


# return game_over, turn_winner
def playturn(player1, player2):
    c1 = player1.fight()
    if c1 is None:
        return True, 2

    c2 = player2.fight()
    if c2 is None:
        return True, 1

    if c1.value > c2.value:
        player1.plunder([c1, c2])
        return False, 1

    elif c2.value > c1.value:
        player2.plunder([c1, c2])
        return False, 2

    else: #tie
        pot = [c1, c2]
        for i in range(3):
            c = player1.fight()
            if c is None:
                return True, 2
            pot.append(c)

            c = player2.fight()
            if c is None:
                return True, 1
            pot.append(c)

        game_over, result = playturn(player1, player2)

        winner = player1 if result == 1 else player2
        winner.plunder(pot)

        return game_over, result


def playgame():
    random.shuffle(CARD_LIST)
    player1 = Player(CARD_LIST[:26])
    player2 = Player(CARD_LIST[26:])

    turn_counter = 0
    game_over = False
    while not game_over:
        # print(player1, player2)

        game_over, winner = playturn(player1, player2)
        # print(winner, 'wins this battle')

        turn_counter += 1

    #print(winner, 'wins in', turn_counter, 'moves')
    #print('  ', len(deck1), len(deck2))
    return winner, turn_counter


if __name__ == '__main__':
    p1_wins = p2_wins = 0
    turn_count_map = {}
    if os.path.exists('war.csv'):
        with open('war.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for r in reader:
                turn_count_map[int(r[0])] = int(r[1])
    else:
        turn_count_map = dict()

    for i in range(10000):
        # if i % 1000 == 0:
        #     print("game", i)

        winner, turns = playgame()

        if winner == 1:
            p1_wins += 1
        else:
            p2_wins += 1

        if turns in turn_count_map:
            turn_count_map[turns] += 1
        else:
            turn_count_map[turns] = 1
    
    # with open('war.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for pair in sorted(turn_count_map.items()):
    #         # print(pair)
    #         writer.writerow(pair)

    print(p1_wins, 'wins to', p2_wins)
