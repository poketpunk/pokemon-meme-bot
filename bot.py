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


def fetch_meme_from_reddit():
  # Используем более реалистичный User-Agent браузера Chrome, чтобы обходить 403 ошибку
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept": (
          "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
      ),
      "Accept-Language": "en-US,en;q=0.5",
  }

  url = "https://www.reddit.com/r/pokemonmemes/hot.json?limit=30"

  try:
    response = requests.get(url, headers=headers, timeout=15)
    print(f"Статус ответа от Reddit: {response.status_code}")

    if response.status_code != 200:
      print(
          "⚠️ Reddit защищается от запросов с сервера. Пробую запасной"
          " вариант..."
      )
      return None

    data = response.json()
    posts = data.get("data", {}).get("children", [])
    random.shuffle(posts)

    for post in posts:
      p_data = post.get("data", {})
      title = p_data.get("title", "")
      image_url = p_data.get("url", "")
      permalink = p_data.get("permalink", "")
      is_video = p_data.get("is_video", False)

      if not is_video and any(
          image_url.lower().endswith(ext) for ext in [".jpg", ".png", ".jpeg"]
      ):
        source_link = f"https://reddit.com{permalink}"
        return {"title": title, "image_url": image_url, "link": source_link}

  except Exception as e:
    print(f"Ошибка при запросе к Reddit: {e}")

  return None


def run():
  print("--- ЗАПУСК БОТА С МЕМАМИ POKÉMON ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  meme_data = fetch_meme_from_reddit()

  # Если Reddit заблокировал прямое скачивание с GitHub Actions, используем резервную выдачу мемов
  if not meme_data:
    print("ℹ️ Используем резервную базу мемов...")
    backup_memes = [
        {
            "title": (
                "When you pull a common card instead of Charizard after"
                " spending all your money"
            ),
            "image_url": (
                "https://images.unsplash.com/photo-1613771404784-3a5686aa2be3?w=800"
            ),
            "link": "https://reddit.com/r/pokemonmemes",
        },
        {
            "title": (
                "My wallet crying after looking at the new Pokémon TCG set"
                " prices"
            ),
            "image_url": (
                "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800"
            ),
            "link": "https://reddit.com/r/pokemonmemes",
        },
    ]
    # Выбираем случайный резервный мем, которого еще не было
    available_backups = [
        m for m in backup_memes if m["image_url"] not in sent_memes
    ]
    if available_backups:
      meme_data = random.choice(available_backups)

  if not meme_data:
    print("ℹ️ Не удалось найти новый мем.")
    return

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"✅ Публикуем мем: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Пятничное (или не очень) настроение с покемонами!**",
      "🐸 **МЕМУАРЫ ТРЕНЕРА:**",
      "🔥 **Жизненно о коллекционировании и покемонах:**",
      "📦 **Когда открыл очередной бустер в надежде на чаризарда:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 {ru_title}\n\n"
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
      f.write(image_url + "\n")
  else:
    print("❌ Ошибка отправки мема в Telegram!")


run()
