import random

class Blackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        """Create a standard 52-card deck"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def card_value(self, card):
        """Get the value of a card"""
        if card['rank'] in ['J', 'Q', 'K']:
            return 10
        elif card['rank'] == 'A':
            return 11  # Will be adjusted if needed
        else:
            return int(card['rank'])

    def hand_value(self, hand):
        """Calculate the value of a hand"""
        value = sum(self.card_value(card) for card in hand)
        aces = sum(1 for card in hand if card['rank'] == 'A')

        # Adjust for aces
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def deal_initial_cards(self):
        """Deal initial two cards to player and dealer"""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def hit(self, hand):
        """Add a card to the hand"""
        hand.append(self.deck.pop())

    def dealer_play(self):
        """Dealer plays according to standard rules (hit on 16, stand on 17)"""
        while self.hand_value(self.dealer_hand) < 17:
            self.hit(self.dealer_hand)

    def determine_winner(self):
        """Determine the winner of the game"""
        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)

        if player_value > 21:
            return 'lose', 0
        elif dealer_value > 21:
            return 'win', 2
        elif player_value > dealer_value:
            return 'win', 2
        elif player_value < dealer_value:
            return 'lose', 0
        else:
            return 'push', 1

    def get_game_state(self):
        """Get the current state of the game"""
        return {
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'player_value': self.hand_value(self.player_hand),
            'dealer_value': self.hand_value(self.dealer_hand)
        }
