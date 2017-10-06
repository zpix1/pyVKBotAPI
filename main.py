from vk_api import VK, VKMessage # Импортируем главный класс и класс сообщения

from params import creds # Ипортируем модуль с логином и паролем

api = VK(**creds) # Создаем объект API

# Загружаем картинки на сервер вк, получаем их идентификаторы
favorite_pictures = api.upload_photos(list(map(lambda filename: open('pictures/'+filename,'rb'), ['big.jpg','normal.png','small.png'])))

# Этот декоратор вызывает функцию каждый при каждом новом сообщении
@api.on_message_listener(time_interval = 1)
def send_favorite_pictures(message):
    # Так как мы отвечаем на сообщение, сменим получателя на отправителя
    message.receiver = message.sender
    # Посылаем идентичное полученному сообщение (играем в повторюшку)
    api.send_message(message)
    # Посылаем наши картинки
    api.send_message(VKMessage(receiver = message.sender, text = 'Посмотри на эти фотографии', photos = favorite_pictures))
