from flask import Flask, request
import telebot
import os
import json
from deep_translator import GoogleTranslator
import langdetect

# =======================================
# CONFIGURAÇÕES INICIAIS
# =======================================
TOKEN = os.getenv("BOT_TOKEN") or "7646672843:AAHckKPRXKDbEwbRGfY7KTtQEtw27jrQl_U"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =======================================
# LER COMANDOS UNO DE JSON
# =======================================
with open("comandos_uno.json", "r", encoding="utf-8") as f:
    comandos_uno = json.load(f)

# =======================================
# COMANDO /jogos — Mostra o menu de jogos
# =======================================
@bot.message_handler(commands=['jogos'])
def menu_de_jogos(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🎯  Jogo do Quiz", callback_data="show"),
        telebot.types.InlineKeyboardButton("🪢  Jogo da Forca", callback_data="forca"),
        telebot.types.InlineKeyboardButton("🙊  Jogo dos Emojis", callback_data="emotions"),
        telebot.types.InlineKeyboardButton("🃏  Jogo do UNO", url="https://t.me/UnoGameBot")
    )
    bot.send_message(message.chat.id, "🎮 Escolha um Jogo:", reply_markup=markup)

# =======================================
# BOTÕES DO MENU
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
# DETECTA COMANDOS DO UNO BOT
# =======================================
# Corrigir barra dos comandos para evitar clique
def evitar_clique_comando(texto):
    return texto.replace("/", "⧸")

@bot.message_handler(func=lambda m: m.from_user and m.from_user.username == "UnoGameBot" and m.text)
def traduzir_mensagem_unobot(message):
    texto = message.text.strip()
    traducao = frases_uno.get(texto)
    if traducao:
        texto_seguro = evitar_clique_comando(traducao)
        bot.reply_to(message, f"🇧🇷 {texto_seguro}")
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
