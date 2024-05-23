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
    cd telegram-tictactoe-bot
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

