import os
import random
import urllib.parse
from bs4 import BeautifulSoup
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TG_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TG_CHAT")

# Поисковые запросы для поиска свежих мемов и комиксов по покемонам
MEME_QUERIES = [
    'funny pokemon memes reddit',
    'best pokemon tcg memes',
    'pokemon card collector meme',
]


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


def fetch_meme_from_web():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  query = random.choice(MEME_QUERIES)
  encoded_query = urllib.parse.quote(query)
  rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

  try:
    response = requests.get(rss_url, headers=headers, timeout=15)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "xml")
      items = soup.find_all("item")

      for item in items[:5]:
        title = item.title.text if item.title else ""
        link = item.link.text if item.link else ""
        if title and link:
          # Переходим по ссылке статьи, чтобы найти картинку-мем
          art_resp = requests.get(link, headers=headers, timeout=10)
          if art_resp.status_code == 200:
            art_soup = BeautifulSoup(art_resp.text, "html.parser")
            imgs = art_soup.find_all("img")
            for img in imgs:
              src = img.get("src", "")
              # Ищем подходящую картинку (не иконку сайта)
              if src.startswith("http") and any(
                  ext in src.lower() for ext in [".jpg", ".png", ".jpeg"]
              ):
                if (
                    "avatar" not in src
                    and "logo" not in src
                    and "icon" not in src
                ):
                  return {"title": title, "link": link, "image_url": src}
  except Exception as e:
    print(f"Ошибка поиска мема: {e}")

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

  meme_data = fetch_meme_from_web()
  if not meme_data:
    print("ℹ️ Не удалось найти подходящий мем в этот раз.")
    return

  if meme_data["link"] in sent_memes:
    print("ℹ️ Этот мем уже публиковался ранее.")
    return

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"Найден мем: {title}")
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

  # Публикация картинки с мемом в Telegram
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
