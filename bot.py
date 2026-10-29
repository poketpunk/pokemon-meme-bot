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
  # Обязательно указываем User-Agent, чтобы Reddit не блокировал запросы
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Bot/1.0"
          " (PokemonMemeBot)"
      )
  }
  # Берем горячие посты из сабреддита с мемами по покемонам
  url = "https://www.reddit.com/r/pokemonmemes/hot.json?limit=25"

  try:
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
      print(f"Ошибка доступа к Reddit: {response.status_code}")
      return None

    data = response.json()
    posts = data.get("data", {}).get("children", [])

    # Перемешиваем посты, чтобы каждый раз был разный выбор
    random.shuffle(posts)

    for post in posts:
      p_data = post.get("data", {})
      title = p_data.get("title", "")
      image_url = p_data.get("url", "")
      permalink = p_data.get("permalink", "")
      is_video = p_data.get("is_video", False)

      # Проверяем, что это прямая картинка (а не видео, текст или ссылка на сторонний сайт)
      if not is_video and any(
          image_url.lower().endswith(ext) for ext in [".jpg", ".png", ".jpeg"]
      ):
        source_link = f"https://reddit.com{permalink}"
        return {"title": title, "image_url": image_url, "link": source_link}

  except Exception as e:
    print(f"Ошибка при парсинге Reddit: {e}")

  return None


def run():
  print("--- ЗАПУСК БОТА С МЕМАМИ POKÉMON (REDDIT) ---")
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: Не заданы секреты TG_TOKEN или TG_CHAT!")
    return

  sent_memes = set()
  if os.path.exists("sent_memes.txt"):
    with open("sent_memes.txt", "r", encoding="utf-8") as f:
      sent_memes = set(line.strip() for line in f if line.strip())

  meme_data = fetch_meme_from_reddit()
  if not meme_data:
    print("ℹ️ Не удалось найти подходящий мем на Reddit.")
    return

  if meme_data["link"] in sent_memes:
    print("ℹ️ Этот мем уже публиковался ранее.")
    return

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"✅ Найден мем: {title}")
  print(f"Картинка: {image_url}")

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
      f"🔗 [Источник на Reddit]({link})"
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
      f.write(meme_data["link"] + "\n")
  else:
    print("❌ Ошибка отправки мема в Telegram!")


run()
