import os

import chromadb
import openai
import pandas as pd
from typing import List, Dict, Any, Union, Tuple
import json

from chromadb.utils import embedding_functions

import config
from vdb.chroma import search

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

        # vector db
        self.client = chromadb.PersistentClient(path=config.CHROMA_DB)
        emb_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=config.OPENAI_API_KEY, model_name=config.MODEL_EMBEDDING)
        self.collection = self.client.get_collection(name=config.CHROMA_COLLECTION, embedding_function=emb_fn)

        # changed after init
        self.messages_full_log = []
        self.messages_context = []
        self.conversation_context: str = ''
        self.last_answer_from_assistant: str = ''
        # self.most_relevant_docs: List[Dict] = []
        self.most_relevant_docs_df = pd.DataFrame({'ids': [], 'parent_code': [], 'parent_title': [], 'distances': [], 'documents': []})

    def ask_gpt(self, message_txt: str, role: str = 'user', use_system_role=True) -> str:
        # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
        message = {"role": role, "content": message_txt}
        messages = self.get_messages_to_ask(message=message, use_system_role=use_system_role)

        answer = None
        while answer is None:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
            try:
                answer = response['choices'][0]['message']['content']
            except:
                if self._has_context():
                    # remove the oldest message from context, probably because the context is too long
                    self.messages_context.pop(0)
                else:
                    # must be something else wrong
                    answer = 'Cer scuze, nu pot gasi un raspuns bun. Reformulati, va rog.'

        self.messages_context.append(message)
        message_from_assistant = {'role': 'system', 'content': answer}
        self.messages_context.append(message_from_assistant)
        self.last_answer_from_assistant = answer
        return answer

    def get_messages_to_ask(self, message: Dict, use_system_role=True) -> List[Dict[str, str]]:
        messages = []

        # add system role if specified
        if use_system_role and self._is_system_role_specified():
            messages.append({"role": "system", "content": self.role_system})

        # add context with prior messages
        if self._has_context() > 0:
            messages += self.messages_context

        # add last message from user
        messages.append(message)

        # add message with relevant docs if there are any
        message_about_relevant_docs = self.message_with_relevant_docs(message['content'])
        if message_about_relevant_docs is not None:
            messages.append(message_about_relevant_docs)

        return messages

    def has_relevant_docs(self) -> bool:
        return len(self.most_relevant_docs_df) > 0

    def update_most_relevant_docs(self, message: str):
        results = search(query=message, collection=self.collection, as_df=True)
        self.most_relevant_docs_df = pd.concat([self.most_relevant_docs_df, results], ignore_index=True) # self.most_relevant_docs_df.append(results, ignore_index=True)
        self.most_relevant_docs_df = self.most_relevant_docs_df.sort_values(by=['distances'], ascending=True)
        self.most_relevant_docs_df = self.most_relevant_docs_df.drop_duplicates(subset=['parent_code'], keep='first')
        self.most_relevant_docs_df = self.most_relevant_docs_df[self.most_relevant_docs_df['distances'] < config.DISTANCE_THRESHOLD]
        self.most_relevant_docs_df = self.most_relevant_docs_df.head(config.TOP_K_DOCS_RECOMMEND)

    def get_titles_most_relevant_docs(self) -> List[str]:
        return self.most_relevant_docs_df['parent_title'].tolist()

    def message_with_relevant_docs(self, message: str) -> {}:
        self.update_most_relevant_docs(message)
        message = None
        if self.has_relevant_docs():
            message = {
                "role": "user",
                "content": "servicii probabil relevante: " + json.dumps(self.get_titles_most_relevant_docs(), ensure_ascii=False)}
        return message

    def _is_system_role_specified(self) -> bool:
        return self.role_system is not None and self.role_system != ''

    def _has_context(self) -> bool:
        return len(self.messages_context) > 0

    def get_context_from_past(self) -> str:
        pass

    def clear_context(self):
        self.messages_context = []
        self.conversation_context = ''


