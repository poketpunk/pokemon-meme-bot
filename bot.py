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
  print("--- ЗАПУСК ЭЛИТНОГО ПОКЕМОН-МЕМ БОТА ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Элитная база прямых изображений-мемов (только чистый юмор про TCG и коллекционеров)
  god_tier_memes = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull 50 common Zubats"
          ),
          "image_url": "https://i.ibb.co/3053736/m1.jpg",  # Заменено на прямой хостинг картинок без заглушек
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "My bank account watching me buy 'just one more' graded Charizard"
          ),
          "image_url": "https://i.ibb.co/6Y0492F/m2.jpg",
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
      {
          "title": (
              "That friend who opens his very first Pokémon pack and gets a"
              " secret rare worth $1000"
          ),
          "image_url": "https://i.ibb.co/7X1983h/m3.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "Me explaining to my family why a piece of shiny cardboard is"
              " an investment portfolio"
          ),
          "image_url": "https://i.ibb.co/2k9150X/m4.jpg",
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
  ]

  # Если все мемы отправлены, сбрасываем историю для бесконечного цикла
  available_memes = [
      m for m in god_tier_memes if m["image_url"] not in sent_memes
  ]
  if not available_memes:
    print("🔄 Все мемы пройдены. Сбрасываем историю...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = god_tier_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Избранный шедевр для публикации: {title}")
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
    print("✅ УСПЕШНО! Мем отправлен в канал в идеальном качестве.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка отправки: {response.text}")


run()
