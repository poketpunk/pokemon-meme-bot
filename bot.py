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

  # Используем прямые ссылки на картинки с GitHub-репозиториев (Raw), которые отдают файлы мгновенно без блокировок
  memes_database = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull only common cards"
          ),
          "image_url": (
              "https://raw.githubusercontent.com/octocat/Spoon-Knife/main/index.html"
          ),  # Заменим на стабильный URL ниже
          "link": "https://reddit.com/r/pokemonmemes",
      },
  ]

  # Переведем на стопроцентно стабильные прямые картинки-постеры карточек
  reliable_memes = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull only common cards"
          ),
          "image_url": (
              "https://images.dog.ceo/breeds/hound-english/n02089973_1.jpg"
          ),  # Тестовая стабильная картинка, заменим на тематику
          "link": "https://reddit.com/r/pokemonmemes",
      }
  ]

  # Давай сделаем еще проще и надежнее: используем прямые картинки из репозитория Pokémon TCG API (открытые CDN)
  final_memes = [
      {
          "title": (
              "When you spend your entire paycheck on Pokémon booster packs and"
              " pull only common cards"
          ),
          "image_url": (
              "https://images.pokemontcg.io/base1/4_hires.png"
          ),  # Официальная карточка Charizard (хитрейший и самый желанный мем!)
          "link": "https://images.pokemontcg.io/base1/4.png",
      },
      {
          "title": "My wallet crying after looking at the new Pokémon TCG prices",
          "image_url": "https://images.pokemontcg.io/base1/15_hires.png",  # Venusaur
          "link": "https://images.pokemontcg.io/base1/15.png",
      },
      {
          "title": (
              "That friend who opens his very first pack and gets a secret"
              " rare"
          ),
          "image_url": "https://images.pokemontcg.io/base1/2_hires.png",  # Blastoise
          "link": "https://images.pokemontcg.io/base1/2.png",
      },
  ]

  available_memes = [
      m for m in final_memes if m["image_url"] not in sent_memes
  ]
  if not available_memes:
    print("🔄 Сбрасываем историю отправленных мемов...")
    if os.path.exists("sent_memes.txt"):
      os.remove("sent_memes.txt")
    available_memes = final_memes

  meme_data = random.choice(available_memes)

  title = meme_data["title"]
  image_url = meme_data["image_url"]
  link = meme_data["link"]

  print(f"🔥 Публикуем карточку: {title}")
  ru_title = translate_text(title)

  intros = [
      "😂 **Чистая жиза из жизни коллекционеров:**",
      "🔥 **Когда реальность бьет сильнее, чем редкая карта:**",
      "📦 **Будни охотника за редкими сетами Pokémon TCG:**",
      "🐸 **Легендарные находки в бустерах:**",
  ]

  caption = (
      f"{random.choice(intros)}\n\n"
      f"📌 **{ru_title}**\n\n"
      f"🔗 [Официальная база карт]({link})"
  )

  # Скачиваем картинку
  try:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }
    img_response = requests.get(image_url, headers=headers, timeout=20)
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
  files = {"photo": ("card.png", image_bytes, "image/png")}

  response = requests.post(url, data=payload, files=files)
  print(f"Ответ Telegram API: {response.status_code}")

  if response.status_code == 200:
    print("✅ УСПЕШНО! Карточка успешно отправлена в канал.")
    with open("sent_memes.txt", "a", encoding="utf-8") as f:
      f.write(meme_data["image_url"] + "\n")
  else:
    print(f"❌ Ошибка Telegram: {response.text}")


run()
