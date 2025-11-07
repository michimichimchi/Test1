from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.game_history import GameHistory

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200

@user_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()

    history = GameHistory.query.filter_by(user_id=user_id).order_by(GameHistory.timestamp.desc()).limit(50).all()

    return jsonify([h.to_dict() for h in history]), 200

@user_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    users = User.query.order_by(User.balance.desc()).limit(10).all()

    leaderboard = [{
        'rank': idx + 1,
        'username': user.username,
        'balance': user.balance
    } for idx, user in enumerate(users)]

    return jsonify(leaderboard), 200
