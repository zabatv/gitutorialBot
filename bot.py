import os
import requests
from flask import Flask, request, jsonify

TOKEN = "8385354039:AAF6rgn5uLg-oXYTHJCYkoz2XIg5xa5HYPQ"
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
users = {}

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
            "🔸 *Коммит (commit)* — снимок всех файлов в определённый момент времени. "
            "У каждого коммита есть уникальный хеш, автор и сообщение.\n\n"
            "🔸 *Ветка (branch)* — указатель на определённый коммит. "
            "По умолчанию главная ветка называется `main`.\n\n"
            "🔸 *HEAD* — указатель на текущую ветку/коммит.\n\n"
            "🔸 *Индекс (staging area)* — промежуточная зона перед коммитом."
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_workflow": {
        "text": (
            "📘 *Рабочий процесс Git*\n\n"
            "Файл в Git проходит через *3 состояния*:\n\n"
            "1️⃣ *Working Directory* — здесь ты редактируешь файлы\n\n"
            "2️⃣ *Staging Area / Index* — сюда попадают файлы после `git add`\n\n"
            "3️⃣ *Repository* (.git) — сюда попадают файлы после `git commit`\n\n"
            "📌 *Типичный цикл:*\n`изменил → git add → git commit → повторить`"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_branch": {
        "text": (
            "📘 *Ветвление и слияние*\n\n"
            "*Ветка* — способ параллельной разработки.\n"
            "• `main` — стабильная версия\n"
            "• `feature/login` — новая функция\n"
            "• `bugfix/header` — исправление бага\n\n"
            "*Слияние (merge)* — объединение изменений из одной ветки в другую.\n\n"
            "🔸 *Типы слияния:*\n"
            "• *Fast-forward*\n• *Three-way merge*\n\n"
            "🔸 *Стратегии:*\n"
            "• *Git Flow*\n• *GitHub Flow*"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_remote": {
        "text": (
            "📘 *Удалённые репозитории*\n\n"
            "*Remote* — версия проекта в интернете (GitHub, GitLab, Bitbucket).\n\n"
            "🔸 `git clone <url>` — клонировать репозиторий\n"
            "🔸 `git remote add origin <url>` — добавить remote\n"
            "🔸 `git push origin main` — отправить коммиты\n"
            "🔸 `git pull` — получить и слить изменения\n"
            "🔸 `git fetch` — только скачать, без слияния"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "th_conflict": {
        "text": (
            "📘 *Разрешение конфликтов*\n\n"
            "*Конфликт* — когда две ветки изменили одни и те же строки.\n\n"
            "🔸 *Как выглядит:*\n"
            "```\n<<<<<<< HEAD\nМоя версия\n=======\nЧужая версия\n>>>>>>> feature-branch\n```\n\n"
            "🔸 *Что делать:*\n"
            "1. Открыть файл\n"
            "2. Выбрать версию\n"
            "3. Удалить метки\n"
            "4. `git add <файл>`\n"
            "5. `git commit`"
        ),
        "buttons": [("⬅️ К темам теории", "theory_menu")]
    },
    "commands": {
        "text": "🛠 Выбери команду Git:",
        "buttons": [
            ("git init",   "cmd_init"),
            ("git add",    "cmd_add"),
            ("git commit", "cmd_commit"),
            ("git branch", "cmd_branch"),
            ("git merge",  "cmd_merge"),
            ("git push",   "cmd_push"),
            ("⬅️ Назад",   "main"),
        ]
    },
    "cmd_init":   {"text": "🔹 *git init*\n\nИнициализирует новый репозиторий.\n\n`git init`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_add":    {"text": "🔹 *git add*\n\nДобавляет файлы в индекс.\n\n`git add .`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_commit": {"text": "🔹 *git commit*\n\nСохраняет изменения в историю.\n\n`git commit -m \"сообщение\"`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_branch": {"text": "🔹 *git branch*\n\n`git branch new-feature` — создать ветку", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_merge":  {"text": "🔹 *git merge*\n\n`git merge new-feature`", "buttons": [("⬅️ К списку команд", "commands")]},
    "cmd_push":   {"text": "🔹 *git push*\n\n`git push origin main`", "buttons": [("⬅️ К списку команд", "commands")]},
    "finish": {
        "text": (
            "🏁 *Обучение завершено!*\n\n"
            "Ты изучил:\n"
            "✔ Теорию Git\n"
            "✔ Основные команды\n"
            "✔ Прошёл тест\n\n"
            "Удачи в проектах! 🚀"
        ),
        "buttons": [("🔄 Начать заново", "main")]
    },
}

QUIZ = [
    {"q": "❓ *Вопрос 1/7*\nКакая команда создаёт новый Git-репозиторий?",
     "options": [("git start","wrong"),("git init","right"),("git new","wrong"),("git create","wrong")]},
    {"q": "❓ *Вопрос 2/7*\nКакая команда добавляет файлы в индекс?",
     "options": [("git add","right"),("git stage","wrong"),("git commit","wrong"),("git push","wrong")]},
    {"q": "❓ *Вопрос 3/7*\nЧто делает `git commit -m \"msg\"`?",
     "options": [("Отправляет код на сервер","wrong"),
                 ("Сохраняет проиндексированные изменения в историю","right"),
                 ("Создаёт новую ветку","wrong"),("Удаляет файл","wrong")]},
    {"q": "❓ *Вопрос 4/7*\nКакая команда создаёт новую ветку?",
     "options": [("git branch new-name","right"),("git new new-name","wrong"),
                 ("git create new-name","wrong"),("git fork new-name","wrong")]},
    {"q": "❓ *Вопрос 5/7*\nЧто делает `git clone <url>`?",
     "options": [("Удаляет репозиторий","wrong"),
                 ("Копирует удалённый репозиторий на локальный компьютер","right"),
                 ("Создаёт новую ветку","wrong"),("Отправляет коммиты на сервер","wrong")]},
    {"q": "❓ *Вопрос 6/7*\nКакая команда получает изменения и сразу сливает их?",
     "options": [("git fetch","wrong"),("git push","wrong"),("git pull","right"),("git merge","wrong")]},
    {"q": "❓ *Вопрос 7/7*\nКак выглядит метка конфликта?",
     "options": [("<<<<<<< HEAD ... ======= ... >>>>>>> branch","right"),
                 ("### CONFLICT ###","wrong"),("!!! MERGE ERROR !!!","wrong"),("[CONFLICT] text","wrong")]},
]


def kb(buttons):
    return {"inline_keyboard": [[{"text": t, "callback_data": c}] for t, c in buttons]}


def api_call(method, **kwargs):
    try:
        r = requests.post(f"{API}/{method}", json=kwargs, timeout=15)
        return r.json()
    except Exception as e:
        print(f"API error {method}: {e}")
        return None


def send_message(chat_id, text, buttons=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if buttons:
        payload["reply_markup"] = kb(buttons)
    return api_call("sendMessage", **payload)


def edit_message(chat_id, message_id, text, buttons=None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if buttons:
        payload["reply_markup"] = kb(buttons)
    return api_call("editMessageText", **payload)


def answer_callback(callback_id, text=""):
    api_call("answerCallbackQuery", callback_query_id=callback_id, text=text)


def show_menu(chat_id, message_id, menu_name):
    menu = MENUS[menu_name]
    edit_message(chat_id, message_id, menu["text"], menu["buttons"])


def start_quiz(user_id, chat_id, message_id):
    users[user_id] = {"quiz_index": 0, "quiz_score": 0}
    show_quiz_question(user_id, chat_id, message_id)


def show_quiz_question(user_id, chat_id, message_id):
    idx = users[user_id]["quiz_index"]
    q = QUIZ[idx]
    buttons = q["options"] + [("🚪 Выйти в меню", "main")]
    edit_message(chat_id, message_id, q["q"], buttons)


def handle_quiz_answer(user_id, chat_id, message_id, answer):
    state = users.get(user_id)
    if not state:
        return
    idx = state["quiz_index"]
    score = state["quiz_score"]

    if answer == "right":
        score += 1
        state["quiz_score"] = score
        feedback = f"✅ Верно! Правильных ответов: {score}"
    else:
        feedback = f"❌ Неверно. Правильных ответов: {score}"

    idx += 1
    state["quiz_index"] = idx

    if idx >= len(QUIZ):
        if score == len(QUIZ):
            verdict = "🎉 Отличный результат!"
        elif score >= len(QUIZ) * 0.7:
            verdict = "👍 Хороший результат!"
        else:
            verdict = "📚 Стоит повторить теорию."

        text = (
            f"{feedback}\n\n"
            f"🏆 *Тест завершён!*\n"
            f"Твой результат: *{score} из {len(QUIZ)}*\n\n"
            f"{verdict}"
        )
        edit_message(chat_id, message_id, text, [
            ("🔄 Пройти ещё раз", "quiz_start"),
            ("📘 К теории", "theory_menu"),
            ("🏠 В главное меню", "main"),
        ])
        users.pop(user_id, None)
    else:
        edit_message(chat_id, message_id, feedback + "\n\nСледующий вопрос:", [])
        show_quiz_question(user_id, chat_id, message_id)


def handle_callback(user_id, chat_id, message_id, data):
    state = users.get(user_id)
    if state and 0 <= state["quiz_index"] < len(QUIZ):
        options_cb = [cb for _, cb in QUIZ[state["quiz_index"]]["options"]]
        if data in options_cb:
            handle_quiz_answer(user_id, chat_id, message_id, data)
            return
        if data == "main":
            users.pop(user_id, None)

    if data == "quiz_start":
        start_quiz(user_id, chat_id, message_id)
        return

    if data in MENUS:
        if data == "main":
            users.pop(user_id, None)
        show_menu(chat_id, message_id, data)
    else:
        edit_message(chat_id, message_id, "⚠️ Такого раздела нет.")


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}

    if "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        user_id = msg["from"]["id"]
        text = msg.get("text", "")
        if text.startswith("/start"):
            menu = MENUS["main"]
            send_message(chat_id, menu["text"], menu["buttons"])

    elif "callback_query" in data:
        cq = data["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]
        user_id = cq["from"]["id"]
        cb_data = cq["data"]
        answer_callback(cq["id"])
        handle_callback(user_id, chat_id, message_id, cb_data)

    return jsonify(ok=True)


@app.route("/")
def index():
    return "Bot is running", 200


def setup_webhook():
    if not RENDER_URL:
        print("RENDER_EXTERNAL_URL не задан")
        return
    url = f"{RENDER_URL}/webhook"
    r = requests.post(f"{API}/setWebhook", json={"url": url}, timeout=15)
    print("setWebhook:", r.text)


if __name__ == "__main__":
    setup_webhook()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
