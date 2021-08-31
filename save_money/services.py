import json
from requests import request, HTTPError
from save_money.models import Category, Token
import config


class SaveMoneyService:

    API_HOST = config.SAVE_MONEY_API_HOST
    header = {'Authorization': None, 'accept': 'application/json'}

    def set_authorization(self, jwt):
        self.header.update({'Authorization': jwt})

    def _send_request(self, path, **kwargs):
        kwargs.update({
            'url': '{host}{path}'.format(host=self.API_HOST, path=path),
            'headers': self.header
        })

        with request(**kwargs) as response:
            try:
                response.raise_for_status()
                return response
            except HTTPError as error:
                print('REQUEST ERROR: ', error.response.__dict__)
                raise

    def get_token(self, user):
        request = {
            'method': 'post',
            'path': 'users/token/',
            'data': user.__dict__
        }

        response = self._send_request(**request)
        return Token(**response.json()['token'])

    def get_categories(self):
        request = {
            'method': 'get',
            'path': 'cash_flow/categories/',
        }

        response = self._send_request(**request)
        return [Category(id=c.get('id'), name=c.get('name'), is_expense=c.get('is_expense'), is_default=c.get('is_default'), category_type=c.get('category_type')) for c in response.json()]

    def create_movimentation(self, movimentation):
        request = {
            'method': 'post',
            'path': 'cash_flow/movimentation/',
            'data': movimentation.__dict__
        }

        response = self._send_request(**request)
        return response.json()
