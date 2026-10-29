import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_joke():
  if not GEMINI_API_KEY:
    return (
        "Мой мозг: 'Давай отложим деньги.'\nМое сердце: 'А вдруг в бустере"
        " секретный Чаризард?'\nКошелек: *плачет*"
    )

  prompt = (
      "Напиши короткую, очень смешную и жизненную шутку (на русском языке,"
      " 2-3 строчки) про боль коллекционеров карточек Pokémon TCG, открытие"
      " бустеров или слив денег на картон. Без лишних вводных фраз."
  )

  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
  headers = {"Content-Type": "application/json"}
  payload = {"contents": [{"parts": [{"text": prompt}]}]}

  try:
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    if response.status_code == 200:
      data = response.json()
      joke = data["candidates"][0]["content"]["parts"][0]["text"].strip()
      return joke
  except Exception as e:
    print(f"Ошибка ИИ: {e}")

  return "Когда потратил всю зарплату на бокс, а там снова одни комонки."


def run():
  print("--- ЗАПУСК БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Ошибка: Не заданы секреты!")
    return

  joke_text = generate_ai_joke()
  print(f"Шутка: {joke_text}")

  intros = [
      "😂 **Чистая жиза из жизни коллекционеров:**",
      "💀 **Когда реальность бьет сильнее, чем редкая карта:**",
      "📦 **Будни охотника за редкими сетами TCG:**",
  ]

  message = f"{random.choice(intros)}\n\n📌 {joke_text}"

  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "Markdown",
  }

  response = requests.post(url, json=payload)
  print(f"Ответ Telegram: {response.status_code}")

  if response.status_code == 200:
    print("Успешно отправлено!")
  else:
    print("Ошибка отправки в Telegram")


run()
