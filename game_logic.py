from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import random
from user_data import user_data

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
    if all(board[row][col] != " " for row in range(3) for col in range(3)):
        return "Draw"
    return None

def create_inline_keyboard(board):
    keyboard = []
    for r in range(3):
        row = []
        for c in range(3):
            text = board[r][c] if board[r][c] != " " else " "
            row.append(InlineKeyboardButton(text, callback_data=f"{r},{c}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def bot_move(board):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = "O"

async def end_game(update: Update, context: CallbackContext, winner):
    board = context.user_data["board"]
    user_id = update.callback_query.from_user.id

    if winner == "Draw":
        await update.callback_query.message.edit_text(f"Игра окончена. Ничья!\n{board_to_str(board)}", reply_markup=None)
    else:
        if winner == "X":
            user_data[user_id]['rating'] += 1
            await update.callback_query.message.edit_text(f"Игра окончена. Победитель: {winner}!\n{board_to_str(board)}\nВаш рейтинг: {user_data[user_id]['rating']}", reply_markup=None)
        else:
            user_data[user_id]['rating'] -= 1
            await update.callback_query.message.edit_text(f"Игра окончена. Победитель: {winner}!\n{board_to_str(board)}\nВаш рейтинг: {user_data[user_id]['rating']}", reply_markup=None)

    context.user_data.pop("board")

def board_to_str(board):
    return "\n".join([" | ".join(row) for row in board])
