from enum import Enum
import sys
import json
import threading
import requests

import vk

import utils as u


class MessageType(Enum):
    INCOMING = 1
    OUTCOMING = 2

class VKError(Exception):
    pass

class VKMessage():
    def __init__(self,text = '', photos = [], documents = [], type = MessageType.OUTCOMING, sender = 0, receiver = 0):
        self.text = text
        self.attachments = {}
        self.attachments['photos'] = photos
        self.attachments['documents'] = documents
        self.sender = sender

    @staticmethod
    def _from_vk_message_dict(obj):
        photos = []
        if 'attachments' in obj:
            for e in obj['attachments']:
                if e['type'] == 'photo':
                    photos.append("photo{}_{}".format(e['photo']['owner_id'],e['photo']['pid']))

        return VKMessage(text = obj['body'], type = MessageType.INCOMING, sender = obj['uid'], receiver = 0, photos = photos)

class VK():

    def __init__(self,app_id=-1, login='', password='', token=''):
        if app_id == -1:
            raise VKError('App id is not specified.')
        if token != '':
            self.session = vk.AuthSession(app_id=app_id, access_token=token)
        else:
            if login == '' or password == '':
                raise VKError(
                    'Access token or login password pair is not specified.')
            else:
                self._session = vk.AuthSession(
                    app_id=app_id, user_login=login, user_password=password, scope='friends,messages,wall,status,photos')
        self._api = vk.API(self._session)

        self._symbs = [' ', ' ']
        self._no_spam_trigger = 0
        # self._myself = _api.users.get()[0]['uid']

    def on_message_listener(self,time_interval = 10):
        """This function returns a thread that calls listener function if new message arrived and checks it every time_interval seconds."""
        def wrapper(listener):
            def thread_func(listener, ti):
                api = self._api
                while True:
                    n = 1
                    messages = api.messages.get(count=n)
                    if(len(messages) > 1):
                        for i in range(1, len(messages)):
                            if messages[i]['read_state'] == 0:
                                api.messages.markAsRead(
                                    message_ids=str(messages[i]['mid']))
                                print(messages[i])
                                listener(VKMessage._from_vk_message_dict(messages[i]))
                    u.sleep(ti)
            message_thread = threading.Thread(target=thread_func,
                                              args=(listener, time_interval))
            message_thread.start()
            return message_thread
        return wrapper

    def send_message(self, message):
        """Send a message to user_id."""
        self._no_spam_trigger = (self._no_spam_trigger + 1) % len(self._symbs)

        attachments = message.attachments['photos']
        # if len(message.attachments['photos']) > 0:
        #     for file in message.attachments['photos']:
        #         attachments.append(self._upload_photo(file))

        self._api.messages.send(user_id=message.receiver, message=message.text +
                                    self._symbs[self._no_spam_trigger], attachment = attachments)


    def upload_photos(self, photo_files_list):
        """This function uploads photos to vk servers and returns photo ids list."""
        attachments = []
        for file in photo_files_list:
            attachments.append(self._upload_photo(file))
        return attachments

    def _upload_photo(self,file):
        api = self._api
        settings = api.photos.getMessagesUploadServer()
        print(settings)
        # import pdb; pdb.set_trace()

        r = requests.post(settings['upload_url'], files={'photo': file})
        
        print(r.status_code == requests.codes.ok)
        result = r.json()
        # print(result)

        photo = api.photos.saveMessagesPhoto(server=result['server'],
                                             photo=result['photo'],
                                             hash=result['hash'])
        return photo[0]['id']
