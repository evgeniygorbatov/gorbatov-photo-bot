from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Вопросы
(Q1, Q2, Q3, Q4, Q5) = range(5)

# Telegram ID куда отправлять заявки
OWNER_CHAT_ID = 5821754568  # Твой chat_id

# Хранилище для ответов
user_data_store = {}

def start(update: Update, context: CallbackContext):
    user_data_store[update.message.chat_id] = {}
    reply_keyboard = [['Портретная', 'Love story'], ['Семейная', 'Контент для блога'], ['Другое']]
    update.message.reply_text(
        "Привет.\n"
        "Я помогу подобрать фотосессию, которая подойдёт именно тебе — по настроению, формату и целям. "
        "Ответь на несколько коротких вопросов — и мы всё организуем.\n\n"
        "Какую фотосессию ты хочешь?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return Q1

def q1(update, context):
    user_data_store[update.message.chat_id]['Тип'] = update.message.text
    reply_keyboard = [['В ближайшие дни', 'В течение недели'], ['В этом месяце', 'Другое (укажу сам)']]
    update.message.reply_text("Когда хочешь провести съёмку?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q2

def q2(update, context):
    user_data_store[update.message.chat_id]['Дата'] = update.message.text
    reply_keyboard = [['Один', 'Двое'], ['Семья / группа', 'Другое']]
    update.message.reply_text("Сколько человек будет на съёмке?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q3

def q3(update, context):
    user_data_store[update.message.chat_id]['Людей'] = update.message.text
    reply_keyboard = [['Есть референсы', 'Хочу, чтобы ты помог с идеей'], ['Пока не знаю', 'Другое']]
    update.message.reply_text("Есть ли идеи или вдохновение для съёмки?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q4

def q4(update, context):
    user_data_store[update.message.chat_id]['Идея'] = update.message.text
    reply_keyboard = [['До 5 000 ₽', '5 000–10 000 ₽'], ['10 000+ ₽', 'Не знаю / хочу обсудить']]
    update.message.reply_text("На какой бюджет ты рассчитываешь?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return Q5

def q5(update, context):
    user_data_store[update.message.chat_id]['Бюджет'] = update.message.text
    update.message.reply_text("Спасибо! Мои съёмки начинаются от 4 000 ₽. Я получил все ответы — скоро свяжусь с тобой и помогу выбрать лучший вариант.")
    
    # Отправляем все ответы владельцу
    answers = user_data_store[update.message.chat_id]
    message = f"📸 Новая заявка от @{update.message.from_user.username or 'неизвестного пользователя'}:\n\n"
    for key, value in answers.items():
        message += f"{key}: {value}\n"
    
    try:
        # Отправка сообщения владельцу
        context.bot.send_message(chat_id=OWNER_CHAT_ID, text=message)
    except Exception as e:
        update.message.reply_text("Извините, произошла ошибка при отправке заявки. Пожалуйста, попробуйте еще раз позже или свяжитесь напрямую.")
        print(f"Ошибка отправки заявки: {e}")
    
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Диалог отменён.")
    return ConversationHandler.END

def main():
    TOKEN = "8171400853:AAGLdEEbD2TJJZ__iYPr67xjK-FYGOaCZhw"  # Ваш токен
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            Q1: [MessageHandler(Filters.text & ~Filters.command, q1)],
            Q2: [MessageHandler(Filters.text & ~Filters.command, q2)],
            Q3: [MessageHandler(Filters.text & ~Filters.command, q3)],
            Q4: [MessageHandler(Filters.text & ~Filters.command, q4)],
            Q5: [MessageHandler(Filters.text & ~Filters.command, q5)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

