from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from game_logic import create_inline_keyboard, init_board, check_winner, bot_move, end_game
from keyboards import create_profile_play_buttons, create_register_button
from user_data import user_data, REGISTER_NAME

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in user_data:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
        return

    context.user_data["board"] = init_board()
    await update.message.reply_text("Игра началась! Ваш ход:", reply_markup=create_inline_keyboard(context.user_data["board"]))

async def handle_move(update: Update, context: CallbackContext) -> None:
    if "board" not in context.user_data:
        await update.callback_query.message.reply_text("Игра не начата. Введите /start для начала игры.")
        return

    board = context.user_data["board"]
    query = update.callback_query
    move = query.data
    row, col = map(int, move.split(","))
    if board[row][col] != " ":
        await query.answer("Эта клетка уже занята, выберите другую.")
        return

    board[row][col] = "X"
    winner = check_winner(board)
    if winner:
        await end_game(update, context, winner)
        return

    bot_move(board)
    winner = check_winner(board)
    if winner:
        await end_game(update, context, winner)
        return

    await query.edit_message_text("Ваш ход:", reply_markup=create_inline_keyboard(board))

async def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        await update.message.reply_text("Вы уже зарегистрированы.", reply_markup=create_profile_play_buttons())
        return

    await update.message.reply_text("Введите ваше имя:")
    return REGISTER_NAME

async def register_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.text
    user_data[user_id] = {'name': name, 'rating': 0}
    await update.message.reply_text("Регистрация успешна!", reply_markup=create_profile_play_buttons())
    return ConversationHandler.END

async def register_callback(update: Update, context: CallbackContext):
    await register(update, context)

async def profile_callback(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_info = user_data.get(user_id, {})
    name = user_info.get('name', 'Неизвестно')
    rating = user_info.get('rating', 0)
    await update.message.reply_text(f"Ваш профиль:\nИмя: {name}\nРейтинг: {rating}")

async def change_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
        return

    await update.message.reply_text("Введите ваше новое имя:")
    return REGISTER_NAME

async def change_name_save(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    new_name = update.message.text
    user_data[user_id]['name'] = new_name
    await update.message.reply_text(f"Имя успешно изменено на {new_name}.", reply_markup=create_profile_play_buttons())
    return ConversationHandler.END

async def rating(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in user_data:
        rating = user_data[user_id]['rating']
        await update.message.reply_text(f"Ваш текущий рейтинг: {rating}")
    else:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
