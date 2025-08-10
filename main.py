from flask import Flask, request
import telebot
import os
import re

# =======================================
# CONFIGURAÇÕES INICIAIS
# =======================================
TOKEN = os.getenv("BOT_TOKEN") or "7646672843:AAHckKPRXKDbEwbRGfY7KTtQEtw27jrQl_U"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =======================================
# Funções utilitárias para o menu
# =======================================

def build_menu_markup():
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🎯  Jogo do Quiz", callback_data="show"),
        telebot.types.InlineKeyboardButton("🪢  Jogo da Forca", callback_data="forca"),
        telebot.types.InlineKeyboardButton("❌⭕  Jogo da Velha", callback_data="velha"),
        telebot.types.InlineKeyboardButton("🃏  Jogo do UNO", callback_data="uno"),
        telebot.types.InlineKeyboardButton("📒  Bobbie Goods", callback_data="bobbie_goods")  # Novo jogo
    )
    return markup

def enviar_menu_de_jogos(chat_id):
    """Envia o menu de jogos para o chat_id fornecido (reutilizável)."""
    try:
        markup = build_menu_markup()
        print(f"[DEBUG] Enviando menu de jogos para chat_id={chat_id}")
        bot.send_message(chat_id, "🎮 Escolha um Jogo:", reply_markup=markup)
    except Exception as e:
        print(f"Erro ao enviar menu de jogos: {e}")


# =======================================
# COMANDO /jogos — Mostra o menu de jogos
# =======================================
@bot.message_handler(commands=['jogos'])
def menu_de_jogos(message):
    # usar message.chat.id (antes havia uma variável indefinida `chat_id`)
    enviar_menu_de_jogos(message.chat.id)


# =======================================
# CALLBACKS dos botões do menu
# =======================================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    jogo = call.data
    comandos = {
        "show": "/quiz",
        "forca": "/forca",
        "velha": "@xoBot",
        "uno": "/new@unopybot",
        "bobbie_goods": "/start@DoodleGatorBot"  # Novo jogo
    }
    comando = comandos.get(jogo, '/comando')
    try:
        bot.send_message(call.message.chat.id, comando)
    except Exception as e:
        print(f"Erro ao enviar comando do callback: {e}")


# =======================================
# DETECÇÃO DE VENCEDOR DO UNO
# =======================================
TROFEU_STICKER_ID = "CAACAgEAAxkBAAII2GiXJUtcpbS_fG2arXHW8zRF066PAAI5AwACdR4gRMnYSPTiUO3wNgQ"

# Use getattr para evitar AttributeError caso from_user seja None
@bot.message_handler(func=lambda m: m.from_user and getattr(m.from_user, 'username', '').lower() == "unogamebot")
def detectar_vencedor_unobot(message):
    chat_id = message.chat.id
    texto_msg = message.text or ""

    try:
        # Detectar padrão de vitória do UnoBot (ex: "Matheus won!")
        match = re.search(r"(.+?)\s+won!", texto_msg, re.IGNORECASE)
        if match:
            vencedor = match.group(1).strip()

            # Usar Markdown V1 (asteriscos simples) ou ajustar parse_mode conforme preferir
            mensagem_vitoria = (
                f"🏆🎉 *{vencedor.upper()} É O CAMPEÃO DO UNO!* 🎉🏆\n\n"
                f"🔥 Parabéns pela vitória esmagadora! 🔥"
            )
            bot.send_message(chat_id, mensagem_vitoria, parse_mode="Markdown")

            # Enviar sticker de troféu
            bot.send_sticker(chat_id, TROFEU_STICKER_ID)

            # Enviar novamente o menu de jogos
            enviar_menu_de_jogos(chat_id)

    except Exception as e:
        print(f"Erro ao detectar vitória: {e}")


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
    # Se quiser setar webhook automaticamente (opcional), descomente e ajuste a URL:
    # bot.remove_webhook()
    # bot.set_webhook(url=f"https://SEU_DOMINIO_AQUI/{TOKEN}")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
