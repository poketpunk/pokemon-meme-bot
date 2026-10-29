import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_joke():
  """Генерирует уникальную жизовую шутку про Pokémon TCG на русском языке"""
  if not GEMINI_API_KEY:
    print(
        "⚠️ GEMINI_API_KEY не найден, используем резервную шутку из базы."
    )
    fallback_jokes = [
        (
            "Мой мозг: 'Давай отложим деньги на квартплату.'\nМое сердце:"
            " 'А вдруг в следующем бустере секретный Чаризард?'\nКошелек:"
            " *плачет в углу*"
        ),
        (
            "Когда пытаешься объяснить маме, почему этот кусочек картона стоит"
            " дороже подержанной иномарки."
        ),
        (
            "4 стадии коллекционера TCG: Надежда, Боль от комонок, Открытие"
            " еще одного бустера, Повторить."
        ),
    ]
    return random.choice(fallback_jokes)

  prompt = (
      "Напиши короткую, очень смешную и жизненную шутку или мем-текст"
      " (на русском языке, 2-4 строчки) про боль коллекционеров карточек"
      " Pokémon TCG, открытие бустеров, слив всех денег на картон или"
      " охоту за редкими картами. Шутка должна быть понятна русскоязычным"
      " коллекционерам. Без лишних вводных фраз, только текст шутки."
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
    else:
      print(f"❌ Ошибка API ИИ: {response.status_code} - {response.text}")
  except Exception as e:
    print(f"❌ Ошибка соединения с ИИ: {e}")

  return (
      "Когда потратил всю зарплату на коллекционный бокс, а там снова одни"
      " обычные покемоны."
  )


def run():
  print("--- ЗАПУСК АВТОНОМНОГО КАНАЛ-БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  joke_text = generate_ai_joke()
  print(f"🔥 Сгенерирована шутка:\n{joke_text}")

  intros = [
      "😂 **Чистая жиза из жизни коллекционеров:**",
      "💀 **Когда реальность бьет сильнее, чем редкая карта:**",
      "📦 **Будни охотника за редкими сетами TCG:**",
      "🔥 **Классика любого бандла:**",
  ]

  message = (
      f"{random.choice(intros)}\n\n"
      f"📌 {joke_text}\n\n"
      f"💬 *А какая карта снится вам? Делитесь в комментариях!*"
  )

  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "text": message,
      "parse_mode": "Markdown",
  }

  response = requests.post(url, json=payload)
  print(f"Ответ Telegram API: {response.status_code}")

  if response.status_code == 200:
    print("✅ УСПЕШНО! Пост опубликован в канале.")
  else:
    print(f"❌ Ошибка Telegram: {response
