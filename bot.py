import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_joke():
  if not GEMINI_API_KEY:
    print("❌ ОШИБКА: Переменная GEMINI_API_KEY пуста или не передана в Python!")
    return None

  prompt = (
      "Напиши короткую, очень смешную и жизненную шутку (на русском языке,"
      " 2-3 строчки) про боль коллекционеров карточек Pokémon TCG, открытие"
      " бустеров или слив денег на картон. Без лишних вводных фраз."
  )

  # Используем актуальную модель Gemini 3.8 Flash
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
  headers = {"Content-Type": "application/json"}
  payload = {"contents": [{"parts": [{"text": prompt}]}]}

  try:
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    print(f"Ответ от Gemini API: {response.status_code}")

    if response.status_code == 200:
      data = response.json()
      joke = data["candidates"][0]["content"]["parts"][0]["text"].strip()
      return joke
    else:
      print(f"❌ Ошибка ответа Gemini: {response.text}")
  except Exception as e:
    print(f"❌ Исключение при запросе к ИИ: {e}")

  return None


def run():
  print("--- ЗАПУСК БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Ошибка: Не заданы секреты Telegram!")
    return

  joke_text = generate_ai_joke()

  if not joke_text:
    print("⚠️ Сработал резервный вариант (ИИ недоступен).")
    joke_text = "Когда потратил всю зарплату на бокс, а там снова одни комонки."
  else:
    print("✅ Успешно сгенерировано через Gemini 3.8 Flash!")

  print(f"Итоговая шутка: {joke_text}")

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
    print("Успешно отправлено в канал!")
  else:
    print(f"Ошибка отправки в Telegram: {response.text}")


run()
