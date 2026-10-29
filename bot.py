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

  # Надежные прямые ссылки на картинки с Викисклада (Wikimedia Commons), которые никогда не блокируют запросы
  memes_database = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull only common cards"
          ),
          "image_url": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9mon_Trading_Card_Game_logo.svg/800px-Pok%C3%A9mon_Trading_Card_Game_logo.svg.png"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": "My wallet crying after looking at the new Pokémon TCG prices",
          "image_url": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pokémon_logo.svg/800px-International_Pokémon_logo.svg.png"
          ),
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
      {
          "title": (
              "That friend who opens his very first pack and gets a secret"
              " rare"
          ),
          "image_url": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Pokeball.svg/800px-Pokeball.svg.png"
          ),
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

  # Скачиваем картинку с правильными заголовками
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    img_response = requests.get(image_url, headers=headers, timeout=15)
    if img_response.status_code != 200:
      print(
          f"❌ Ошибка загрузки картинки, код ответа: {img_response.status_code}"
      )
      return
    image_bytes = img_response.content
  except Exception as e:
    print(f"❌ Ошибка скачивания: {e}")
    return

  # Отправляем в Telegram
  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
  payload = {
      "chat_id": TELEGRAM_CHAT_ID,
      "caption": caption,
      "parse_mode": "Markdown",
  }
  files = {"photo": ("meme.png", image_bytes, "image/png")}

  response = requests.post(url, data=payload, files=files)
  print(f"Ответ Telegram API: {response.status_code}")

  if response.status_code == 200:
    print("✅ УСПЕШНО! Картинка успешно отправлена в канал.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка Telegram: {response.text}")


run()
