import React, { useState } from 'react';
import { gamesAPI } from '../services/api';
import '../styles/Games.css';

function Blackjack({ user, updateBalance }) {
  const [bet, setBet] = useState(10);
  const [gameState, setGameState] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const startGame = async () => {
    if (bet > user.balance) {
      alert('Insufficient balance!');
      return;
    }

    setLoading(true);
    try {
      const response = await gamesAPI.startBlackjack(bet);
      setGameState(response.data.game_state);
      setSessionId(response.data.session_id);
      setGameOver(false);
      setResult(null);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to start game');
    } finally {
      setLoading(false);
    }
  };

  const hit = async () => {
    setLoading(true);
    try {
      const response = await gamesAPI.blackjackHit();
      setGameState(response.data.game_state);

      if (response.data.game_over) {
        setGameOver(true);
        setResult(response.data.result);
        updateBalance(response.data.balance);
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to hit');
    } finally {
      setLoading(false);
    }
  };

  const stand = async () => {
    setLoading(true);
    try {
      const response = await gamesAPI.blackjackStand();
      setGameState(response.data.game_state);
      setGameOver(true);
      setResult(response.data.result);
      updateBalance(response.data.balance);
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to stand');
    } finally {
      setLoading(false);
    }
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
      <h1>Blackjack</h1>

      {!gameState ? (
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
          <button onClick={startGame} disabled={loading} className="btn-primary">
            {loading ? 'Starting...' : 'Start Game'}
          </button>
        </div>
      ) : (
        <div className="game-board">
          <div className="hand-section">
            <h3>Dealer's Hand (Value: {gameOver ? gameState.dealer_value : '?'})</h3>
            <div className="cards">
              {gameState.dealer_hand.map((card, idx) => (
                !gameOver && idx === 1 ? (
                  <div className="card card-back" key={idx}>?</div>
                ) : renderCard(card)
              ))}
            </div>
          </div>

          <div className="hand-section">
            <h3>Your Hand (Value: {gameState.player_value})</h3>
            <div className="cards">
              {gameState.player_hand.map(renderCard)}
            </div>
          </div>

          {!gameOver ? (
            <div className="game-actions">
              <button onClick={hit} disabled={loading} className="btn-action">Hit</button>
              <button onClick={stand} disabled={loading} className="btn-action">Stand</button>
            </div>
          ) : (
            <div className="game-result">
              <h2>
                {result === 'win' && 'You Win!'}
                {result === 'lose' && 'You Lose!'}
                {result === 'push' && 'Push!'}
              </h2>
              <button onClick={() => setGameState(null)} className="btn-primary">
                Play Again
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Blackjack;
