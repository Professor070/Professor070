<h1 align="center">
  🤖 Auto Caption Telegram Bot
</h1>

<p align="center">
  <img src="https://img.icons8.com/fluency/96/bot.png" alt="Bot Icon"/>
</p>

<p align="center">
  <b>A smart Telegram bot that automatically adds captions to any media you send.</b><br>
  Built with ❤️ using <code>Python</code> + <code>Pyrogram</code> and deployable on <code>Heroku</code>.
</p>

---

## 🚀 Features

<ul>
  <li>✨ Instantly adds the file name as a caption for videos, documents & images</li>
  <li>🖼 Supports photos, videos, and all Telegram document types</li>
  <li>⚡ Super fast & lightweight</li>
  <li>🛠 Easy one-click Heroku deployment</li>
</ul>

---

## 🧠 How It Works

Just send any file to the bot and it will:
1. Extract the file name
2. Add it as the caption
3. Instantly return the media with the caption!

---

## 🔧 Deploy to Heroku

Deploy your own bot to Heroku in seconds 👇

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/yourusername/auto-caption-bot">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" />
  </a>
</p>

---

## 📝 Setup Instructions

### 🔑 Required Variables

| Variable     | Description                                       |
|--------------|---------------------------------------------------|
| `API_ID`     | From [my.telegram.org](https://my.telegram.org)   |
| `API_HASH`   | From [my.telegram.org](https://my.telegram.org)   |
| `BOT_TOKEN`  | From [@BotFather](https://t.me/BotFather)         |

---

### 🚀 Manual Deploy (Optional)

```bash
git clone https://github.com/yourusername/auto-caption-bot
cd auto-caption-bot
heroku create
heroku config:set API_ID=12345 API_HASH=abc BOT_TOKEN=xyz
git push heroku main
```

---

## 🧰 Built With

- Python 🐍
- Pyrogram ⚙️
- Heroku ☁️

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 👨‍💻 Developer

<p align="center">
  <a href="https://github.com/Professor070">👨‍💻 Professor070</a>
</p>

---

<p align="center"><b>⭐ Star this repo if you like it!</b></p>
