import time
from telethon.sync import TelegramClient
import json
from config import api_id, phone, api_hash
from os.path import join, dirname

client = TelegramClient(phone, api_id, api_hash)
client.start()


def load_file(title_file):
    with open(title_file ) as file:
        return json.load( file ) 

def main():
    path_to_self = dirname( __file__ )
    normativs = load_file( join( path_to_self, 'prof_normativ.json' ) )
    bot_name = 'ChatGPT_ForTelegramBot'
    bot_gpt=client.get_entity(bot_name)
    #  Название упражнения:
    #     {normativ['title']}
    #  Если встречается  слово шланг используй слово рукав
    #     Если встречается  слово сосуд используй слово емкость
    for normativ in normativs.values():
        msg = f'''
        Упражнение:
        {normativ['process']}

        Напиши минимально необходимое оборудование через запятую:
        '''
        request = request_gpt(client, bot_gpt, msg)
        print(request)
        if request.startswith('Максимальная длина контекста составляет'):
            request = 'БОП, снаряжение, веревка, СИЗОД, рукава, ПТВ, секундомер'
        normativ['devices'] = request
    # exit()
    with open(join( path_to_self, 'prof_normativ_update.json' ), 'w') as f:
        json.dump(normativs,f)


def request_gpt(client, bot, msg)->str:
    client.send_message(entity=bot,message=msg)
    send_msg_id = get_last_msg(bot)[0].id
    while True:
        time.sleep(17)
        msg = get_last_msg(bot)
        if msg[0].id != send_msg_id:
            return(msg[0].message)


def get_last_msg(bot):
    return client.get_messages(bot, limit= 1) 


def create_educational_question(subject_study, theme, question):
    bot_gpt=client.get_entity('ChatGPT_ForTelegramBot')
    msg = f'''
Дисциплина: {subject_study}
Тема: {theme}
Учебный вопрос: {question}

Напиши реферат:
    '''
    return request_gpt(client, bot_gpt, msg)


if __name__ == '__main__':
    main()