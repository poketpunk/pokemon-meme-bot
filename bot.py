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
  print("--- ЗАПУСК ЭЛИТНОГО БОТА С МЕМАМИ POKÉMON ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Золотая коллекция прямых картинок-мемов про Pokémon TCG и коллекционирование
  elite_memes = [
      {
          "title": (
              "When you check your bank account after buying 'just one more'"
              " Pokémon booster box"
          ),
          "image_url": "https://i.imgur.com/716187v.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": "Expectation vs Reality of opening vintage Pokémon packs",
          "image_url": "https://i.imgur.com/2Y32h8t.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "Me protecting my PSA 10 Charizard from literally anything in"
              " the universe"
          ),
          "image_url": "https://i.imgur.com/839015c.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "When someone says 'They're just kids' cards' and you calculate"
              " your portfolio value"
          ),
          "image_url": "https://i.imgur.com/5L2130d.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "That face when you pull a common card that costs less than the"
              " sleeve protecting it"
          ),
          "image_url": "https://i.imgur.com/1943921.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": "Opening packs with friends: pure chaos and broken dreams",
          "image_url": "https://i.imgur.com/9730248.jpg",
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  # Фильтруем то, что уже отправляли
  available_memes = [
      m for m in elite_memes if m["image_url"] not in sent_memes
  ]

  if not available_memes:
    print(
        "ℹ️ Круг замкнулся! Все элитные мемы были опубликованы. Сбрасываем"
        " историю..."
    )
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = elite_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Публикуем шедевр: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Жиза, от которой больно:**",
      "🔥 **Суровая реальность коллекционера карт:**",
      "📦 **Когда надежда умирает последней (вместе с бюджетом):**",
      "🐸 **Классика покемон-сообщества:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{ru_title}**\n\n"
      f"🔗 [Оригинал на Reddit]({link})"
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
    print("✅ УСПЕШНО! Элитный мем улетел в канал.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print("❌ Ошибка отправки мема в Telegram!")


run()
