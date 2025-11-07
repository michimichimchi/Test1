# Mini Games Casino

A full-stack web application featuring four classic casino games: Blackjack, Roulette, Baccarat, and Poker. Built with React and Flask, featuring user authentication, virtual currency, game history tracking, and leaderboards.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Four Casino Games**:
  - **Blackjack**: Classic card game against the dealer
  - **Roulette**: European roulette with various betting options
  - **Baccarat**: Traditional punto banco style
  - **Poker**: 5-card draw against the dealer
- **Virtual Currency**: Start with $1000 chips, bet and win across all games
- **Game History**: Track all your past games and results
- **Leaderboard**: See top players by balance
- **Responsive Design**: Casino-themed UI with modern styling

## Tech Stack

### Backend
- Python 3.x
- Flask (Web framework)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- MySQL (Database)
- bcrypt (Password hashing)

### Frontend
- React 18
- React Router (Navigation)
- Axios (API calls)
- CSS3 (Styling)

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher
- npm or yarn

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Test1
```

### 2. Set up MySQL Database

Create a new MySQL database:

```sql
CREATE DATABASE mini_games_db;
```

### 3. Backend Setup

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your database credentials:

```
DATABASE_URL=mysql+pymysql://your_username:your_password@localhost/mini_games_db
JWT_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 4. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd ../frontend
npm install
```

## Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The Flask server will start on `http://localhost:5000`

### Start the Frontend Development Server

In a new terminal:

```bash
cd frontend
npm start
```

The React app will start on `http://localhost:3000`

## Usage

1. **Register**: Create a new account with a username and password
2. **Login**: Log in with your credentials
3. **Play Games**: Navigate to any of the four games from the home page
4. **Place Bets**: Each game starts with a betting interface
5. **Track Progress**: View your game history and check the leaderboard

## Game Rules

### Blackjack
- Goal: Get as close to 21 as possible without going over
- Beat the dealer's hand to win
- Payout: 1:1 (bet $10, win $10)

### Roulette
- Bet on numbers (0-36), colors (red/black), or ranges (low/high, even/odd)
- Single number: 35:1 payout
- Other bets: 1:1 payout

### Baccarat
- Bet on Player, Banker, or Tie
- Player: 1:1 payout
- Banker: 0.95:1 payout (5% commission)
- Tie: 8:1 payout

### Poker (5-Card Draw)
- Get a better 5-card hand than the dealer
- Payout: 1:1

## Project Structure

```
Test1/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   └── game_history.py    # Game history model
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   ├── games.py           # Game endpoints
│   │   └── user.py            # User/leaderboard routes
│   └── game_logic/
│       ├── blackjack.py       # Blackjack game logic
│       ├── roulette.py        # Roulette game logic
│       ├── baccarat.py        # Baccarat game logic
│       └── poker.py           # Poker game logic
└── frontend/
    ├── public/
    │   └── index.html
    └── src/
        ├── components/        # Reusable components
        ├── pages/            # Page components
        ├── services/         # API service
        ├── styles/           # CSS files
        └── App.js
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### User
- `GET /api/user/profile` - Get user profile (protected)
- `GET /api/user/history` - Get game history (protected)
- `GET /api/user/leaderboard` - Get leaderboard

### Games
- `POST /api/games/blackjack/start` - Start blackjack game
- `POST /api/games/blackjack/hit` - Hit in blackjack
- `POST /api/games/blackjack/stand` - Stand in blackjack
- `POST /api/games/roulette/play` - Play roulette
- `POST /api/games/baccarat/play` - Play baccarat
- `POST /api/games/poker/play` - Play poker

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected API routes
- CORS configuration
- Input validation

## Future Enhancements

- Real-time multiplayer support with WebSockets
- More casino games (Craps, Slots, etc.)
- Social features (friends, chat)
- Achievements and rewards system
- Mobile app version
- Payment integration for real money (with proper licensing)

## License

This project is for educational purposes only.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
