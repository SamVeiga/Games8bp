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
# BALÃO DE AJUDA — Enviado sempre que o UNO Bot fala
# =======================================
ajuda_texto = (
    "📘 *Comandos do UNO Bot*\n\n"
    "`/join` ➕ Entrar\n"
    "`/start` ▶️ Iniciar\n"
    "`/skip` ⏩ Pular vez\n"
    "`/kick` 👢 Expulsar\n"
    "`/leave` 🚪 Sair\n"
    "`/close` 🔒 Fechar lobby\n"
    "`/open` 🔓 Reabrir lobby\n"
    "`/ranking` 🏆 Pontuação\n"
    "`/modes` 🎮 Modos de jogo\n"
    "`/howto` 📘 Regras\n"
    "`/settings` ⚙️ Regras/config\n"
    "`/alert` 🔔 Notificar\n"
    "`/multion` 📣 Múltiplos alertas\n"
    "`/multioff` 🔕 Sem alertas\n"
    "`/about` ℹ️ Sobre o bot\n"
    "`/source` 💻 Código-fonte\n"
    "`/news` 📰 Novidades"
)

ultimo_balao_id = {}

@bot.message_handler(func=lambda m: m.from_user and m.from_user.username == "UnoGameBot" and m.text)
def mostrar_balao_ajuda(message):
    chat_id = message.chat.id
    try:
        if chat_id in ultimo_balao_id:
            bot.delete_message(chat_id, ultimo_balao_id[chat_id])
        enviado = bot.send_message(chat_id, ajuda_texto, parse_mode="Markdown")
        ultimo_balao_id[chat_id] = enviado.message_id
    except Exception as e:
        print(f"Erro ao mostrar ou apagar balão: {e}")

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
