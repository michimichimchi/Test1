from datetime import datetime
from models import db

class GameHistory(db.Model):
    __tablename__ = 'game_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # blackjack, roulette, baccarat, poker
    bet_amount = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(20), nullable=False)  # win, lose, push
    winnings = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.JSON)  # Store game-specific details

    def to_dict(self):
        return {
            'id': self.id,
            'game_type': self.game_type,
            'bet_amount': self.bet_amount,
            'result': self.result,
            'winnings': self.winnings,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details
        }
