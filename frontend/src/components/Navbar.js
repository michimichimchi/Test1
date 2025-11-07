import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">Mini Games Casino</Link>
      </div>
      <div className="navbar-menu">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/leaderboard" className="nav-link">Leaderboard</Link>
        <Link to="/history" className="nav-link">History</Link>
      </div>
      <div className="navbar-user">
        <span className="balance">Balance: ${user?.balance?.toFixed(2) || '0.00'}</span>
        <span className="username">{user?.username}</span>
        <button onClick={onLogout} className="btn-logout">Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;
