import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8385354039:AAF6rgn5uLg-oXYTHJCYkoz2XIg5xa5HYPQ"
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

MENUS = {
    "main": {
        "text": "👋 Привет! Это бот-обучалка по Git.\n\nВыбери раздел:",
        "buttons": [
            ("📘 Теория Git", "theory_menu"),
            ("🛠 Основные команды", "commands"),
            ("❓ Мини-тест (7 вопросов)", "quiz_start"),
            ("🏁 Завершить обучение", "finish"),
        ]
    },
    "theory_menu": {
        "text": "📘 *Теория Git*\n\nВыбери тему для изучения:",
        "buttons": [
            ("1️⃣ Что такое Git", "th_what"),
            ("2️⃣ Основные концепции", "th_concepts"),
            ("3️⃣ Рабочий процесс", "th_workflow"),
            ("4️⃣ Ветвление и слияние", "th_branch"),
            ("5️⃣ Удалённые репозитории", "th_remote"),
            ("6️⃣ Разрешение конфликтов", "th_conflict"),
            ("⬅️ Назад", "main"),
        ]
    },
    "th_what": {
        "text": (
            "📘 *Что такое Git?*\n\n"
            "*Git* — это распределённая система контроля версий, "
            "созданная Линусом Торвальдсом в 2005 году для разработки ядра Linux.\n\n"
            "*Зачем нужен Git?*\n"
            "• 🔹 Хранить всю историю изменений кода\n"
            "• 🔹 Откатываться к любой предыдущей версии\n"
            "• 🔹 Работать над проектом нескольким людям одновременно\n"
            "• 🔹 Создавать экспериментальные ветки без риска для основного кода\n"
            "• 🔹 Синхронизировать код между компьютерами через серверы (GitHub, GitLab)\n\n"
            "*Отличие от SVN/CVS:*\n"
            "В Git каждый разработчик имеет *полную копию* репозитория со всей историей. "
            "Это делает систему быстрой и надёжной."
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_concepts": {
        "text": (
            "📘 *Основные концепции Git*\n\n"
            "🔸 *Репозиторий (repository)* — папка проекта с историей Git (скрытая папка `.git`).\n\n"
            "🔸 *Коммит (commit)* — снимок (snapshot) всех файлов в определённый момент времени. "
            "У каждого коммита есть уникальный хеш (например, `a3f9b2c`), автор и сообщение.\n\n"
            "🔸 *Ветка (branch)* — это просто указатель на определённый коммит. "
            "По умолчанию главная ветка называется `main` (ранее `master`).\n\n"
            "🔸 *HEAD* — специальный указатель на текущую ветку/коммит, в котором ты находишься.\n\n"
            "🔸 *Индекс (staging area)* — промежуточная зона, куда попадают файлы перед коммитом."
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_workflow": {
        "text": (
            "📘 *Рабочий процесс Git*\n\n"
            "Файл в Git проходит через *3 состояния*:\n\n"
            "1️⃣ *Working Directory* (рабочая папка)\n"
            "   └─ Здесь ты редактируешь файлы\n\n"
            "2️⃣ *Staging Area / Index* (индекс)\n"
            "   └─ Сюда попадают файлы после `git add`\n"
            "   └─ Это «черновик» следующего коммита\n\n"
            "3️⃣ *Repository* (.git)\n"
            "   └─ Сюда попадают файлы после `git commit`\n"
            "   └─ Это уже история\n\n"
            "📌 *Типичный цикл работы:*\n"
            "`изменил → git add → git commit → повторить`"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_branch": {
        "text": (
            "📘 *Ветвление и слияние*\n\n"
            "*Ветка* — это способ параллельной разработки. "
            "Например:\n"
            "• `main` — стабильная версия\n"
            "• `feature/login` — новая функция входа\n"
            "• `bugfix/header` — исправление бага\n\n"
            "*Слияние (merge)* — объединение изменений из одной ветки в другую.\n\n"
            "🔸 *Типы слияния:*\n"
            "• *Fast-forward* — если в основной ветке не было новых коммитов\n"
            "• *Three-way merge* — если были изменения в обеих ветках\n\n"
            "🔸 *Популярные стратегии:*\n"
            "• *Git Flow* — ветки `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`\n"
            "• *GitHub Flow* — упрощённая: только `main` и `feature/*`"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_remote": {
        "text": (
            "📘 *Удалённые репозитории*\n\n"
            "*Remote* — это версия проекта, размещённая в интернете "
            "(например, на GitHub, GitLab, Bitbucket).\n\n"
            "🔸 *git clone <url>* — клонировать удалённый репозиторий к себе\n\n"
            "🔸 *git remote add origin <url>* — добавить удалённый репозиторий\n\n"
            "🔸 *git push* — отправить свои коммиты на сервер\n"
            "   `git push origin main`\n\n"
            "🔸 *git pull* — получить изменения с сервера и сразу слить их\n"
            "   (это `git fetch` + `git merge` в одной команде)\n\n"
            "🔸 *git fetch* — только скачать изменения, без слияния\n\n"
            "По умолчанию удалённый репозиторий называется `origin`."
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_conflict": {
        "text": (
            "📘 *Разрешение конфликтов*\n\n"
            "*Конфликт* возникает, когда две ветки изменяют *одни и те же строки* "
            "в одном файле, и Git не может сам решить, чью версию взять.\n\n"
            "🔸 *Как выглядит конфликт в файле:*\n"
            "```\n"
            "<<<<<<< HEAD\n"
            "Моя версия строки\n"
            "=======\n"
            "Версия из другой ветки\n"
            ">>>>>>> feature-branch\n"
            "```\n\n"
            "🔸 *Что делать:*\n"
            "1. Открыть файл в редакторе\n"
            "2. Выбрать нужную версию (или объединить)\n"
            "3. Удалить служебные метки `<<<<<<<`, `=======`, `>>>>>>>`\n"
            "4. Выполнить `git add <файл>`\n"
            "5. Сделать `git commit`\n\n"
            "💡 *Совет:* используй `git pull --rebase` и делай маленькие коммиты — "
            "так конфликты возникают реже."
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "commands": {
        "text": "🛠 Выбери команду Git, которую хочешь изучить:",
        "buttons": [
            ("git init",     "cmd_init"),
            ("git add",      "cmd_add"),
            ("git commit",   "cmd_commit"),
            ("git branch",   "cmd_branch"),
            ("git merge",    "cmd_merge"),
            ("git push",     "cmd_push"),
            ("⬅️ Назад",     "main"),
        ]
    },
    "cmd_init":   {"text": "🔹 *git init*\n\nИнициализирует новый Git-репозиторий.\n\n`git init`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_add":    {"text": "🔹 *git add*\n\nДобавляет файлы в индекс.\n\n`git add .` — добавить все изменения", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_commit": {"text": "🔹 *git commit*\n\nСохраняет изменения в историю.\n\n`git commit -m \"сообщение\"`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_branch": {"text": "🔹 *git branch*\n\nРабота с ветками.\n\n`git branch new-feature` — создать ветку", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_merge":  {"text": "🔹 *git merge*\n\nСливает ветки.\n\n`git merge new-feature`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_push":   {"text": "🔹 *git push*\n\nОтправляет коммиты на сервер.\n\n`git push origin main`", "buttons": [("⬅️ К списку команд", "commands")]},
    "finish": {
        "text": (
            "🏁 *Обучение завершено!*\n\n"
            "Ты изучил:\n"
            "✔ Теорию Git (6 тем)\n"
            "✔ Основные команды\n"
            "✔ Прошёл тест из 7 вопросов\n\n"
            "Удачи в проектах! 🚀"
        ),
        "buttons": [("🔄 Начать заново", "main")]
    },
}

QUIZ = [
    {
        "q": "❓ *Вопрос 1/7*\nКакая команда создаёт новый Git-репозиторий?",
        "options": [
            ("git start",  "wrong"),
            ("git init",   "right"),
            ("git new",    "wrong"),
            ("git create", "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 2/7*\nКакая команда добавляет файлы в индекс (staging area)?",
        "options": [
            ("git add",    "right"),
            ("git stage",  "wrong"),
            ("git commit", "wrong"),
            ("git push",   "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 3/7*\nЧто делает команда `git commit -m \"msg\"`?",
        "options": [
            ("Отправляет код на сервер", "wrong"),
            ("Сохраняет проиндексированные изменения в историю", "right"),
            ("Создаёт новую ветку", "wrong"),
            ("Удаляет файл", "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 4/7*\nКакая команда создаёт новую ветку?",
        "options": [
            ("git branch new-name", "right"),
            ("git new new-name",    "wrong"),
            ("git create new-name", "wrong"),
            ("git fork new-name",   "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 5/7*\nЧто делает `git clone <url>`?",
        "options": [
            ("Удаляет репозиторий", "wrong"),
            ("Копирует удалённый репозиторий на локальный компьютер", "right"),
            ("Создаёт новую ветку", "wrong"),
            ("Отправляет коммиты на сервер", "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 6/7*\nКакая команда получает изменения с сервера И сразу сливает их?",
        "options": [
            ("git fetch", "wrong"),
            ("git push",  "wrong"),
            ("git pull",  "right"),
            ("git merge", "wrong"),
        ]
    },
    {
        "q": "❓ *Вопрос 7/7*\nКак выглядит метка конфликта в файле?",
        "options": [
            ("<<<<<<< HEAD ... ======= ... >>>>>>> branch", "right"),
            ("### CONFLICT ###", "wrong"),
            ("!!! MERGE ERROR !!!", "wrong"),
            ("[CONFLICT] text", "wrong"),
        ]
    },
]


def create_keyboard(buttons):
    keyboard = [[InlineKeyboardButton(text, callback_data=cb)] for text, cb in buttons]
    return InlineKeyboardMarkup(keyboard)


async def show_menu(query, menu_name):
    menu = MENUS[menu_name]
    await query.edit_message_text(
        text=menu["text"],
        reply_markup=create_keyboard(menu["buttons"]),
        parse_mode="Markdown"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = MENUS["main"]
    await update.message.reply_text(
        text=menu["text"],
        reply_markup=create_keyboard(menu["buttons"]),
        parse_mode="Markdown"
    )


async def start_quiz(query, context):
    context.user_data["quiz_index"] = 0
    context.user_data["quiz_score"] = 0
    await show_quiz_question(query, context)


async def show_quiz_question(query, context):
    idx = context.user_data["quiz_index"]
    question = QUIZ[idx]
    buttons = question["options"] + [("🚪 Выйти в меню", "main")]
    await query.edit_message_text(
        text=question["q"],
        reply_markup=create_keyboard(buttons),
        parse_mode="Markdown"
    )


async def handle_quiz_answer(query, context):
    answer = query.data
    idx = context.user_data["quiz_index"]
    score = context.user_data["quiz_score"]

    if answer == "right":
        score += 1
        context.user_data["quiz_score"] = score
        feedback = f"✅ Верно! Правильных ответов: {score}"
    else:
        feedback = f"❌ Неверно. Правильных ответов: {score}"

    idx += 1
    context.user_data["quiz_index"] = idx

    if idx >= len(QUIZ):
        await query.edit_message_text(
            text=(
                f"{feedback}\n\n"
                f"🏆 *Тест завершён!*\n"
                f"Твой результат: *{score} из {len(QUIZ)}*\n\n"
                + ("🎉 Отличный результат!" if score == len(QUIZ) else
                   "👍 Хороший результат!" if score >= len(QUIZ) * 0.7 else
                   "📚 Стоит повторить теорию.")
            ),
            reply_markup=create_keyboard([
                ("🔄 Пройти ещё раз", "quiz_start"),
                ("📘 К теории", "theory_menu"),
                ("🏠 В главное меню", "main"),
            ]),
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(
            text=feedback + "\n\nСледующий вопрос:",
            reply_markup=create_keyboard([])
        )
        await show_quiz_question(query, context)


async def buttons_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    button_id = query.data

    if button_id == "quiz_start":
        await start_quiz(query, context)
        return

    if "quiz_index" in context.user_data:
        idx = context.user_data["quiz_index"]
        if 0 <= idx < len(QUIZ):
            options_cb = [cb for _, cb in QUIZ[idx]["options"]]
            if button_id in options_cb or button_id == "main":
                if button_id == "main":
                    context.user_data.pop("quiz_index", None)
                    context.user_data.pop("quiz_score", None)
                    await show_menu(query, "main")
                    return
                await handle_quiz_answer(query, context)
                return

    if button_id in MENUS:
        if button_id == "main":
            context.user_data.pop("quiz_index", None)
            context.user_data.pop("quiz_score", None)
        await show_menu(query, button_id)
    else:
        await query.edit_message_text("⚠️ Такого раздела нет.")


def main():
    if not RENDER_URL:
        raise RuntimeError("Не задана переменная RENDER_EXTERNAL_URL")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons_handler))

    port = int(os.environ.get("PORT", 8080))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{RENDER_URL}/{TOKEN}",
    )


if __name__ == "__main__":
    main()
