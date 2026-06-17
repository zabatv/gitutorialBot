import requests
import time
import json

# ==================== НАСТРОЙКИ ====================
TOKEN = "8385354039:AAF6rgn5uLg-oXYTHJCYkoz2XIg5xa5HYPQ"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Состояние пользователей (для теста)
user_states = {}

# ==================== МЕНЮ БОТА (Git) ====================
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

    # ===== ТЕОРИЯ =====
    "theory_menu": {
        "text": "📘 *Теория Git*\n\nВыбери тему для изучения:",
        "buttons": [
            ("1️⃣ Что такое Git", "th_what"),
            ("2️⃣ Концепции", "th_concepts"),
            ("3️⃣ Рабочий процесс", "th_workflow"),
            ("4️⃣ Ветвление", "th_branch"),
            ("5️⃣ Удалённые репозитории", "th_remote"),
            ("6️⃣ Конфликты", "th_conflict"),
            ("⬅️ Назад", "main"),
        ]
    },
    "th_what": {
        "text": "📘 *Что такое Git?*\n\n"
                "Git — распределённая система контроля версий, "
                "созданная Линусом Торвальдсом в 2005 году.\n\n"
                "Зачем нужен:\n"
                "• Хранить историю изменений\n"
                "• Откатываться к любой версии\n"
                "• Работать параллельно над проектом\n"
                "• Синхронизировать код через GitHub/GitLab",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },
    "th_concepts": {
        "text": "📘 *Основные концепции*\n\n"
                "🔸 Репозиторий — папка проекта с историей (.git)\n"
                "🔸 Коммит — снимок состояния файлов\n"
                "🔸 Ветка — указатель на коммит\n"
                "🔸 HEAD — текущая ветка/коммит\n"
                "🔸 Индекс — зона перед коммитом",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },
    "th_workflow": {
        "text": "📘 *Рабочий процесс*\n\n"
                "Файл проходит 3 состояния:\n"
                "1️⃣ Working Directory (рабочая папка)\n"
                "2️⃣ Staging Area (индекс)\n"
                "3️⃣ Repository (.git)\n\n"
                "Цикл: изменил → git add → git commit → повторить",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },
    "th_branch": {
        "text": "📘 *Ветвление и слияние*\n\n"
                "Ветки: main, feature/*, bugfix/*\n\n"
                "Слияние (merge):\n"
                "• Fast-forward — если не было новых коммитов\n"
                "• Three-way merge — если были изменения в обеих ветках\n\n"
                "Стратегии: Git Flow, GitHub Flow",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },
    "th_remote": {
        "text": "📘 *Удалённые репозитории*\n\n"
                "🔸 git clone — клонировать\n"
                "🔸 git push — отправить на сервер\n"
                "🔸 git pull — получить + слить\n"
                "🔸 git fetch — только получить\n\n"
                "По умолчанию remote называется origin",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },
    "th_conflict": {
        "text": "📘 *Разрешение конфликтов*\n\n"
                "<<<<<<< HEAD\n"
                "мой код\n"
                "=======\n"
                "чужой код\n"
                ">>>>>>> branch\n\n"
                "Что делать:\n"
                "1. Открыть файл\n"
                "2. Выбрать версию\n"
                "3. git add → git commit",
        "buttons": [("⬅️ К темам", "theory_menu")]
    },

    # ===== КОМАНДЫ =====
    "commands": {
        "text": "🛠 Выбери команду Git:",
        "buttons": [
            ("git init", "cmd_init"),
            ("git add", "cmd_add"),
            ("git commit", "cmd_commit"),
            ("git branch", "cmd_branch"),
            ("git merge", "cmd_merge"),
            ("git push", "cmd_push"),
            ("⬅️ Назад", "main"),
        ]
    },
    "cmd_init": {"text": "🔹 git init\n\nСоздаёт новый репозиторий в текущей папке.", "buttons": [("⬅️ К командам", "commands")]},
    "cmd_add": {"text": "🔹 git add .\n\nДобавляет все изменения в индекс.", "buttons": [("⬅️ К командам", "commands")]},
    "cmd_commit": {"text": "🔹 git commit -m \"msg\"\n\nСохраняет изменения в историю.", "buttons": [("⬅️ К командам", "commands")]},
    "cmd_branch": {"text": "🔹 git branch name\n\nСоздаёт новую ветку.", "buttons": [("⬅️ К командам", "commands")]},
    "cmd_merge": {"text": "🔹 git merge name\n\nСливает ветку в текущую.", "buttons": [("⬅️ К командам", "commands")]},
    "cmd_push": {"text": "🔹 git push origin main\n\nОтправляет коммиты на сервер.", "buttons": [("⬅️ К командам", "commands")]},

    # ===== ЗАВЕРШЕНИЕ =====
    "finish": {
        "text": "🏁 *Обучение завершено!*\n\n"
                "Ты изучил:\n"
                "✔ Теорию Git\n"
                "✔ Основные команды\n"
                "✔ Прошёл тест\n\n"
                "Удачи в проектах! 🚀",
        "buttons": [("🔄 Начать заново", "main")],
    },
}

# ==================== ТЕСТ ====================
QUIZ = [
    {"q": "❓ 1/7. Какая команда создаёт репозиторий?",
     "options": [("git start","wrong"),("git init","right"),("git new","wrong"),("git create","wrong")]},
    {"q": "❓ 2/7. Что добавляет файлы в индекс?",
     "options": [("git add","right"),("git stage","wrong"),("git commit","wrong"),("git push","wrong")]},
    {"q": "❓ 3/7. Что делает git commit -m?",
     "options": [("Отправляет на сервер","wrong"),("Сохраняет в историю","right"),("Создаёт ветку","wrong"),("Удаляет файл","wrong")]},
    {"q": "❓ 4/7. Как создать ветку?",
     "options": [("git branch name","right"),("git new name","wrong"),("git create name","wrong"),("git fork name","wrong")]},
    {"q": "❓ 5/7. Что делает git clone?",
     "options": [("Удаляет репо","wrong"),("Копирует удалённое репо","right"),("Создаёт ветку","wrong"),("Отправляет коммиты","wrong")]},
    {"q": "❓ 6/7. Что делает git pull?",
     "options": [("Только скачивает","wrong"),("Отправляет на сервер","wrong"),("Получает + сливает","right"),("Создаёт ветку","wrong")]},
    {"q": "❓ 7/7. Как выглядит метка конфликта?",
     "options": [("<<<<<<< HEAD ... ======= ... >>>>>>>","right"),("### CONFLICT ###","wrong"),("!!! ERROR !!!","wrong"),("[CONFLICT]","wrong")]},
]

# ==================== TELEGRAM API ====================

def send_message(chat_id, text, buttons=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if buttons:
        keyboard = {"inline_keyboard": [[{"text": t, "callback_data": c}] for t, c in buttons]}
        payload["reply_markup"] = json.dumps(keyboard)
    r = requests.post(f"{API_URL}/sendMessage", data=payload, timeout=30)
    return r.json()


def edit_message(chat_id, message_id, text, buttons=None):
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if buttons:
        keyboard = {"inline_keyboard": [[{"text": t, "callback_data": c}] for t, c in buttons]}
        payload["reply_markup"] = json.dumps(keyboard)
    r = requests.post(f"{API_URL}/editMessageText", data=payload, timeout=30)
    return r.json()


def answer_callback(query_id, text=""):
    payload = {"callback_query_id": query_id, "text": text}
    requests.post(f"{API_URL}/answerCallbackQuery", data=payload, timeout=30)


def get_updates(offset=None):
    payload = {"timeout": 30}
    if offset is not None:
        payload["offset"] = offset
    try:
        r = requests.get(f"{API_URL}/getUpdates", params=payload, timeout=40)
        return r.json()
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return {"ok": False, "result": []}


# ==================== ЛОГИКА ====================

def show_menu(chat_id, message_id, menu_name, is_callback=False):
    if menu_name not in MENUS:
        if is_callback:
            edit_message(chat_id, message_id, "⚠️ Такого раздела нет.")
        else:
            send_message(chat_id, "⚠️ Такого раздела нет.")
        return

    menu = MENUS[menu_name]
    if is_callback:
        edit_message(chat_id, message_id, menu["text"], menu["buttons"])
    else:
        send_message(chat_id, menu["text"], menu["buttons"])


def start_quiz(chat_id, message_id):
    """Запуск теста."""
    user_states[chat_id] = {"quiz_index": 0, "quiz_score": 0, "in_quiz": True}
    show_quiz_question(chat_id, message_id, is_callback=True)


def show_quiz_question(chat_id, message_id, is_callback=True):
    state = user_states.get(chat_id)
    if not state:
        return
    idx = state["quiz_index"]
    q = QUIZ[idx]
    buttons = q["options"] + [("🚪 Выйти в меню", "quiz_exit")]
    if is_callback:
        edit_message(chat_id, message_id, q["q"], buttons)
    else:
        send_message(chat_id, q["q"], buttons)


def handle_quiz_answer(chat_id, message_id, answer):
    state = user_states[chat_id]
    idx = state["quiz_index"]
    score = state["quiz_score"]

    if answer == "right":
        score += 1
        state["quiz_score"] = score
        feedback = f"✅ Верно! ({score}/{len(QUIZ)})"
    else:
        feedback = f"❌ Неверно. ({score}/{len(QUIZ)})"

    idx += 1
    state["quiz_index"] = idx

    if idx >= len(QUIZ):
        # Тест завершён
        if score == len(QUIZ):
            msg = "🎉 Отличный результат!"
        elif score >= 5:
            msg = "👍 Хороший результат!"
        else:
            msg = "📚 Стоит повторить теорию."

        edit_message(chat_id, message_id,
                     f"{feedback}\n\n🏆 *Итог: {score}/{len(QUIZ)}*\n\n{msg}",
                     [("🔄 Пройти ещё раз", "quiz_start"),
                      ("🏠 В главное меню", "main")])
        # Сбрасываем состояние
        user_states.pop(chat_id, None)
    else:
        # Следующий вопрос
        edit_message(chat_id, message_id, feedback)
        show_quiz_question(chat_id, message_id, is_callback=False)


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        # Сбрасываем состояние при /start
        user_states.pop(chat_id, None)
        show_menu(chat_id, None, "main", is_callback=False)
    else:
        send_message(chat_id, "Нажми /start, чтобы открыть меню.")


def handle_callback(callback_query):
    query_id = callback_query["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]
    button_id = callback_query["data"]

    answer_callback(query_id)

    state = user_states.get(chat_id)

    # --- Выход из теста ---
    if button_id == "quiz_exit":
        user_states.pop(chat_id, None)
        show_menu(chat_id, message_id, "main", is_callback=True)
        return

    # --- Запуск теста ---
    if button_id == "quiz_start":
        start_quiz(chat_id, message_id)
        return

    # --- Ответ на вопрос теста ---
    if state and state.get("in_quiz"):
        idx = state["quiz_index"]
        if 0 <= idx < len(QUIZ):
            options_cb = [c for _, c in QUIZ[idx]["options"]]
            if button_id in options_cb:
                handle_quiz_answer(chat_id, message_id, button_id)
                return

    # --- Обычные меню ---
    if button_id in MENUS:
        show_menu(chat_id, message_id, button_id, is_callback=True)
    else:
        edit_message(chat_id, message_id, "⚠️ Такого раздела нет.")


# ==================== ГЛАВНЫЙ ЦИКЛ ====================

def main():
    print("🤖 Бот про Git запущен (requests)...")
    offset = None

    while True:
        try:
            updates = get_updates(offset)
            if not updates.get("ok"):
                time.sleep(3)
                continue

            for update in updates.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])
                elif "callback_query" in update:
                    handle_callback(update["callback_query"])

        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен.")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(3)


if __name__ == "__main__":
    main()
