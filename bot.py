import os
import telebot
from openai import OpenAI

# --- VERIFICACIÓN DE VARIABLES ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

print("DEBUG BOT_TOKEN:", BOT_TOKEN)
print("DEBUG GROQ_API_KEY:", GROQ_API_KEY)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN no está definido en las variables de entorno")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY no está definido en las variables de entorno")

# --- CONFIGURACIÓN GROQ ---
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama3-70b-8192"
bot = telebot.TeleBot(BOT_TOKEN)

print("🚀 IBC MEDIC CLOUD Iniciado correctamente...")

# --- PERSONALIDAD DEL BOT ---
SYSTEM_PROMPT = """
Eres el asistente médico IBC_MEDIC_CLOUD del Instituto Biológico Centroamericano.
Eres un experto en medicina interna, urgencias y medicina integrativa.
Tus respuestas deben ser directas, con tono profesional y técnico.
Siempre responde en español.
"""

# --- MANEJADOR DE MENSAJES ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_id = message.chat.id
        user_text = message.text

        bot.send_chat_action(chat_id, 'typing')

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.6
        )

        respuesta = response.choices[0].message.content
        bot.reply_to(message, respuesta)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error en el sistema: {e}")

# --- INICIAR BOT ---
bot.polling(none_stop=True)
