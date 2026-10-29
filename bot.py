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
  print("--- ЗАПУСК ИДЕАЛЬНОГО БОТА С МЕМАМИ ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  # Проверенные прямые картинки-мемы и атмосферные арты TCG с прямым расширением файлов (.jpg/.png)
  clean_memes = [
      {
          "title": (
              "When you spend your last money on booster packs and get zero"
              " ultra rares"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1613771404784-3a5686aa2be3?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://t.me/pokemon",
      },
      {
          "title": (
              "The face you make when someone handles your mint condition"
              " Charizard without gloves"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://t.me/pokemon",
      },
      {
          "title": "Collector's internal pain when looking at graded card prices",
          "image_url": (
              "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1200&auto=format&fit=crop&q=80"
          ),
          "link": "https://t.me/pokemon",
      },
  ]

  available_memes = [
      m for m in clean_memes if m["image_url"] not in sent_memes
  ]

  if not available_memes:
    print("ℹ️ Сбрасываем историю отправленных мемов...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = clean_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Публикуем: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Жиза, от которой больно:**",
      "🔥 **Суровая реальность коллекционера карт:**",
      "📦 **Когда надежда умирает последней:**",
      "🐸 **Классика сообщества:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{ru_title}**\n\n"
      f"🔗 [Сообщество TCG]({link})"
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
    print("✅ УСПЕШНО! Мем отправлен без логотипов.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print("❌ Ошибка отправки мема в Telegram!")


run()
