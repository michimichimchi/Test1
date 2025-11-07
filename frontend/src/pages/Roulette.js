import React, { useState } from 'react';
import { gamesAPI } from '../services/api';
import '../styles/Games.css';

function Roulette({ user, updateBalance }) {
  const [bet, setBet] = useState(10);
  const [betType, setBetType] = useState('red');
  const [betValue, setBetValue] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const playGame = async () => {
    if (bet > user.balance) {
      alert('Insufficient balance!');
      return;
    }

    if (betType === 'number' && (betValue === '' || betValue < 0 || betValue > 36)) {
      alert('Please enter a valid number (0-36)');
      return;
    }

    setLoading(true);
    try {
      const response = await gamesAPI.playRoulette(bet, betType, betValue || betType);
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
    setBetValue('');
  };

  return (
    <div className="game-container">
      <h1>Roulette</h1>

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
            <label>Bet Type:</label>
            <select value={betType} onChange={(e) => setBetType(e.target.value)}>
              <option value="red">Red</option>
              <option value="black">Black</option>
              <option value="even">Even</option>
              <option value="odd">Odd</option>
              <option value="low">Low (1-18)</option>
              <option value="high">High (19-36)</option>
              <option value="number">Specific Number</option>
            </select>
          </div>

          {betType === 'number' && (
            <div className="bet-input">
              <label>Number (0-36):</label>
              <input
                type="number"
                min="0"
                max="36"
                value={betValue}
                onChange={(e) => setBetValue(e.target.value)}
                placeholder="Enter number"
              />
            </div>
          )}

          <button onClick={playGame} disabled={loading} className="btn-primary">
            {loading ? 'Spinning...' : 'Spin Wheel'}
          </button>
        </div>
      ) : (
        <div className="game-result-section">
          <h2>Result</h2>
          <div className={`roulette-result ${result.color}`}>
            <div className="result-number">{result.result}</div>
            <div className="result-color">{result.color.toUpperCase()}</div>
          </div>
          <h3>
            {result.outcome === 'win' ? `You Win! +$${result.winnings.toFixed(2)}` : `You Lose! -$${Math.abs(result.winnings).toFixed(2)}`}
          </h3>
          <button onClick={resetGame} className="btn-primary">Play Again</button>
        </div>
      )}
    </div>
  );
}

export default Roulette;
