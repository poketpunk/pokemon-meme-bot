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
  print("--- ЗАПУСК УЛЬТИМАТИВНОГО БОТА С МЕМАМИ ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Проверенная база прямых ссылок на качественные картинки-мемы
  god_tier_memes = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull 50 common Zubats"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1613771404784-3a5686aa2be3?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "My bank account watching me buy 'just one more' graded Charizard"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
      {
          "title": (
              "That friend who opens his very first Pokémon pack and gets a"
              " secret rare worth $1000"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  available_memes = [
      m for m in god_tier_memes if m["image_url"] not in sent_memes
  ]
  if not available_memes:
    print("🔄 Сбрасываем историю отправленных мемов...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = god_tier_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Скачиваем и публикуем шедевр: {title}")
  ru_title = translate_text(title)

  # Скачиваем картинку локально в память скрипта, чтобы обойти блокировки хостингов
  try:
    img_response = requests.get(image_url, timeout=15)
    if img_response.status_code != 200:
      print(f"❌ Не удалось скачать картинку по ссылке: {image_url}")
      return
    image_bytes = img_response.content
  except Exception as e:
    print(f"❌ Ошибка скачивания картинки: {e}")
    return

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

  # Отправляем файл напрямую в Telegram API через multipart/form-data
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
    print("✅ УСПЕШНО! Мем отправлен в канал в идеальном качестве.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка отправки в Telegram: {response.text}")


run()
