import os
import openai

import config

from typing import List, Dict, Any, Union, Tuple

# set configs
openai.api_key = os.getenv("OPENAI_API_KEY", config.OPENAI_API_KEY)


class Chat:

    def __init__(
            self,
            model=config.MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            top_p=config.TOP_P,
            frequency_penalty=config.FREQUENCY_PENALTY,
            presence_penalty=config.PRESENCE_PENALTY,
            role_system=config.ROLE_SYSTEM,
    ):
        # settings at init
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.role_system = role_system

        # changed after init
        self.messages_full_log = []
        self.messages_last_context = []
        self.conversation_context: str = ''
        self.last_answer: str = ''

    def ask_gpt(self, message_txt: str, role: str = 'user', use_system_role=True) -> str:
        # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
        message = {"role": role, "content": message_txt}
        messages = self.get_messages_to_ask(message=message, use_system_role=use_system_role)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
        )
        self.messages_last_context.append(message)
        answer = response['choices'][0]['message']['content']
        message_from_assistant = {'role': 'system', 'content': answer}
        self.messages_last_context.append(message_from_assistant)
        self.last_answer = answer
        return answer

    def get_messages_to_ask(self, message: Dict, use_system_role=True) -> List[Dict[str, str]]:
        messages = []

        if use_system_role and self._is_system_role_specified():
            messages.append({"role": "system", "content": self.role_system})

        if self._has_context() > 0:
            messages += self.messages_last_context

        messages.append(message)

        return messages

    def _is_system_role_specified(self) -> bool:
        return self.role_system is not None and self.role_system != ''

    def _has_context(self) -> bool:
        return len(self.messages_last_context) > 0

    def get_context_from_past(self) -> str:
        pass

    def clear_context(self):
        self.messages_last_context = []
        self.conversation_context = ''


