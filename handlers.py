from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from game_logic import init_board, check_winner, create_inline_keyboard, bot_move, board_to_str
from keyboards import create_register_button, create_profile_play_buttons
from user_data import update_user_data, get_user_data, load_user_data

REGISTER_NAME = range(1)

# Обработка хода пользователя
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

# Завершение игры и объявление победителя
async def end_game(update: Update, context: CallbackContext, winner):
    board = context.user_data["board"]
    user_id = update.callback_query.from_user.id

    if winner == "Draw":
        await update.callback_query.message.edit_text(f"Игра окончена. Ничья!\n{board_to_str(board)}", reply_markup=None)
    else:
        if winner == "X":
            rating = get_user_data(user_id, 'rating', 0) + 1
            update_user_data(user_id, 'rating', rating)
            await update.callback_query.message.edit_text(f"Игра окончена. Победитель: {winner}!\n{board_to_str(board)}\nВаш рейтинг: {rating}", reply_markup=None)
        else:
            rating = get_user_data(user_id, 'rating', 0) - 1
            update_user_data(user_id, 'rating', rating)
            await update.callback_query.message.edit_text(f"Игра окончена. Победитель: {winner}!\n{board_to_str(board)}\nВаш рейтинг: {rating}", reply_markup=None)

    context.user_data.pop("board")

# Начало новой игры
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = load_user_data()

    if str(user_id) not in user_data:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
        return

    context.user_data["board"] = init_board()
    await update.message.reply_text("Игра началась! Ваш ход:", reply_markup=create_inline_keyboard(context.user_data["board"]))

# Обработка нажатия на кнопку "ПРОФИЛЬ"
async def profile_callback(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = get_user_data(user_id, 'name', 'Неизвестно')
    rating = get_user_data(user_id, 'rating', 0)
    await update.message.reply_text(f"Ваш профиль:\nИмя: {name}\nРейтинг: {rating}")

# Обработка нажатия на кнопку "ИГРАТЬ"
async def play_callback(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data = load_user_data()

    if str(user_id) not in user_data:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
        return

    context.user_data["board"] = init_board()
    await update.message.reply_text("Игра началась! Ваш ход:", reply_markup=create_inline_keyboard(context.user_data["board"]))

# Регистрация нового пользователя
async def register(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data = load_user_data()

    if str(user_id) in user_data:
        await update.message.reply_text("Вы уже зарегистрированы.", reply_markup=create_profile_play_buttons())
        return

    await update.message.reply_text("Введите ваше имя:")
    return REGISTER_NAME

# Завершение регистрации после получения имени
async def register_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    name = update.message.text
    user_data = load_user_data()

    if str(user_id) in user_data:
        await update.message.reply_text("Вы уже зарегистрированы.", reply_markup=create_profile_play_buttons())
        return

    update_user_data(user_id, 'name', name)
    update_user_data(user_id, 'rating', 0)
    await update.message.reply_text("Регистрация успешна!", reply_markup=create_profile_play_buttons())
    return ConversationHandler.END

# Изменение имени
async def change_name(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data = load_user_data()

    if str(user_id) not in user_data:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")
        return

    await update.message.reply_text("Введите ваше новое имя:")
    return REGISTER_NAME

# Завершение изменения имени
async def change_name_save(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    new_name = update.message.text
    update_user_data(user_id, 'name', new_name)
    await update.message.reply_text(f"Имя успешно изменено на {new_name}.", reply_markup=create_profile_play_buttons())
    return ConversationHandler.END

# Проверка рейтинга
async def rating(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if str(user_id) in load_user_data():
        rating = get_user_data(user_id, 'rating')
        await update.message.reply_text(f"Ваш текущий рейтинг: {rating}")
    else:
        await update.message.reply_text("Вы не зарегистрированы. Введите /register для регистрации.")

# Регистрация обработчиков
def register_handlers(application):
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)]
        },
        fallbacks=[]
    )

    change_name_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', change_name)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_save)]
        },
        fallbacks=[]
    )

    application.add_handler(registration_handler)
    application.add_handler(change_name_handler)
    application.add_handler(CommandHandler("rating", rating))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_move))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("ПРОФИЛЬ"), profile_callback))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("ИГРАТЬ"), play_callback))
