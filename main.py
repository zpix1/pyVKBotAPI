from vk_api import VK, VKMessage

from params import creds

api = VK(**creds)

favorite_pictures = api.upload_photos(list(map(lambda filename: open('pictures/'+filename,'rb'), ['big.jpg','normal.png','small.png'])))

@api.on_message_listener(time_interval = 1)
def send_favorite_pictures(message):
    message.receiver = message.sender
    # print
    api.send_message(message)
    api.send_message(VKMessage(receiver = message.sender, text = 'Look at this pictures!', ))

# api.on_message_listener(send_favorite_pictures,1)