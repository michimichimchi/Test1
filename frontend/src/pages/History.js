import React, { useState, useEffect } from 'react';
import { userAPI } from '../services/api';
import '../styles/History.css';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await userAPI.getHistory();
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getResultClass = (result) => {
    if (result === 'win') return 'result-win';
    if (result === 'lose') return 'result-lose';
    return 'result-push';
  };

  return (
    <div className="history-container">
      <h1>Game History</h1>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : history.length === 0 ? (
        <div className="no-history">
          <p>No game history yet. Start playing to see your results here!</p>
        </div>
      ) : (
        <div className="history-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Game</th>
                <th>Bet</th>
                <th>Result</th>
                <th>Winnings</th>
              </tr>
            </thead>
            <tbody>
              {history.map((game) => (
                <tr key={game.id}>
                  <td>{formatDate(game.timestamp)}</td>
                  <td className="game-type">{game.game_type}</td>
                  <td>${game.bet_amount.toFixed(2)}</td>
                  <td className={getResultClass(game.result)}>
                    {game.result.toUpperCase()}
                  </td>
                  <td className={game.winnings >= 0 ? 'positive' : 'negative'}>
                    {game.winnings >= 0 ? '+' : ''}${game.winnings.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;
