import os
import random
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")


def run():
  print("--- ЗАПУСК БОТА С ОРИГИНАЛЬНЫМИ МЕМАМИ ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  real_memes = [
      {
          "title": (
              "My brain: You already have 50 Charizards.\nMe buying another"
              " booster box anyway:"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1563089145-599997674d42?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "When you try to explain to your mom why a piece of cardboard"
              " costs more than a used car"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pkmntcgmemes",
      },
      {
          "title": (
              "Me opening a $200 booster box just to pull common cards worth 5"
              " cents"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
      {
          "title": (
              "When someone touches your graded PSA 10 collection without"
              " washing their hands first"
          ),
          "image_url": (
              "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1000&auto=format&fit=crop&q=80"
          ),
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  available_memes = [
      m for m in real_memes if m["image_url"] not in sent_memes
  ]
  if not available_memes:
    print("🔄 Сбрасываем историю отправленных мемов...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = real_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Публикуем мем: {title}")

  intros = [
      "😂 **Pure TCG collector vibes:**",
      "💀 **When reality hits harder than a rare card:**",
      "📦 **Every card collector's pain:**",
      "🔥 **Typical pack opening experience:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{title}**\n\n"
      f"🔗 [Meme Source]({link})"
  )

  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    img_response = requests.get(image_url, headers=headers, timeout=20)
    if img_response.status_code != 200:
      print(f"❌ Ошибка загрузки картинки: {img_response.status_code}")
      return
    image_bytes = img_response.content
  except Exception as e:
    print(f"❌ Ошибка скачивания: {e}")
    return

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
    print("✅ УСПЕШНО! Мем отправлен в канал.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка Telegram: {response.text}")


run()
