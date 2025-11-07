import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (username, password) => api.post('/auth/register', { username, password }),
  login: (username, password) => api.post('/auth/login', { username, password })
};

export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  getHistory: () => api.get('/user/history'),
  getLeaderboard: () => api.get('/user/leaderboard')
};

export const gamesAPI = {
  // Blackjack
  startBlackjack: (bet) => api.post('/games/blackjack/start', { bet }),
  blackjackHit: () => api.post('/games/blackjack/hit'),
  blackjackStand: () => api.post('/games/blackjack/stand'),

  // Roulette
  playRoulette: (bet, bet_type, bet_value) => api.post('/games/roulette/play', { bet, bet_type, bet_value }),

  // Baccarat
  playBaccarat: (bet, bet_on) => api.post('/games/baccarat/play', { bet, bet_on }),

  // Poker
  playPoker: (bet) => api.post('/games/poker/play', { bet })
};

export default api;
