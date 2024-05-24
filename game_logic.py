from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import random

def init_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    for row in board:
        for cell in row:
            if cell == " ":
                return None
    return "Draw"

def create_inline_keyboard(board):
    keyboard = []
    for i, row in enumerate(board):
        keyboard_row = []
        for j, cell in enumerate(row):
            text = cell if cell != " " else " "
            keyboard_row.append(InlineKeyboardButton(text, callback_data=f"{i},{j}"))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(keyboard)

def bot_move(board):
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "O"

def board_to_str(board):
    return "\n".join([" | ".join(row) for row in board])
