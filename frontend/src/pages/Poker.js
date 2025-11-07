import React, { useState } from 'react';
import { gamesAPI } from '../services/api';
import '../styles/Games.css';

function Poker({ user, updateBalance }) {
  const [bet, setBet] = useState(10);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const playGame = async () => {
    if (bet > user.balance) {
      alert('Insufficient balance!');
      return;
    }

    setLoading(true);
    try {
      const response = await gamesAPI.playPoker(bet);
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
      <h1>5-Card Draw Poker</h1>

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

          <button onClick={playGame} disabled={loading} className="btn-primary">
            {loading ? 'Dealing...' : 'Deal Cards'}
          </button>
        </div>
      ) : (
        <div className="game-board">
          <div className="hand-section">
            <h3>Dealer's Hand</h3>
            <div className="cards">
              {result.game_state.dealer_hand.map(renderCard)}
            </div>
            <p className="hand-name">{result.game_state.dealer_hand_name}</p>
          </div>

          <div className="hand-section">
            <h3>Your Hand</h3>
            <div className="cards">
              {result.game_state.player_hand.map(renderCard)}
            </div>
            <p className="hand-name">{result.game_state.player_hand_name}</p>
          </div>

          <div className="game-result">
            <h2>
              {result.result === 'win' && `You Win! +$${result.winnings.toFixed(2)}`}
              {result.result === 'lose' && `You Lose! -$${Math.abs(result.winnings).toFixed(2)}`}
              {result.result === 'push' && 'Push! (Tie)'}
            </h2>
            <button onClick={resetGame} className="btn-primary">Play Again</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Poker;
