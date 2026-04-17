import telebot
from openai import OpenAI
import os

# --- CONFIGURACIÓN ---
# Leemos las llaves que pusiste en Render (Environment Variables)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Configuración del cliente OpenAI (Groq)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Modelo a usar (Llama 3 70B - Ultra rápido y potente)
MODEL_NAME = "llama3-70b-8192"

bot = telebot.TeleBot(BOT_TOKEN)

print("🚀 IBC MEDIC CLOUD Iniciado correctamente...")

# Personalidad del Bot
SYSTEM_PROMPT = """
Eres el asistente médico IBC_MEDIC_CLOUD.
Eres un experto en medicina interna y urgencias.
Tus respuestas deben ser directas, con tono profesional y técnico.
Siempre responde en español.
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        
        # Indicar que está escribiendo
        bot.send_chat_action(chat_id, 'typing')
        
        # Consulta a Groq (La IA en la nube)
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
        bot.reply_to(message, f"Error en el sistema en la nube: {e}")

# Iniciar el bot con modo "nuestop" (para que nunca se apague por errores pequeños)
bot.polling(none_stop=True)
