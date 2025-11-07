import random

class Baccarat:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.banker_hand = []

    def create_deck(self):
        """Create a standard 52-card deck"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def card_value(self, card):
        """Get the value of a card in baccarat"""
        if card['rank'] in ['J', 'Q', 'K', '10']:
            return 0
        elif card['rank'] == 'A':
            return 1
        else:
            return int(card['rank'])

    def hand_value(self, hand):
        """Calculate the value of a hand (only last digit counts)"""
        value = sum(self.card_value(card) for card in hand)
        return value % 10

    def deal_initial_cards(self):
        """Deal initial two cards to player and banker"""
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.banker_hand = [self.deck.pop(), self.deck.pop()]

    def should_player_draw(self):
        """Determine if player should draw a third card"""
        return self.hand_value(self.player_hand) <= 5

    def should_banker_draw(self, player_third_card=None):
        """Determine if banker should draw a third card"""
        banker_value = self.hand_value(self.banker_hand)

        if banker_value <= 2:
            return True
        elif banker_value >= 7:
            return False

        # Complex banker drawing rules
        if player_third_card is None:
            return banker_value <= 5

        player_third_value = self.card_value(player_third_card)

        if banker_value == 3:
            return player_third_value != 8
        elif banker_value == 4:
            return player_third_value in [2, 3, 4, 5, 6, 7]
        elif banker_value == 5:
            return player_third_value in [4, 5, 6, 7]
        elif banker_value == 6:
            return player_third_value in [6, 7]

        return False

    def play_round(self):
        """Play a complete round of baccarat"""
        self.deal_initial_cards()

        player_third_card = None

        # Player's turn
        if self.should_player_draw():
            player_third_card = self.deck.pop()
            self.player_hand.append(player_third_card)

        # Banker's turn
        if self.should_banker_draw(player_third_card):
            self.banker_hand.append(self.deck.pop())

        player_value = self.hand_value(self.player_hand)
        banker_value = self.hand_value(self.banker_hand)

        return {
            'player_hand': self.player_hand,
            'banker_hand': self.banker_hand,
            'player_value': player_value,
            'banker_value': banker_value
        }

    def determine_winner(self, bet_on):
        """
        Determine the winner
        bet_on can be: 'player', 'banker', 'tie'
        """
        player_value = self.hand_value(self.player_hand)
        banker_value = self.hand_value(self.banker_hand)

        if player_value == banker_value:
            if bet_on == 'tie':
                return 'win', 8  # 8:1 payout for tie
            else:
                return 'push', 1  # Push if bet on player/banker

        if player_value > banker_value:
            if bet_on == 'player':
                return 'win', 1  # 1:1 payout
            else:
                return 'lose', 0
        else:
            if bet_on == 'banker':
                return 'win', 0.95  # 0.95:1 payout (5% commission)
            else:
                return 'lose', 0
