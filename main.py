from flask import Flask, request
import telebot
import os

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
        telebot.types.InlineKeyboardButton("🎯 Show do Milhão", callback_data="show"),
        telebot.types.InlineKeyboardButton("🪢 Jogo da Forca", callback_data="forca"),
        telebot.types.InlineKeyboardButton("😄 Jogo dos Emotions", callback_data="emotions")
    )
    bot.send_message(message.chat.id, "🎮 Escolha um jogo para começar:", reply_markup=markup)

# =======================================
# Quando clica em um botão do menu
# =======================================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    jogo = call.data
    comandos = {
        "show": "//showdomilhao",
        "forca": "//jogodaforca",
        "emotions": "//jogodoemotions"
    }
    resposta = f"✅ Para jogar, envie:\n\n`{comandos.get(jogo, '//comando')}`"
    bot.send_message(call.message.chat.id, resposta, parse_mode="Markdown")

# =======================================
# WEBHOOK — Para funcionar no Render
# =======================================
@app.route('/' + TOKEN, methods=['POST'])  # ← CORRIGIDO AQUI!
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
