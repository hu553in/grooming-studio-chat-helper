import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

ADDRESS = (
    "ул. Чокана Валиханова, д. 2, офис №3 (вход с торца дома, слева от шлагбаума, на домофоне — 3)"
)

form_state = {}

BREED_ITEMS = [
    (
        "breed_corgi",
        "Вельш-корги",
        "🐶 Вельш-корги\n\n"
        "Комплексный груминг — 3000 ₽.\n"
        "Мытьё, сушка, вычёс, лапы и гигиена входят в стоимость.\n\n"
        "Точная цена может меняться в зависимости от состояния шерсти и пожеланий по стрижке.",
    ),
    (
        "breed_spitz",
        "Шпиц",
        "🦊 Шпиц\n\n"
        "Комплексный груминг — 3500 ₽.\n"
        "Цена зависит от размера собаки, состояния шерсти и колтунов.",
    ),
    (
        "breed_york",
        "Йоркширский терьер",
        "Стоимость: 1500–2500 ₽\n"
        "⏱ Примерное время: 2,5–3 ч\n\n"
        "Цена зависит от длины шерсти, наличия колтунов, "
        "адаптации к грумингу и пожеланий по стрижке.\n\n"
        "В комплекс входит:\n"
        "• гигиеническая обработка,\n"
        "• стрижка когтей,\n"
        "• чистка ушек и глаз,\n"
        "• купание с профессиональной косметикой,\n"
        "• уходовая маска для мягкости и блеска шерсти,\n"
        "• сушка и бережный выдув компрессором,\n"
        "• стрижка по желанию.",
    ),
]

BREED_BY_ID = {breed_id: text for breed_id, _, text in BREED_ITEMS}

NAILS_TEXT = (
    "По когтям\n\n"
    "Я работаю без жёсткой фиксации «через силу».\n"
    "Если собаке тревожно или она активно сопротивляется, я не буду стригать когти насильно.\n\n"
    "Я пробую разные варианты:\n"
    "• угощение и переключение внимания,\n"
    "• работа на полу, если так спокойнее,\n"
    "• перерывы и маленькие шаги,\n"
    "• аккуратный подпил поэтапно.\n\n"
    "Если собака всё равно против, мы останавливаемся и можем "
    "обсудить с вами адаптационные визиты, чтобы постепенно "
    "сформировать более спокойное отношение к уходу."
)

ADAPTATION_TEXT = (
    "Адаптация — это короткие визиты, чтобы собака без стресса "
    "познакомилась со студией, запахами, звуками, инструментами, "
    "мной и самим процессом.\n\n"
    "Кому особенно подходит адаптация:\n"
    "• тревожные и чувствительные собаки,\n"
    "• щенки и первый груминг,\n"
    "• собаки с негативным опытом в прошлом,\n"
    "• те, кто боится фена, стола, ножниц,\n"
    "• собаки, которые не дают трогать лапы, морду или уши.\n\n"
    "На адаптационных визитах мы:\n"
    "• знакомимся со студией,\n"
    "• даём понюхать и спокойно посмотреть на инструменты,\n"
    "• двигаемся в очень мягком темпе,\n"
    "• используем поощрение и паузы.\n\n"
    "Цель адаптации — чтобы собака чувствовала себя уверенно и безопасно на уходе."
)

FORM_TEXT = (
    "Перед визитом, пожалуйста, заполните небольшую анкету.\n\n"
    "В анкете будут вопросы про:\n"
    "• имя и породу собаки,\n"
    "• возраст,\n"
    "• как собака сейчас переносит груминг,\n"
    "• уровень тревожности и особенности поведения,\n"
    "• ограничения по здоровью и питанию.\n\n"
    "Анкета помогает заранее учесть потребности вашего питомца "
    "и подобрать максимально бережный подход.\n\n"
    "Ссылка на анкету — https://forms.gle/AknnpWHxSKjS929bA"
)

REVIEW_TEXT = (
    "Спасибо, что выбрали нашу студию и доверили нам заботу о вашем питомце ✨\n\n"
    "Если вам всё понравилось, будем очень благодарны за отзыв в 2ГИС "
    "— для нас это большая поддержка и помощь в развитии 🧡\n\n"
    "Вот ссылка:\n"
    "https://go.2gis.com/nrLV8\n\n"
    "Спасибо за доверие и будем рады видеть вас снова! 🐶✨"
)


async def send_main_menu(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Подтверждение записи", callback_data="booking")],
            [InlineKeyboardButton("Запрос отзыва", callback_data="review_request")],
            [InlineKeyboardButton("Стоимость услуг", callback_data="prices_menu")],
            [InlineKeyboardButton("Когти", callback_data="nails")],
            [InlineKeyboardButton("Адаптация", callback_data="adaptation")],
            [InlineKeyboardButton("Анкета", callback_data="form")],
        ]
    )
    await context.bot.send_message(chat_id, "Меню:", reply_markup=markup)


async def send_breeds_menu(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text=button_text, callback_data=breed_id)]
            for breed_id, button_text, _ in BREED_ITEMS
        ]
        + [[InlineKeyboardButton("⬅️ Назад", callback_data="menu_main")]]
    )
    await context.bot.send_message(
        chat_id, "Стоимость услуг — выберите породу:", reply_markup=markup
    )


async def send_answer_main(chat_id: int, text: str, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Назад", callback_data="menu_main")]])
    await context.bot.send_message(chat_id, text, reply_markup=markup)


async def send_answer_breed(chat_id: int, text: str, context: ContextTypes.DEFAULT_TYPE):
    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("⬅️ К породам", callback_data="prices_menu")],
            [InlineKeyboardButton("🏠 В меню", callback_data="menu_main")],
        ]
    )
    await context.bot.send_message(chat_id, text, reply_markup=markup)


async def start_booking(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    form_state[chat_id] = {"step": "date"}
    await context.bot.send_message(chat_id, "Введите дату визита (например: 12 января):")


async def handle_booking_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None:
        return
    chat_id = message.chat.id
    form_state[chat_id]["date"] = message.text
    form_state[chat_id]["step"] = "time"
    await context.bot.send_message(chat_id, "Введите время визита (например: 14:00):")


async def handle_booking_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None:
        return
    chat_id = message.chat.id
    form_state[chat_id]["time"] = message.text
    date = form_state[chat_id]["date"]
    time = form_state[chat_id]["time"]
    text = (
        "Здравствуйте!\n\n"
        f"Ваш питомец записан на груминг:\n"
        f"📅 Дата: {date}\n"
        f"⏰ Время: {time}\n"
        f"📍 Адрес: {ADDRESS}\n"
        "🗺 2ГИС: https://go.2gis.com/nrLV8\n\n"
        "В студии для поощрения есть говяжье лёгкое.\n\n"
        "Если у вашего питомца есть ограничения по питанию или особые "
        "предпочтения — возьмите, пожалуйста, с собой любимые вкусняшки "
        "или немного корма 🧡\n\n"
        "Также в студии представлены разные натуральные лакомства "
        "от Омского производителя (@korgi_smi) — при желании вы можете "
        "приобрести их у нас 🐾\n\n"
        "Также я отправляю памятку для владельцев перед грумингом."
    )
    await send_answer_main(chat_id, text, context)
    form_state.pop(chat_id, None)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat.id
    form_state.pop(chat_id, None)
    await send_main_menu(chat_id, context)


async def _handle_static_callback(
    chat_id: int, data: str, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    handlers = {
        "review_request": lambda: send_answer_main(chat_id, REVIEW_TEXT, context),
        "prices_menu": lambda: send_breeds_menu(chat_id, context),
        "nails": lambda: send_answer_main(chat_id, NAILS_TEXT, context),
        "adaptation": lambda: send_answer_main(chat_id, ADAPTATION_TEXT, context),
        "form": lambda: send_answer_main(chat_id, FORM_TEXT, context),
    }
    handler = handlers.get(data)
    if handler is not None:
        await handler()
        return True
    if data in BREED_BY_ID:
        await send_answer_breed(chat_id, BREED_BY_ID[data], context)
        return True
    return False


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None or query.message is None:
        return
    data = query.data
    chat_id = query.message.chat.id
    if data is None:
        await query.answer(text="Что-то пошло не так 😅")
        return

    if data == "menu_main":
        await query.answer()
        form_state.pop(chat_id, None)
        await send_main_menu(chat_id, context)
        return

    if data == "booking":
        await query.answer()
        form_state.pop(chat_id, None)
        await start_booking(chat_id, context)
        return

    if await _handle_static_callback(chat_id, data, context):
        await query.answer()
        return

    await query.answer(text="Что-то пошло не так 😅")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    chat_id = update.message.chat.id
    state = form_state.get(chat_id, {})
    step = state.get("step")
    if step == "date":
        await handle_booking_date(update, context)
    elif step == "time":
        await handle_booking_time(update, context)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")
    print("Bot is running...")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.run_polling()


if __name__ == "__main__":
    main()
