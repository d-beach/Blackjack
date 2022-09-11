# Hand class
class Hand:
    def __init__(self, cards):
        self.cards = cards
        
    # Returns value of player and dealer hand
    def get_value(self):
        value = 0
        ace_count = 0
        
        for card in self.cards:
            card_val = card.value

            # Hand case with one ace
            if card_val == 1: 
                ace_count += 1
            else:
                value += min(card_val,10)
        # All other cases with 0 or multiple aces
        if ace_count == 0:
            return value

        elif value + 11 > 21:
            return value + ace_count

        elif ace_count == 1:
            return value + 11

        elif value + 11 + (ace_count - 1) <= 21:
            return value + 11 + (ace_count - 1)

        else:
            return value + ace_count

    # Add cards to hand after they are dealt from deck
    def add_to_hand(self, card):
        self.cards.append(card)

    # return string of cards that are in player and or dealer hand
    def __str__(self):
        card_string = [str(card) for card in self.cards]
        return ", ".join(card_string)
 