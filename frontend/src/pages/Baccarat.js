import React, { useState } from 'react';
import { gamesAPI } from '../services/api';
import '../styles/Games.css';

function Baccarat({ user, updateBalance }) {
  const [bet, setBet] = useState(10);
  const [betOn, setBetOn] = useState('player');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const playGame = async () => {
    if (bet > user.balance) {
      alert('Insufficient balance!');
      return;
    }

    setLoading(true);
    try {
      const response = await gamesAPI.playBaccarat(bet, betOn);
      setResult(response.data);
      updateBalance(response.data.balance);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to play');
    } finally {
      setLoading(false);
    }
  };

  const resetGame = () => {
    setResult(null);
  };

  const renderCard = (card) => {
    const suitSymbols = {
      hearts: '♥',
      diamonds: '♦',
      clubs: '♣',
      spades: '♠'
    };
    const color = card.suit === 'hearts' || card.suit === 'diamonds' ? 'red' : 'black';
    return (
      <div className={`card ${color}`} key={Math.random()}>
        <div className="card-rank">{card.rank}</div>
        <div className="card-suit">{suitSymbols[card.suit]}</div>
      </div>
    );
  };

  return (
    <div className="game-container">
      <h1>Baccarat</h1>

      {!result ? (
        <div className="bet-section">
          <h2>Place Your Bet</h2>

          <div className="bet-input">
            <label>Bet Amount:</label>
            <input
              type="number"
              min="1"
              max={user.balance}
              value={bet}
              onChange={(e) => setBet(Number(e.target.value))}
            />
          </div>

          <div className="bet-type-section">
            <label>Bet On:</label>
            <div className="bet-options">
              <button
                className={`bet-option ${betOn === 'player' ? 'active' : ''}`}
                onClick={() => setBetOn('player')}
              >
                Player (1:1)
              </button>
              <button
                className={`bet-option ${betOn === 'banker' ? 'active' : ''}`}
                onClick={() => setBetOn('banker')}
              >
                Banker (0.95:1)
              </button>
              <button
                className={`bet-option ${betOn === 'tie' ? 'active' : ''}`}
                onClick={() => setBetOn('tie')}
              >
                Tie (8:1)
              </button>
            </div>
          </div>

          <button onClick={playGame} disabled={loading} className="btn-primary">
            {loading ? 'Playing...' : 'Deal Cards'}
          </button>
        </div>
      ) : (
        <div className="game-board">
          <div className="hand-section">
            <h3>Player's Hand (Value: {result.game_state.player_value})</h3>
            <div className="cards">
              {result.game_state.player_hand.map(renderCard)}
            </div>
          </div>

          <div className="hand-section">
            <h3>Banker's Hand (Value: {result.game_state.banker_value})</h3>
            <div className="cards">
              {result.game_state.banker_hand.map(renderCard)}
            </div>
          </div>

          <div className="game-result">
            <h2>
              {result.result === 'win' && `You Win! +$${result.winnings.toFixed(2)}`}
              {result.result === 'lose' && `You Lose! -$${Math.abs(result.winnings).toFixed(2)}`}
              {result.result === 'push' && 'Push! (Tie)'}
            </h2>
            <p>
              Winner: {result.game_state.player_value > result.game_state.banker_value ? 'Player' :
                result.game_state.player_value < result.game_state.banker_value ? 'Banker' : 'Tie'}
            </p>
            <button onClick={resetGame} className="btn-primary">Play Again</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Baccarat;
