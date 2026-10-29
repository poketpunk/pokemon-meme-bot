import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")


def translate_text(text):
  if not text:
    return ""
  try:
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": "ru",
        "dt": "t",
        "q": text[:4000],
    }
    response = requests.get(url, params=params, timeout=10)
    if response.status_code == 200:
      data = response.json()
      return "".join([item[0] for item in data[0] if item[0]])
  except Exception as e:
    print(f"Ошибка перевода: {e}")
  return text


def run():
  print("--- ЗАПУСК БОТА С МЕМАМИ POKÉMON ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Проверенная база с прямыми ссылками на картинки-мемы, которые отлично рендерятся в Telegram
  meme_database = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon cards and get"
              " all common duplicates"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "Me explaining to my friends why this piece of cardboard is"
              " worth $5,000"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1613771404784-3a5686aa2be3?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "That one friend who pulls a secret rare Charizard on his very"
              " first booster pack"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  available_memes = [
      m for m in meme_database if m["image_url"] not in sent_memes
  ]

  if not available_memes:
    print("ℹ️ История пуста или сброшена, обновляем пул...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = meme_database

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"✅ Публикуем мем: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Настроение коллекционера:**",
      "🐸 **Жизненная ситуация в сообществе покемонов:**",
      "🔥 **Когда реальность бьет сильнее, чем редкая карта:**",
      "📦 **Будни охотника за редкими сетами:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{ru_title}**\n\n"
      f"🔗 [Источник]({link})"
  )

  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "photo": image_url,
      "caption": caption,
      "parse_mode": "Markdown",
  }

  response = requests.post(url, json=payload)
  print(f"Ответ Telegram API: {response.status_code}")

  if response.status_code == 200:
    print("✅ УСПЕШНО! Мем опубликован в канале.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print("❌ Ошибка отправки мема в Telegram!")


run()
