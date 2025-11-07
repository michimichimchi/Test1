from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.user import User
from models.game_history import GameHistory
from game_logic.blackjack import Blackjack
from game_logic.roulette import Roulette
from game_logic.baccarat import Baccarat
from game_logic.poker import Poker

games_bp = Blueprint('games', __name__)

# Store active game sessions (in production, use Redis or similar)
active_games = {}

@games_bp.route('/blackjack/start', methods=['POST'])
@jwt_required()
def start_blackjack():
    user_id = get_jwt_identity()
    data = request.get_json()
    bet = data.get('bet', 10)

    user = User.query.get(user_id)
    if user.balance < bet:
        return jsonify({'error': 'Insufficient balance'}), 400

    # Create new game
    game = Blackjack()
    game.deal_initial_cards()

    # Store game session
    session_id = f"{user_id}_blackjack"
    active_games[session_id] = {'game': game, 'bet': bet}

    return jsonify({
        'session_id': session_id,
        'game_state': game.get_game_state(),
        'bet': bet
    }), 200

@games_bp.route('/blackjack/hit', methods=['POST'])
@jwt_required()
def blackjack_hit():
    user_id = get_jwt_identity()
    session_id = f"{user_id}_blackjack"

    if session_id not in active_games:
        return jsonify({'error': 'No active game'}), 400

    game = active_games[session_id]['game']
    game.hit(game.player_hand)

    game_state = game.get_game_state()

    # Check if player busted
    if game_state['player_value'] > 21:
        bet = active_games[session_id]['bet']
        result, _ = game.determine_winner()

        # Update balance
        user = User.query.get(user_id)
        user.balance -= bet

        # Record game
        history = GameHistory(
            user_id=user_id,
            game_type='blackjack',
            bet_amount=bet,
            result=result,
            winnings=-bet,
            details=game_state
        )
        db.session.add(history)
        db.session.commit()

        del active_games[session_id]

        return jsonify({
            'game_state': game_state,
            'game_over': True,
            'result': result,
            'balance': user.balance
        }), 200

    return jsonify({
        'game_state': game_state,
        'game_over': False
    }), 200

@games_bp.route('/blackjack/stand', methods=['POST'])
@jwt_required()
def blackjack_stand():
    user_id = get_jwt_identity()
    session_id = f"{user_id}_blackjack"

    if session_id not in active_games:
        return jsonify({'error': 'No active game'}), 400

    game = active_games[session_id]['game']
    bet = active_games[session_id]['bet']

    # Dealer plays
    game.dealer_play()

    # Determine winner
    result, multiplier = game.determine_winner()

    # Update balance
    user = User.query.get(user_id)
    winnings = (bet * multiplier) - bet

    user.balance += winnings

    # Record game
    history = GameHistory(
        user_id=user_id,
        game_type='blackjack',
        bet_amount=bet,
        result=result,
        winnings=winnings,
        details=game.get_game_state()
    )
    db.session.add(history)
    db.session.commit()

    del active_games[session_id]

    return jsonify({
        'game_state': game.get_game_state(),
        'result': result,
        'winnings': winnings,
        'balance': user.balance
    }), 200

@games_bp.route('/roulette/play', methods=['POST'])
@jwt_required()
def play_roulette():
    user_id = get_jwt_identity()
    data = request.get_json()

    bet = data.get('bet', 10)
    bet_type = data.get('bet_type')
    bet_value = data.get('bet_value')

    user = User.query.get(user_id)
    if user.balance < bet:
        return jsonify({'error': 'Insufficient balance'}), 400

    game = Roulette()
    result = game.spin()

    # Check if bet wins
    multiplier = game.check_bet(bet_type, bet_value, result)

    if multiplier > 0:
        winnings = bet * multiplier
        outcome = 'win'
    else:
        winnings = -bet
        outcome = 'lose'

    user.balance += winnings

    # Record game
    history = GameHistory(
        user_id=user_id,
        game_type='roulette',
        bet_amount=bet,
        result=outcome,
        winnings=winnings,
        details={
            'result_number': result,
            'result_color': game.get_color(result),
            'bet_type': bet_type,
            'bet_value': bet_value
        }
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({
        'result': result,
        'color': game.get_color(result),
        'outcome': outcome,
        'winnings': winnings,
        'balance': user.balance
    }), 200

@games_bp.route('/baccarat/play', methods=['POST'])
@jwt_required()
def play_baccarat():
    user_id = get_jwt_identity()
    data = request.get_json()

    bet = data.get('bet', 10)
    bet_on = data.get('bet_on')  # 'player', 'banker', or 'tie'

    user = User.query.get(user_id)
    if user.balance < bet:
        return jsonify({'error': 'Insufficient balance'}), 400

    game = Baccarat()
    game_state = game.play_round()

    result, multiplier = game.determine_winner(bet_on)

    if result == 'win':
        winnings = bet * multiplier
    elif result == 'push':
        winnings = 0
    else:
        winnings = -bet

    user.balance += winnings

    # Record game
    history = GameHistory(
        user_id=user_id,
        game_type='baccarat',
        bet_amount=bet,
        result=result,
        winnings=winnings,
        details={
            **game_state,
            'bet_on': bet_on
        }
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({
        'game_state': game_state,
        'result': result,
        'winnings': winnings,
        'balance': user.balance
    }), 200

@games_bp.route('/poker/play', methods=['POST'])
@jwt_required()
def play_poker():
    user_id = get_jwt_identity()
    data = request.get_json()

    bet = data.get('bet', 10)

    user = User.query.get(user_id)
    if user.balance < bet:
        return jsonify({'error': 'Insufficient balance'}), 400

    game = Poker()
    game_state = game.play_round()

    result, multiplier = game.compare_hands(game.player_hand, game.dealer_hand)

    if result == 'win':
        winnings = bet * (multiplier - 1)
    elif result == 'push':
        winnings = 0
    else:
        winnings = -bet

    user.balance += winnings

    # Record game
    history = GameHistory(
        user_id=user_id,
        game_type='poker',
        bet_amount=bet,
        result=result,
        winnings=winnings,
        details=game_state
    )
    db.session.add(history)
    db.session.commit()

    return jsonify({
        'game_state': game_state,
        'result': result,
        'winnings': winnings,
        'balance': user.balance
    }), 200
