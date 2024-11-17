# coding: utf-8
from dataclasses import dataclass
import typing

from pydantic import BaseModel
import requests

from . import interface


@dataclass
class UrlDesignator:
    CHAT_COMPLETIONS: str = '/v1/chat/completions'


class ChatGptApi:

    BASE_URL: str = 'https://api.openai.com'

    _headers: dict
    _request: requests.Session

    def __init__(self, token: str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        self._headers = headers
        self._request = requests.Session()
        self._request.headers.update(self._headers)

    def _post_response(self, url: str, data: BaseModel) -> typing.Optional[requests.Response]:
        """ Posts data to the corresponding url.

            Args:
                url (str): Url to request a response from
                data (BaseModel): Dataclass to post to tthe url
            
            Returns:
                200 Response for the corresponding url, or None
        """
        full_path = self.BASE_URL + url
        json_data = data.model_dump_json()
        response = self._request.post(url=full_path, data=json_data)

        if response.status_code != 200:
            print('Response Status Code Not 200: ', response.status_code, response, response.json())

        return response

    def ask_prompt(
            self,
            prompt: str,
            model: interface.GPTModel = interface.GPTModel.GPT_4,
            temperature: float = 0,
        ) -> typing.Optional[interface.GPTResponseData]:
        """ Ask a prompt to the GPT chatbot.

            Args:
                prompt (str): The prompt to send to the GPT chatbot.
                model (interface.GPTModel): The model to use for the GPT chatbot.
                temperature (float): The temperature to use for the GPT chatbot (0-1).
            
            Returns:
                The response from the GPT chatbot.
        """
        url = UrlDesignator.CHAT_COMPLETIONS
        request_data = interface.GPTRequestData(model=model, messages=[interface.Message(role='user', content=prompt)], temperature=temperature)
        response = self._post_response(url, request_data)
        return interface.GPTResponseData(**response.json()) if response else None
