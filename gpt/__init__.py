import time
from telethon.sync import TelegramClient
import openai as ai

# openai.api_key = api_key

def create_answere(api_key):
    ai.api_key = api_key
    def generate_gpt3_response(subject_study, theme, question, print_output=False):
        """
        Query OpenAI GPT-3 for the specific key and get back a response
        :type user_text: str the user's text to query for
        :type print_output: boolean whether or not to print the raw output JSON
        """

        return 'template'

        user_text = f'''
Дисциплина: {subject_study}.
Тема: {theme}.
Учебный вопрос: {question}.

Напиши реферат на 1500 слов:
'''     
        # ai.Completion.create()
        completions = ai.Completion.create(
            engine='text-davinci-003',  # Determines the quality, speed, and cost.
            temperature=0.5,            # Level of creativity in the response
            prompt=user_text,           # What the user typed in
            max_tokens=3500,             # Maximum tokens in the prompt AND response
            n=1,                        # The number of completions to generate
            stop=None,                  # An optional setting to control response generation
        )

        # Displaying the output can be helpful if things go wrong
        if print_output:
            print(completions)

        # Return the first choice's text
        return completions.choices[0].text.split('\n')
    
    return generate_gpt3_response



class BotGPT:

    def __init__(self, phone, api_id, api_hash) -> None:
        self.client = TelegramClient(phone, api_id, api_hash)
        # print(phone, api_id, api_hash)
        self.client.start()
        self.bot_gpt = self.client.get_entity('ChatGPT_ForTelegramBot')
        
    def request_gpt(self,  msg)->str:
        self.client.send_message(entity=self.bot_gpt,message=msg)
        send_msg_id = self.get_last_msg().id
        while True:
            time.sleep(17)
            msg = self.get_last_msg()
            if msg.id != send_msg_id:
                return msg.message.split('\n') 


    def get_last_msg(self):
        return self.client.get_messages( self.bot_gpt, limit= 1 )[0]


    def create_educational_question(self, subject_study, theme, question):
        msg = f'''
    Дисциплина: {subject_study}.
    Тема: {theme}.
    Учебный вопрос: {question}.

    Напиши реферат на 1500 слов:
        '''
        return self.request_gpt(msg)

