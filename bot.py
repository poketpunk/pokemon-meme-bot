import os
import random
from google import genai
from google.genai import errors
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_joke():
  if not GEMINI_API_KEY:
    print("❌ ОШИБКА: Переменная GEMINI_API_KEY не задана!")
    return None

  # Инициализируем официальный клиент Google GenAI
  client = genai.Client(api_key=GEMINI_API_KEY)

  prompt = (
      "Напиши короткую, очень смешную и жизненную шутку (на русском языке,"
      " 2-3 строчки) про боль коллекционеров карточек Pokémon TCG, открытие"
      " бустеров или слив денег на картон. Без лишних вводных фраз."
  )

  # Пробуем получить ответ через официальный клиент (он сам выбирает актуальную модель)
  models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash"]

  for model_name in models_to_try:
    try:
      print(f"Попытка генерации через модель: {model_name}")
      response = client.models.generate_content(
          model=model_name,
          contents=prompt,
      )
      if response and response.text:
        return response.text.strip()
    except Exception as e:
      print(f"❌ Ошибка с моделью {model_name}: {e}")
      continue

  return None


def run():
  print("--- ЗАПУСК БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Ошибка: Не заданы секреты Telegram!")
    return

  joke_text = generate_ai_joke()

  # Если ИИ не ответил, честно отменяем публикацию без заглушек
  if not joke_text:
    print(
        "❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось получить шутку от ИИ. Публикация"
        " отменена."
    )
    return

  print(f"✅ Успешно сгенерировано:\n{joke_text}")

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
