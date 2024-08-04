import telebot
import os
import random

# Token del bot proporcionado por BotFather
TOKEN = '6930526870:AAH8nnWgG4NlRuo7nl3io3YCOjZ2Tk74WEc'

# ID del canal al que quieres enviar los archivos
CANAL_ID = '@hakai_referencias'

# Archivos para almacenar los últimos IDs procesados de imagen y video
STATE_FILE_PHOTO = 'last_processed_photo.txt'
STATE_FILE_VIDEO = 'last_processed_video.txt'

# Crea el objeto bot
bot = telebot.TeleBot(TOKEN)

# Conjuntos para almacenar los IDs procesados
processed_photos = set()
processed_videos = set()

# Función para enviar archivo al canal especificado
def send_file_to_channel(file_id, file_type, caption):
    try:
        # Enviar el archivo al canal especificado
        if file_type == 'photo':
            bot.send_photo(CANAL_ID, file_id, caption=caption)
        elif file_type == 'video':
            bot.send_video(CANAL_ID, file_id, caption=caption)
    
    except Exception as e:
        print(f'Error al enviar archivo: {str(e)}')
        

# Función para manejar mensajes de texto y archivos multimedia
@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_messages(message):
    chat_id = message.chat.id
    
    # Verificar si es una foto o video con comentario que comienza con /sendfiles
    if message.caption:
        if message.caption.startswith('/sendfiles'):
            try:
                # Eliminar el comando /sendfiles del caption
                caption = message.caption.replace('/sendfiles', '', 1).strip()
                
                file_id = message.photo[-1].file_id if message.content_type == 'photo' else message.video.file_id
                file_type = message.content_type
                
                # Verificar si el archivo ya ha sido procesado
                if check_if_processed(file_id, file_type):
                    return
                
                # Guardar el ID del archivo procesado
                save_processed_file(file_id, file_type)
                
                # Eliminar el mensaje que contiene el comando sendfiles antes de enviarlo al canal
                bot.delete_message(chat_id, message.message_id)
                
                # Enviar el archivo al canal especificado sin incluir el mensaje original
                send_file_to_channel(file_id, file_type, caption)
            
            except Exception as e:
                print(f'Error al procesar el mensaje: {str(e)}')
        else:
            # Responder si el comando /sendfiles no está bien escrito
            bot.reply_to(message, '¡Error! comando mal escrito..')

# Función para verificar si el archivo ya ha sido procesado
def check_if_processed(file_id, file_type):
    try:
        if file_type == 'photo':
            return file_id in processed_photos
        elif file_type == 'video':
            return file_id in processed_videos
    
    except Exception as e:
        print(f'Error al verificar el archivo procesado: {str(e)}')
        return False

# Función para guardar el ID del archivo procesado
def save_processed_file(file_id, file_type):
    try:
        if file_type == 'photo':
            processed_photos.add(file_id)
            with open(STATE_FILE_PHOTO, 'a') as f:
                f.write(f'{file_id}\n')
        elif file_type == 'video':
            processed_videos.add(file_id)
            with open(STATE_FILE_VIDEO, 'a') as f:
                f.write(f'{file_id}\n')
    
    except Exception as e:
        print(f'Error al guardar el archivo procesado: {str(e)}')

# Función para manejar comandos
@bot.message_handler(commands=['sendfiles'])
def handle_send_files(message):
    bot.reply_to(message, '')

# Iniciar el bot
bot.polling()