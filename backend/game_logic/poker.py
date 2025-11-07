import random
from collections import Counter

class Poker:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        """Create a standard 52-card deck"""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit, 'value': idx} for idx, rank in enumerate(ranks, 2) for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_hand(self):
        """Deal 5 cards"""
        return [self.deck.pop() for _ in range(5)]

    def rank_value(self, card):
        """Get numeric value for comparison"""
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return rank_order[card['rank']]

    def evaluate_hand(self, hand):
        """
        Evaluate poker hand strength
        Returns: (rank, high_card) where rank is 1-10 (10 being royal flush)
        """
        ranks = [self.rank_value(card) for card in hand]
        suits = [card['suit'] for card in hand]
        rank_counts = Counter(ranks)

        is_flush = len(set(suits)) == 1
        sorted_ranks = sorted(ranks)
        is_straight = sorted_ranks == list(range(min(ranks), max(ranks) + 1))

        # Check for ace-low straight (A-2-3-4-5)
        if sorted_ranks == [2, 3, 4, 5, 14]:
            is_straight = True
            sorted_ranks = [1, 2, 3, 4, 5]

        counts = sorted(rank_counts.values(), reverse=True)
        unique_ranks = sorted(rank_counts.keys(), key=lambda x: (rank_counts[x], x), reverse=True)

        # Royal Flush
        if is_flush and is_straight and max(ranks) == 14 and min(ranks) == 10:
            return (10, max(ranks))

        # Straight Flush
        if is_flush and is_straight:
            return (9, max(sorted_ranks))

        # Four of a Kind
        if counts == [4, 1]:
            return (8, unique_ranks[0])

        # Full House
        if counts == [3, 2]:
            return (7, unique_ranks[0])

        # Flush
        if is_flush:
            return (6, max(ranks))

        # Straight
        if is_straight:
            return (5, max(sorted_ranks))

        # Three of a Kind
        if counts == [3, 1, 1]:
            return (4, unique_ranks[0])

        # Two Pair
        if counts == [2, 2, 1]:
            return (3, max(unique_ranks[:2]))

        # One Pair
        if counts == [2, 1, 1, 1]:
            return (2, unique_ranks[0])

        # High Card
        return (1, max(ranks))

    def get_hand_name(self, rank):
        """Get the name of the hand rank"""
        names = {
            10: "Royal Flush",
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card"
        }
        return names.get(rank, "Unknown")

    def compare_hands(self, player_hand, dealer_hand):
        """Compare two hands and determine winner"""
        player_score = self.evaluate_hand(player_hand)
        dealer_score = self.evaluate_hand(dealer_hand)

        if player_score[0] > dealer_score[0]:
            return 'win', 2
        elif player_score[0] < dealer_score[0]:
            return 'lose', 0
        else:
            # Same hand rank, compare high card
            if player_score[1] > dealer_score[1]:
                return 'win', 2
            elif player_score[1] < dealer_score[1]:
                return 'lose', 0
            else:
                return 'push', 1

    def play_round(self):
        """Play a round of 5-card draw poker"""
        self.player_hand = self.deal_hand()
        self.dealer_hand = self.deal_hand()

        player_score = self.evaluate_hand(self.player_hand)
        dealer_score = self.evaluate_hand(self.dealer_hand)

        return {
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'player_hand_name': self.get_hand_name(player_score[0]),
            'dealer_hand_name': self.get_hand_name(dealer_score[0])
        }
