import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Используем ключ DeepSeek


def generate_ai_joke():
  if not DEEPSEEK_API_KEY:
    print("❌ ОШИБКА: Переменная DEEPSEEK_API_KEY не задана!")
    return None

  url = "https://api.deepseek.com/chat/completions"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
  }

  payload = {
      "model": "deepseek-chat",  # Стабильная модель DeepSeek-V3
      "messages": [{
          "role": "user",
          "content": (
              "Напиши короткую, очень смешную и жизненную шутку (на русском языке,"
              " 2-3 строчки) про боль коллекционеров карточек Pokémon TCG, открытие"
              " бустеров или слив денег на картон. Без лишних вводных фраз."
          ),
      }],
      "stream": False,
  }

  try:
    print("Отправка запроса в DeepSeek API...")
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Ответ от DeepSeek API: {response.status_code}")

    if response.status_code == 200:
      data = response.json()
      joke = data["choices"][0]["message"]["content"].strip()
      return joke
    else:
      print(f"❌ Ошибка ответа DeepSeek: {response.text}")
  except Exception as e:
    print(f"❌ Исключение при запросе к DeepSeek: {e}")

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
        "❌ КРИТИЧЕСКАЯ ОШИБКА: DeepSeek недоступен. Публикация отменена без"
        " заглушек."
    )
    return

  print(f"✅ Успешно сгенерировано через DeepSeek:\n{joke_text}")

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
