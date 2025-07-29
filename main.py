from flask import Flask, request
import telebot
import os

# 🔐 Coloque aqui o token que o BotFather te deu
TOKEN = os.environ.get("BOT_TOKEN", "COLE_SEU_TOKEN_AQUI")
bot = telebot.TeleBot(TOKEN)

# ✅ Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎮 Olá! Eu sou o bot de jogos!\nUse /jogar para ver os jogos disponíveis.")

# ✅ Comando /ajuda
@bot.message_handler(commands=['ajuda'])
def ajuda(message):
    texto = (
        "📋 Comandos disponíveis:\n"
        "/jogar - Iniciar jogo\n"
        "/placar - Ver pontuação\n"
        "/regras - Ver regras dos jogos"
    )
    bot.reply_to(message, texto)

# ✅ Comando /jogar
@bot.message_handler(commands=['jogar'])
def jogar(message):
    jogos = [
        "1️⃣ Show do Milhão",
        "2️⃣ Jogo da Forca",
        "3️⃣ Quiz Relâmpago"
    ]
    resposta = "Escolha o jogo que deseja jogar:\n\n" + "\n".join(jogos)
    bot.reply_to(message, resposta)

# ✅ Flask + Webhook
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Bot de jogos está online!'

@app.route('/', methods=['POST'])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return 'OK', 200

if __name__ == '__main__':
    app.run()
