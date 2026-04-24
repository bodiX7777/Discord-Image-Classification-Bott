import telebot
from dotenv import load_dotenv
import os
from cv_service import handle_image
load_dotenv()
bot = telebot.TeleBot(token=os.getenv("TG_API_TOKEN"))

# Замени 'TOKEN' на токен твоего бота


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        f'Привет, {message.from_user.first_name}!\n\n'
        'Я бот, который распознает спортивные мячи. Отправь мне фото, и я попробую найти все, что знаю'
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
  
    downloaded_file = bot.download_file(file_info.file_path)
    image_path = f'images/{message.message_id}.jpg'
    with open (image_path, 'wb') as file:
        file.write(downloaded_file)
 
    
    result = handle_image(image_path)


    response_text = ''
    if len(result) > 0:
        response_text = 'Найдены обыекты: \n'
        for obj in result:
            response_text += f'Класс: {obj["class"]}, вероятность: {obj["confidence"]}%\n'
        with open(image_path.split('.')[0] + '_result.jpg', 'rb') as file:
            bot.send_photo(message.chat.id, file, caption=response_text)
    else:
        response_text = 'Объекты не обнаружены'
        bot.send_message(message.chat.id, response_text)

    os.remove(image_path) 




bot.infinity_polling()