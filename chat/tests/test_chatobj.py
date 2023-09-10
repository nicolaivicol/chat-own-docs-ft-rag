import unittest
import json

import config
from chat.chatobj import Chat

class TestAll(unittest.TestCase):

    # @classmethod
    # def setUpClass(self):
    #     code_service = '003000100'
    #     self.raw_json = get_service(code=code_service, save_to_disk=True)

    def test_chat_simple(self):
        chat = Chat()
        message = "Salut"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

        message = "certificat de casatorie"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

        message = "Certificat/duplicat al certificatului de căsătorie"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

    def test_chat_question_out_domain(self):
        chat = Chat()
        message = "Care este cursul valutar?"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

    def test_chat_question_out_domain_2(self):
        chat = Chat()
        message = "Cum sa ajung la Orhei?"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

    def test_chat_cine_esti(self):
        print(config.ROLE_SYSTEM)
        chat = Chat()
        message = "Cine esti?"
        chat.ask_gpt(message)
        print(f'User: {message}')
        print(f'Assistant: {chat.last_answer_from_assistant}')

