# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack mini games casino web application with four casino games (Blackjack, Roulette, Baccarat, Poker), featuring user authentication, virtual currency system, game history tracking, and leaderboards.

## Technology Stack

- **Backend**: Python/Flask with MySQL database
- **Frontend**: React with React Router
- **Authentication**: JWT tokens with bcrypt password hashing
- **Database**: MySQL with SQLAlchemy ORM

## Architecture

### Backend Structure

The backend follows a modular Flask application pattern:

- **Models** (backend/models/): SQLAlchemy models for User and GameHistory
- **Routes** (backend/routes/): Blueprint-based routing for auth, games, and user endpoints
- **Game Logic** (backend/game_logic/): Separate Python classes for each game's business logic
- **Configuration**: Environment-based config using python-dotenv

### Frontend Structure

React single-page application with:

- **Component-based architecture**: Separate components for Login, Register, Navbar
- **Page components**: One for each game plus Home, Leaderboard, and History
- **API service layer**: Centralized axios-based API calls in services/api.js
- **Protected routes**: Authentication-based routing in App.js

### Game Logic Architecture

Each game (Blackjack, Roulette, Baccarat, Poker) has:
1. A Python class in backend/game_logic/ handling game rules and state
2. API endpoints in backend/routes/games.py for game actions
3. A React page component in frontend/src/pages/ for the UI

Blackjack uses session storage for multi-step gameplay (hit/stand), while other games are single-round with immediate results.

## Common Development Commands

### Backend

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run Flask server (default port 5000)
python app.py

# Create/reset database tables
# Tables are auto-created on first run via db.create_all() in app.py
```

### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Run development server (port 3000)
npm start

# Build for production
npm build
```

### Database Setup

Create MySQL database before first run:
```sql
CREATE DATABASE mini_games_db;
```

Configure database connection in backend/.env:
```
DATABASE_URL=mysql+pymysql://username:password@localhost/mini_games_db
JWT_SECRET_KEY=your-secret-key
```

## Key Implementation Details

### Authentication Flow
1. User registers/logs in via /api/auth routes
2. Server returns JWT token
3. Frontend stores token in localStorage
4. Token automatically added to requests via axios interceptor
5. Protected routes use @jwt_required() decorator

### Game Flow Pattern
1. Frontend sends bet amount to game endpoint
2. Backend validates user balance
3. Game logic class executes game rules
4. Result updates user balance in database
5. Game history record created
6. Updated balance returned to frontend

### Virtual Currency System
- Users start with $1000 balance
- Balance stored in users table
- Each game outcome updates balance atomically
- Game history tracks all bets and winnings

## Database Schema

**users table**:
- id, username (unique), password_hash, balance (default 1000), created_at

**game_history table**:
- id, user_id (FK), game_type, bet_amount, result (win/lose/push), winnings, timestamp, details (JSON)

## Important Notes

- Active Blackjack games stored in memory (active_games dict) - in production, use Redis
- All game outcomes are server-authoritative to prevent cheating
- Balance updates and history recording happen in the same transaction
- Frontend balance updates optimistically after each game result
