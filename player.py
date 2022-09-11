from dealer import Dealer

#Player class. Inherit Dealer class.
class Player(Dealer):
    def __init__(self, balance):
        super().__init__()
        self.balance = balance


