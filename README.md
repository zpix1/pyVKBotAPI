This README is created only for russian speaking people. If you want to use this api to create a vk bot, but you don't speak russian, you should send an email (zpix-dev@list.ru)

# pyVKBotAPI - API для создания ботов в социальной сети ВКонтакте (vk.com)
## Что это?
Это обертка для pythonVKAPI. Поскольку, по сути, vk модуль для Python это лишь обертка HTTP API, писать ботов на ней не особо удобно. pyVKBotAPI упрощает задачу и позволяет создать своего бота в несколько строк кода.
## Установка
Для использования API следуйте следующим инструкциям:
1. Проверьте, что у вас стоит Python 3, если нет - поставьте его
2. Скачайте модуль api vk `pip install vk`
3. Скачайте или склонируйте этот git репозиторий
## Использование
Разберем простого вк бота на этом API

Вы должны указать логин и пароль вашего бота в вк (api для групп еще в разработке). Это легко сделать - создайте файл `params.py` со следующим содержимым:
```Python
creds = {
    "login": "Логин Бота",
    "password": "Пароль Бота",
    "app_id": "ID приложения"
}
```
Уже сейчас вы можете его запустить командой `python main.py`
```Python
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

```
Как видно, все работает

![alt text](https://i.imgur.com/vaitmAT.png "")

