import telebot
from openai import OpenAI
import os

# --- CONFIGURACIÓN DE LA NUBE ---
# Leemos las variables de entorno que pondremos en Render
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Configuración de Groq (La Inteligencia en la Nube)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# Nombre del modelo Llama 3 70B (Muy potente y rápido)
MODEL_NAME = "llama3-70b-8192"

bot = telebot.TeleBot(BOT_TOKEN)

print("🚀 IBC MEDIC CLOUD Iniciado...")

# Personalidad del nuevo bot
SYSTEM_PROMPT = """
Eres el asistente médico IBC_MEDIC_CLOUD.
Tienes acceso a los conocimientos médicos más actualizados gracias a la infraestructura en la nube.
Responde con precisión, rapidez y tono profesional.
Siempre en español.
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_id = message.chat.id
        user_text = message.text
        
        # Indicar que está escribiendo
        bot.send_chat_action(chat_id, 'typing')
        
        # Consulta a Groq (No necesita tu Mac encendida)
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

# Iniciar el bot
bot.polling(none_stop=True)
