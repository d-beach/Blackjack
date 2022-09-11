import random
from card import Card

# Deck class
class Deck:

    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()

    #Create cards in deck using values and suits from card file
    def create_deck(self):
        for suit in range(4):
            for value in range(1, 14):
                card = Card(suit, value)
                self.cards.append(card)

    # Shuffle deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal cards from deck
    def deal(self, num):
        cards_dealt = []

        for i in range(num):

            card = self.cards.pop()
            cards_dealt.append(card)

        return cards_dealt
        

