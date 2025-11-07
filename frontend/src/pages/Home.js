import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

function Home({ user }) {
  const games = [
    {
      name: 'Blackjack',
      path: '/blackjack',
      description: 'Beat the dealer by getting as close to 21 as possible without going over',
      icon: '🃏'
    },
    {
      name: 'Roulette',
      path: '/roulette',
      description: 'Bet on numbers, colors, or ranges and watch the wheel spin',
      icon: '🎰'
    },
    {
      name: 'Baccarat',
      path: '/baccarat',
      description: 'Bet on Player, Banker, or Tie in this classic card game',
      icon: '🎴'
    },
    {
      name: 'Poker',
      path: '/poker',
      description: 'Get the best 5-card hand to beat the dealer',
      icon: '♠️'
    }
  ];

  return (
    <div className="home-container">
      <div className="welcome-section">
        <h1>Welcome to Mini Games Casino, {user?.username}!</h1>
        <p className="balance-display">Your Balance: ${user?.balance?.toFixed(2)}</p>
      </div>
      <div className="games-grid">
        {games.map((game) => (
          <Link to={game.path} key={game.name} className="game-card">
            <div className="game-icon">{game.icon}</div>
            <h2>{game.name}</h2>
            <p>{game.description}</p>
            <button className="btn-play">Play Now</button>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;
