from deck import Deck
from hand import Hand

class Game:
    MINIMUM_BET = 1

    def __init__(self, player, dealer):
        self.player = player
        self.dealer = dealer
        self.bet = None
        self.deck = Deck()

    # Logic for placing bet
    def place_bet(self):
        while True:
            bet = float(input("How much would you like to bet? "))
            # If bet is more than player balance tell them to bet again
            if bet > self.player.balance:
                print("You don't have enough funds. Try again")
            # If bet is less than 1
            elif bet < self.MINIMUM_BET:
                print(f"The minimum bet is {self.MINIMUM_BET}. Try again")
            # Subtract bet from balance
            else:
                self.player.balance -= bet
                self.bet = bet
                break

    # Logic for winning round
    def round_winner(self):
        player_hand = self.player.get_str_hand()
        dealer_hand = self.dealer.get_str_hand()
        # Player wins
        if player_hand > dealer_hand:
            self.player.balance += self.bet*2
            print(f"You won ${self.bet}!")
        # Player loses
        elif player_hand < dealer_hand:
            print(f"Sorry the dealer won the hand, you lose ${self.bet}.")
        # Tie 
        else:
            self.player.balance += self.bet
            print(f"You tied with the dealer. Your bet of ${self.bet} has been returned.")

    #Confirm starting game
    def start_confirm(self):
        decision_to_play = input(
            f"You are starting with ${self.player.balance}, would you like to play? " ).lower()
        return decision_to_play == "yes"

    # Logic to start round once game has begun
    def start_round(self):
        self.place_bet()
        self.deal_hand()
        
        # Check for blakcjack case
        if self.blackjack():
            return
        # Handle player bust
        player_lost = self.player_turn()
        if player_lost:
            print(f"Your hand is over 21, you lose ${self.bet}.")
            return
        # Handle dealer bust
        dealer_lost = self.dealer_turn()
        if dealer_lost:
            self.player.balance += self.bet * 2
            print(f"The dealer busts, you win. You are awarded ${self.bet}.")
            return
        # Inform result 
        self.round_winner()
        self.reset_round()

    # Logic for how to handle when a player has blackjack
    def blackjack(self):
        if self.player.hand.get_value() != 21:
            return False

        if self.player.hand.get_value == 21:
            self.player.balance += self.bet
            print(
                "Both you and the dealer have blackjack. This round is a tie. You're bet has been returned."
            )
            return True

        self.player.balance += self.bet * 2.5
        print(f"You have blackjack. You win {self.bet * 1.5}")
        return True

    # Function to start game
    def start_game(self):
        # Check if player has money to bet
        while self.player.balance > 0:
            #If player does not confirm start leave the game
            if not self.start_confirm():
                print(f"You left the game with ${self.player.balance}.")
                break

            self.start_round()
            print()
        # If player doesn't have enough money leave game
        else:
            print("You are now out of money. Please restart to play again.")

    # Deal hand to player and dealer
    def deal_hand(self):
            self.player.hand = Hand(self.deck.deal(2))
            self.dealer.hand = Hand(self.deck.deal(2))
            self.dealer.hand.cards[1].hidden = True

            print("You were dealt: ", self.player.get_str_hand())
            print("The dealer was dealt: ", self.dealer.get_str_hand())

    # Logic for player deciding to hit
    def decide_to_hit(self):
        while True:
            # Ask if player wants to hit or stay
            hit_decision = input("Would you like to hit or stay? ")
            decision = ["hit", "stay"]
            # Make sure player inputs hit or stay
            if hit_decision in decision:
                break
            else:
                print("Invalid option")
        # return true if player decides to hit
        return hit_decision == "hit"
                
    # Logic for player turn       
    def player_turn(self):
        while True:
            # Decision for player to hit or stay
            hit = self.decide_to_hit()
            
            if not hit:
                break
            # If player decides to hit
            new_card = self.deck.deal(1)[0]
            self.player.hit(new_card)
            print("You were dealt: ", new_card)
            print("Your hand is now: ", self.player.get_str_hand())
            # Player busts (value above 21)
            if self.player.hand.get_value() > 21:
                return True
            
            return False

    # Logic for dealer turn
    def dealer_turn(self):
        # Other card in dealer hand no longer hidden
        self.dealer.hand.cards[1].hidden = False
        print("The dealer has: ", self.dealer.get_str_hand())
        # Dealer hits if hand below 16
        while self.dealer.hand.get_value() <= 16:
            new_card = self.deck.deal(1)[0]
            self.dealer.hit(new_card)
            print("The dealer now has: ", new_card)
            print("Their hand is now: ", self.dealer.get_str_hand())
        # Dealer busts (hand above 21)
        if self.dealer.hand.get_value() > 21:
            return True
        
        return False

    def reset_round(self):
        self.deck = Deck()
        self.player.hand = None
        self.dealer.hand = None
        self.bet = None
