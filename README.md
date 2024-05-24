# Telegram Bot for Tic-Tac-Toe Game

This is a simple Telegram bot that allows users to play Tic-Tac-Toe with the bot. Users can register, view their profile, and play the game. The bot keeps track of user ratings, which are updated based on the game outcomes.

## Features

- User registration and profile management
- Tic-Tac-Toe game with the bot
- User ratings updated based on game outcomes
- Commands and buttons for easy interaction

## Installation

Follow these steps to install and run the bot on a Linux server.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/olegdobrynin/tictactoe-tgbot.git
    cd tictactoe-tgbot
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a file named `.env` in the project root directory.
    - Add your Telegram bot token to the `.env` file:
      ```env
      TOKEN=your_telegram_bot_token
      ```

5. **Initialize the database:**
    The database will be initialized automatically when the bot is started for the first time.

6. **Run the bot:**
    ```bash
    python main.py
    ```

## Project Structure

tictactoe-tgbot/
├── config.py
├── game_logic.py
├── handlers.py
├── keyboards.py
├── main.py
├── requirements.txt
├── user_data.py
├── user_data.json
├── .env
└── README.md



### `main.py`
- Entry point of the bot application.

### `handlers.py`
- Contains all the command and callback query handlers.

### `game_logic.py`
- Contains the game logic for Tic-Tac-Toe.

### `keyboards.py`
- Contains the functions to create various keyboards used in the bot.

### `database.py`
- Manages the database operations for user data.

### `config.py`
- Loads the environment variables.

### `requirements.txt`
- Lists all the dependencies required by the project.

### `.env`
- Stores the environment variables (e.g., bot token).

## Usage

### Registering a User
1. Send `/register` to the bot.
2. Enter your name when prompted.

### Viewing Profile
- Click the "ПРОФИЛЬ" button to view your profile information, including your name and rating.

### Playing the Game
- Click the "ИГРАТЬ" button to start a new game of Tic-Tac-Toe with the bot.

### Changing Name
1. Send `/change_name` to the bot.
2. Enter your new name when prompted.

### Viewing Rating
- Send `/rating` to view your current rating.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
