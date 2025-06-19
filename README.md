<h1 align="center">
  🤖 Auto Caption Telegram Bot
</h1>

<p align="center">
  <img src="https://img.icons8.com/fluency/96/bot.png" alt="Bot Icon"/>
</p>

<p align="center">
  <b>A smart Telegram bot that automatically adds captions to media you send.</b><br>
  Built with ❤️ using <code>Python</code> + <code>Pyrogram</code> and deployed on <code>Heroku</code>.
</p>

---

## 🚀 Features

<ul>
  <li>📥 Automatically adds file name as caption for videos/documents</li>
  <li>🖼 Supports images, videos, documents</li>
  <li>⚡ Fast & lightweight</li>
  <li>🛠 Easy Heroku Deployment</li>
</ul>

---

## 🧠 How It Works

When you send a file to the bot, it:
1. Extracts file name
2. Adds it as caption
3. Sends it back instantly!

---

## 🔧 Deploy to Heroku

Click this button to deploy instantly to Heroku 👇

<p align="center">
  <a href="https://heroku.com/deploy?template=https://github.com/yourusername/auto-caption-bot">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" />
  </a>
</p>

---

## 📝 Setup Instructions

### 🔑 Required Variables

| Variable     | Description                     |
|--------------|---------------------------------|
| `API_ID`     | Get it from [my.telegram.org](https://my.telegram.org) |
| `API_HASH`   | From the same place as above    |
| `BOT_TOKEN`  | Get it from [@BotFather](https://t.me/BotFather) |

### 🧪 Manual Deploy (Optional)

```bash
git clone https://github.com/yourusername/auto-caption-bot
cd auto-caption-bot
heroku create
heroku config:set API_ID=12345 API_HASH=abc BOT_TOKEN=xyz
git push heroku main
🧰 Built With
Python 🐍

Pyrogram ⚙️

Heroku ☁️

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first.

🧑‍💻 Developer
<p align="center"> <a href="https://github.com/yourusername">👨‍💻 yourusername</a> </p>
