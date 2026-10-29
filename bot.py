import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_ai_joke():
  """Генерирует уникальную шутку про Pokémon TCG с помощью Gemini API"""
  if not GEMINI_API_KEY:
    print(
        "⚠️ GEMINI_API_KEY не найден, используем резервную элитную шутку из"
        " базы."
    )
    fallback_jokes = [
        (
            "My brain: 'Save money for rent.'\nMy heart: 'What if the next"
            " booster pack has a secret rare Charizard?'\nWallet: *cries in"
            " bankruptcy*"
        ),
        (
            "When someone handles your PSA 10 graded card without gloves and"
            " you have to consider legal action."
        ),
        (
            "The 4 stages of TCG collecting: Hope, Regret, Opening another"
            " booster box, Repeat."
        ),
    ]
    return random.choice(fallback_jokes)

  prompt = (
      "Write a short, hilarious, and relatable English meme text (2-4 lines)"
      " about the pain and obsession of collecting Pokémon TCG cards, opening"
      " booster packs, spending all money on cardboard, or dealing with rare"
      " cards. Keep it authentic to Reddit meme culture. Do not include"
      " introductory filler text, just give the joke itself."
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
      "When you spend your last money on a booster box and pull 50 common"
      " Zubats."
  )


def run():
  print("--- ЗАПУСК ИИ-БОТА С БЕСКОНЕЧНЫМИ МЕМАМИ ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  # Генерируем уникальную шутку на лету
  joke_text = generate_ai_joke()
  print(f"🔥 Сгенерирована свежая шутка:\n{joke_text}")

  intros = [
      "😂 **AI-generated TCG pain:**",
      "💀 **Fresh from the neural network collector brain:**",
      "📦 **Today's wisdom for Pokémon card addicts:**",
      "🔥 **Generated pure unfiltered collector reality:**",
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
    print("✅ УСПЕШНО! Уникальный сгенерированный мем опубликован в канале.")
  else:
    print(f"❌ Ошибка Telegram: {response.text}")


run()
