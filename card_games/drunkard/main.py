import random
from collections import deque

class Cards:
    suits = {
        1: 'Пики',
        2: 'Червы',
        3: 'Бубны',
        4: 'Трефы',
             }
    values = {
        6: '6',
        7: '7',
        8: '8',
        9: '9',
        10: '10',
        11: 'валет',
        12: 'Дама',
        13: 'Король',
        14: 'Туз',
    }
    def __init__(self, name: str):
        """Создание колоды карт и распределение по игрокам"""
        self.name = name
        deck = [[c, v] for c in self.suits.keys() for v in self.values.keys()]
        sorted_deck = random.choices(deck, k=36)
        self.players_deck = deque(sorted_deck[0:18])
        self.opponents_deck = deque(sorted_deck[18:36])

    def play(self):
        r = 0
        while True:
            if len(self.players_deck) == 0:
                print('Вы проиграли!')
                break
            elif len(self.opponents_deck) == 0:
                print('Вы выиграли!')
                break
            else:
                r += 1
                print(r, f'колода {self.name}:', len(self.players_deck), 'колода опонента:', len(self.opponents_deck))
                let = []
                player, opponent = self.players_deck.pop(), self.opponents_deck.pop()
                print(f'*** {self.name}', self.suits[player[0]], self.values[player[1]], '***  VS  *** Opponent',
                      self.suits[opponent[0]], self.values[opponent[1]], '***')
                if (player[1] > opponent[1]) or (player[1] == 6 and opponent[1] == 14):
                    self.players_deck.appendleft(player)
                    self.players_deck.appendleft(opponent)
                elif (player[1] < opponent[1]) or (player[1] == 14 and opponent[1] == 6):
                    self.opponents_deck.appendleft(player)
                    self.opponents_deck.appendleft(opponent)
                else:
                    while player[1] == opponent[1]:
                        if len(self.players_deck) >= 2 and len(self.opponents_deck) >= 2:
                            print('УВАУ!! Индентичные карты! ложим по одной сверху')
                            let.extend([player, opponent, self.players_deck.pop(), self.opponents_deck.pop()])
                        elif len(self.players_deck) == 1 and len(self.opponents_deck) == 1:
                            print('УВАУ!!кто-то на грани поражения')
                            let.extend([player, opponent])
                        if len(self.players_deck) != 0 and len(self.opponents_deck) != 0:
                            player = self.players_deck.pop()
                            opponent = self.opponents_deck.pop()
                            print(f'*** {self.name}', self.suits[player[0]], self.values[player[1]], '***  VS  *** Opponent',
                                    self.suits[opponent[0]], self.values[opponent[1]], '***')
                            if player[1] > opponent[1]:
                                self.players_deck.appendleft(player)
                                self.players_deck.appendleft(opponent)
                                self.players_deck.extendleft(let)
                            elif player[1] < opponent[1]:
                                self.opponents_deck.appendleft(player)
                                self.opponents_deck.appendleft(opponent)
                                self.opponents_deck.extendleft(let)
            print()


if __name__ == '__main__':
    Cards('DD').play()
