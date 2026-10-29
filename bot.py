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
  print("--- ЗАПУСК ИДЕАЛЬНОГО МЕМ-БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Точная база проверенных мемов и жизненных ситуаций TCG с качественными картинками
  memes_database = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull only common cards"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1000&auto=format&fit=crop&q=80"
          ),  # Игровой/коллекционный вайб
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": "My wallet crying after looking at the new Pokémon TCG prices",
          "image_url": (
              "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=1000&auto=format&fit=crop&q=80"
          ),  # Атмосфера гейминга/коллекционирования
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
      {
          "title": (
              "That friend who opens his very first pack and gets a secret"
              " rare"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1612287233202-b51b366167ef?w=1000&auto=format&fit=crop&q=80"
          ),  # Эмоции от игры/карт
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  available_memes = [
      m for m in memes_database if m["image_url"] not in sent_memes
  ]
  if not available_memes:
    print("🔄 Сбрасываем историю отправленных мемов...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = memes_database

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Публикуем мем: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Чистая жиза из жизни коллекционеров:**",
      "🔥 **Когда реальность бьет сильнее, чем редкая карта:**",
      "📦 **Будни охотника за редкими сетами Pokémon TCG:**",
      "🐸 **Классика сообщества покемонов:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{ru_title}**\n\n"
      f"🔗 [Сообщество мемов]({link})"
  )

  # Скачиваем картинку
  try:
    img_response = requests.get(image_url, timeout=15)
    if img_response.status_code != 200:
      print(f"❌ Ошибка загрузки картинки")
      return
    image_bytes = img_response.content
  except Exception as e:
    print(f"❌ Ошибка: {e}")
    return

  # Отправляем в Telegram
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "caption": caption,
      "parse_mode": "Markdown",
  }
  files = {"photo": ("meme.jpg", image_bytes, "image/jpeg")}

  response = requests.post(url, data=payload, files=files)
  print(f"Ответ Telegram API: {response.status_code}")

  if response.status_code == 200:
    print("✅ УСПЕШНО! Мем отправлен.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка: {response.text}")


run()
