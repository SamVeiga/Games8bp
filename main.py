from flask import Flask, request
import telebot
import os

# Tradução automática
from deep_translator import GoogleTranslator
import langdetect

# =======================================
# CONFIGURAÇÕES INICIAIS
# =======================================
TOKEN = os.getenv("BOT_TOKEN") or "7646672843:AAHckKPRXKDbEwbRGfY7KTtQEtw27jrQl_U"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =======================================
# COMANDO /start — Mostra o menu de jogos
# =======================================
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🎯  Jogo do Quiz", callback_data="show"),
        telebot.types.InlineKeyboardButton("🪢  Jogo da Forca", callback_data="forca"),
        telebot.types.InlineKeyboardButton("🙊  Jogo dos Emojis", callback_data="emotions")
    )
    bot.send_message(message.chat.id, "🎮 Escolha um Jogo:", reply_markup=markup)

# =======================================
# Quando clica em um botão do menu
# =======================================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    jogo = call.data
    comandos = {
        "show": "/quiz",
        "forca": "/forca",
        "emotions": "/jogodoemotions"
    }
    comando = comandos.get(jogo, '/comando')
    bot.send_message(call.message.chat.id, comando)

# =======================================
# MENSAGENS — Tradução automática para UNO Bot e bots oficiais
# =======================================
@bot.message_handler(func=lambda m: True)
def traduzir_mensagens(message):
    texto = message.text
    if not texto:
        return

    # Ignora mensagens do próprio bot para evitar loop
    if message.from_user and message.from_user.id == bot.get_me().id:
        return

    # Traduz mensagens do UNO Bot pelo username 'unobot'
    if message.from_user and message.from_user.username and message.from_user.username.lower() == "unobot":
        try:
            traducao = GoogleTranslator(source='auto', target='pt').translate(texto)
            bot.reply_to(message, f"🔁 {traducao}")
        except Exception as e:
            print(f"Erro ao traduzir UNO Bot: {e}")
        return

    # Traduz mensagens de bots oficiais (is_bot == True)
    if message.from_user and message.from_user.is_bot:
        try:
            try:
                idioma = langdetect.detect(texto)
            except:
                idioma = 'desconhecido'

            if idioma != 'pt':
                traducao = GoogleTranslator(source='auto', target='pt').translate(texto)
                bot.reply_to(message, f"🔁 {traducao}")
        except Exception as e:
            print(f"Erro ao traduzir bot oficial: {e}")

# =======================================
# WEBHOOK — Para funcionar no Render
# =======================================
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return 'Bot Games8bp funcionando!', 200

# =======================================
# INÍCIO — Porta obrigatória para o Render
# =======================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
