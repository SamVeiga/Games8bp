from flask import Flask, request
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Lista de jogos
jogos = [
    {"nome": "🎯 Show do Milhão", "comando": "//show"},
    {"nome": "🪢 Jogo da Forca", "comando": "//forca"},
    {"nome": "😃 Jogo dos Emotions", "comando": "//emotions"}
]

# Mensagem com os botões
def montar_mensagem_jogos():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for jogo in jogos:
        btn = telebot.types.InlineKeyboardButton(text=jogo["nome"], callback_data=jogo["comando"])
        markup.add(btn)
    return markup

# Comando para exibir os jogos
@bot.message_handler(commands=['jogos'])
def enviar_lista_jogos(message):
    bot.send_message(
        message.chat.id,
        "🎮 *Jogos Disponíveis*\n\nEscolha abaixo o jogo que você quer iniciar:",
        reply_markup=montar_mensagem_jogos(),
        parse_mode="Markdown"
    )

# Quando a pessoa clica no botão
@bot.callback_query_handler(func=lambda call: True)
def tratar_callback(call):
    bot.answer_callback_query(call.id, f"Use o comando: {call.data}")

# Webhook
@app.route(f'/{API_TOKEN}', methods=['POST'])
def receber_mensagem():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot Games8bp está rodando!", 200

# Iniciar
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render fornece PORT dinamicamente
    app.run(host='0.0.0.0', port=port)
